from buildflow import endpoint
from buildflow.exceptions import HTTPException
from buildflow.dependencies import dependency, Scope
from buildflow.responses import RedirectResponse
from google_auth_oauthlib import flow as google_auth_flow
from starlette.requests import Request


from launchflow_chat.settings import env


SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


@dependency(scope=Scope.REPLICA)
class AuthFlow:
    def __init__(self):
        self.client = google_auth_flow.Flow.from_client_config(
            {
                "web": {
                    "client_id": env.client_id,
                    "project_id": env.gcp_project_id,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": env.client_secret,
                    "redirect_uris": [
                        env.redirect_uri,
                    ],
                    "javascript_origins": env.javascript_origins,
                }
            },
            scopes=SCOPES,
        )
        self.client.redirect_uri = env.redirect_uri


@endpoint(route="/auth/login", method="GET")
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


@endpoint("/auth/callback/google", method="GET")
async def auth_callback(request: Request, auth_flow: AuthFlow):
    code = request.query_params.get("code")
    if code is None:
        raise HTTPException(401)
    user_id_token = fetch_id_token(code, auth_flow)
    request.session["id_token"] = user_id_token
    return RedirectResponse("/")


@endpoint("/auth/logout", method="GET")
async def auth_logout(request: Request):
    request.session.pop("id_token", None)
    return "logged out"
