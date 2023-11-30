from buildflow import Service

from saas_starter.processors.hello_world import hello_world_endpoint

service = Service(service_id="hello-world-service")
service.add_endpoint(hello_world_endpoint)
