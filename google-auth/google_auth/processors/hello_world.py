from buildflow import endpoint

@endpoint("/", method="GET")
def hello_world_endpoint() -> str:
    return "Hello World!"
