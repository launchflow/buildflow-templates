from buildflow import Service

from long_running_workflows.processors.hello_world import hello_world_endpoint

service = Service(service_id="hello-world-service")
service.add_endpoint(hello_world_endpoint)
