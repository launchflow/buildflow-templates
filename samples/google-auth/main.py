"""Sample for how to authenticate google users using OAuth2."""

import os
import uuid

from buildflow import Flow
from buildflow.exceptions import HTTPException
from buildflow.dependencies import dependency, Scope
from buildflow.dependencies.auth import AuthenticatedGoogleUserDepBuilder
from buildflow.middleware import SessionMiddleware
from buildflow.requests import Request
from buildflow.responses import RedirectResponse

from google_auth_oauthlib import flow as google_auth_flow


app = Flow()

service = app.service(service_id="auth-sample")
service.add_middleware(SessionMiddleware, secret_key=str(uuid.uuid4()))

# Set up a google user if the user is authenticated
# We use `session_id_token` to indicate we can use "token_id" from the session
# to fetch the user id token.
MaybeAuthenticatedGoogleUser = AuthenticatedGoogleUserDepBuilder(
    session_id_token="id_token", raise_on_unauthenticated=False
)


@service.endpoint(route="/", method="GET")
async def index(user_dep: MaybeAuthenticatedGoogleUser) -> str:
    if user_dep.google_user is None:
        return RedirectResponse("/auth/login")
    return f"Hello {user_dep.google_user.name}"


@dependency(scope=Scope.REPLICA)
class AuthFlow:
    def __init__(self):
        self.client = google_auth_flow.Flow.from_client_config(
            {
                "web": {
                    "client_id": os.environ["CLIENT_ID"],
                    "client_secret": os.environ["CLIENT_SECRET"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": [
                        "http://localhost:8000/auth/callback/google",
                    ],
                    "javascript_origins": "http://localhost:8000",
                }
            },
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
        )
        self.client.redirect_uri = "http://localhost:8000/auth/callback/google"


@service.endpoint(route="/auth/login", method="GET")
async def auth_login(auth_flow: AuthFlow):
    authorization_url, state = auth_flow.client.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        approval_prompt="force",
    )
    return RedirectResponse(authorization_url)


def fetch_id_token(code: str, auth_flow: AuthFlow) -> str:
    creds = dict(auth_flow.client.fetch_token(code=code))
    return creds["id_token"]


@service.endpoint("/auth/callback/google", method="GET")
async def auth_callback(request: Request, auth_flow: AuthFlow):
    code = request.query_params.get("code")
    if code is None:
        raise HTTPException(401)
    user_id_token = fetch_id_token(code, auth_flow)
    request.session["id_token"] = user_id_token
    return RedirectResponse("/")
