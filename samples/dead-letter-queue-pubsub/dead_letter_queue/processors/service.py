from buildflow import Service

from dead_letter_queue.processors.hello_world import hello_world_endpoint

service = Service(service_id="hello-world-service")
service.add_endpoint(hello_world_endpoint)
