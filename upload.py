import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Tuple

import requests
import yaml

# Set global environment variables
os.environ["GCP_PROJECT_ID"] = "launchflow"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "postgres"
os.environ["DEV_GCP_PROJECT_ID"] = "launchflow"
os.environ["PROD_GCP_PROJECT_ID"] = "launchflow"
os.environ["LOCAL_GCP_PROJECT_ID"] = "launchflow"
os.environ["STACK"] = "local"
os.environ["S3_BUCKET_NAME"] = "launchflow"
os.environ["MOTHERDUCK_TOKEN"] = "123"
os.environ["DATABASE_TIER"] = "db-custom-1-3840"
os.environ["DATABASE_PASSWORD"] = "postgres"
os.environ["DATABASE_USER"] = "postgres"
os.environ["CLIENT_ID"] = "123"
os.environ["REDIRECT_URI"] = "http://localhost:3000"
os.environ["CLIENT_SECRET"] = "123"
os.environ["JAVASCRIPT_ORIGINS"] = "http://localhost:3000"
os.environ["CREATE_MODELS"] = "false"
os.environ["MODEL_BUCKET"] = "launchflow"
os.environ["MODEL_PATH"] = "models"
os.environ["MAX_CONTEXT_SIZE"] = "1024"
os.environ["CPUS_PER_REPLICA"] = "2"


successful = []


@dataclass
class Template:
    name: str
    description: str
    tags: List[str]
    cloud_providers: List[str]
    code_preview_path: str
    directory: str

    @property
    def template_flow_path(self) -> str:
        raise NotImplementedError

    @property
    def cwd(self) -> str:
        raise NotImplementedError


@dataclass
class Walkthrough(Template):
    def __post_init__(self):
        self.tags.append("walkthrough")

    @property
    def template_flow_path(self):
        return os.path.join(
            "walkthroughs", self.directory, ".buildflow", "build", "template.flow"
        )

    @property
    def cwd(self) -> str:
        return os.path.join("walkthroughs", self.directory)


@dataclass
class StarterTemplate(Template):
    def __post_init__(self):
        self.tags.append("starter-template")

    @property
    def template_flow_path(self):
        return os.path.join(
            "starter-templates", self.directory, ".buildflow", "build", "template.flow"
        )

    @property
    def cwd(self) -> str:
        return os.path.join("starter-templates", self.directory)


@dataclass
class Sample(Template):
    def __post_init__(self):
        self.tags.append("sample")

    @property
    def template_flow_path(self):
        return os.path.join(
            "samples", self.directory, ".buildflow", "build", "template.flow"
        )

    @property
    def cwd(self) -> str:
        return os.path.join("samples", self.directory)


@dataclass
class BuildFlowTemplates:
    walkthroughs: List[Walkthrough]
    starter_templates: List[StarterTemplate]
    samples: List[Sample]

    def __post_init__(self):
        self.walkthroughs = [Walkthrough(**template) for template in self.walkthroughs]
        self.starter_templates = [
            StarterTemplate(**template) for template in self.starter_templates
        ]
        self.samples = [Sample(**template) for template in self.samples]

    def iter_templates(self):
        for template in self.walkthroughs:
            yield template
        for template in self.starter_templates:
            yield template
        for template in self.samples:
            yield template


def load_yaml(file_path: str) -> BuildFlowTemplates:
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
        return BuildFlowTemplates(**data)


def upload_template_to_fastapi(
    upload_url: str, github_base_url: str, template: Template
):
    github_url = f"{github_base_url}/{template.cwd}"
    data = {
        "display_name": template.name,
        "description": template.description,
        "github_url": github_url,
        "cloud_providers": ",".join(template.cloud_providers),
        "tags": ",".join(template.tags),
        "code_preview": template.code_preview_path,
    }
    files = {"template_flow_file": open(template.template_flow_path, "rb")}

    response = requests.post(upload_url, files=files, data=data)
    return response


def run_command(cwd: str, command: str) -> Tuple[int, str, str]:
    """
    Executes a command in a specified directory.

    :param cwd: The current working directory where the command should be executed.
    :param command: The command to execute.
    :return: A tuple containing the return code, stdout, and stderr of the command.
    """
    try:
        print(f"Running command: {command}")
        result = subprocess.run(
            command, cwd=cwd, shell=True, text=True, capture_output=True, check=True
        )
        print(f"Command result: {result}")
        return (result.returncode, result.stdout, result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        return (e.returncode, e.stdout, e.stderr)


def build_template(template: Template):
    buildflow_build_command = f"buildflow build --as-template"
    return_code, stdout, stderr = run_command(template.cwd, buildflow_build_command)
    if return_code != 0:
        return f"Error building template: {template.name}\nstdout: {stdout}\nstderr: {stderr}"
    successful.append(template.name)
    return "success"


upload_url = "http://localhost:3003/templates/upload"
drop_all_templates_url = "http://localhost:3003/templates/drop"
github_base_url = "https://github.com/launchflow/buildflow-templates/tree/main"

all_templates_file_path = "templates.yaml"
buildflow_templates = load_yaml(all_templates_file_path)

num_success = 0
num_failure = 0
futures = []

# Create a ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    # Submit tasks to the executor
    for template in buildflow_templates.iter_templates():
        print(f"Building template: {template.name}")
        future = executor.submit(build_template, template)
        futures.append(future)

    # Process completed tasks
    for future in as_completed(futures):
        result = future.result()
        if result == "success":
            num_success += 1
        else:
            print(result)
            num_failure += 1

print(f"num_success: {num_success}")
print(f"num_failure: {num_failure}")

for name in successful:
    print(name)


# Clear all templates in the database
response = requests.delete(drop_all_templates_url)
print("DELETE:", response.text)

# Upload all templates to the database
for template in buildflow_templates.iter_templates():
    if template.name not in successful:
        continue
    response = upload_template_to_fastapi(upload_url, github_base_url, template)
    if response.status_code != 200:
        print(f"Error uploading template: {template.name}")
        print(response.text)
