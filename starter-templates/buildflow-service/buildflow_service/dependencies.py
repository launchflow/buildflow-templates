"""This file can contain all of the dependencies needed by your flow.

For example if you needed a authenticated google user: https://docs.launchflow.com/buildflow/dependencies/auth

    from buildflow.dependencies.auth import AuthenticatedGoogleUserDepBuilder

    AuthenticatedGoogleUserDep = AuthenticatedGoogleUserDepBuilder()

Then in your buildflow_service/service.py file you can use
the dependency like so:

    @endpoint("/", method="GET")
    def hello_world_endpoint(user_dep: AuthenticatedGoogleUserDep) -> str:
        return "Hello World!"
"""
