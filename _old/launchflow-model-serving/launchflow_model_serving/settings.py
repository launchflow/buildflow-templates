"""This file defines any environment variables needed to run."""

from enum import Enum
import os

import dotenv


class Environment(Enum):
    DEV = "dev"
    PROD = "prod"
    LOCAL = "local"


class Settings:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.env = Environment(os.getenv("STACK", "local"))
        self.use_gcp = os.getenv("USE_GCP", "false").lower() == "true"
        if self.use_gcp:
            self.gcp_project_id = os.getenv("GCP_PROJECT_ID")
        else:
            self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.gcp_project_id = os.environ["GCP_PROJECT_ID"]
        self.model_bucket = os.environ["MODEL_BUCKET"]
        self.model_path = os.environ["MODEL_PATH"]
        self.max_context_size = os.environ.get("MAX_CONTEXT_SIZE", 1024)
        self.cpus_pre_replics = os.environ.get("CPUS_PER_REPLICA", 2)


env = Settings()
