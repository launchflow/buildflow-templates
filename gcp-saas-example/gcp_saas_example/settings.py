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
        self.gcp_project_id = os.environ["GCP_PROJECT_ID"]

        # database settings
        self.database_tier = os.getenv("DATABASE_TIER", "db-custom-1-3840")
        self.database_password = os.environ["DATABASE_PASSWORD"]
        self.database_user = os.environ["DATABASE_USER"]

        # auth settings
        self.client_id = os.environ["CLIENT_ID"]
        self.redirect_uri = os.environ["REDIRECT_URI"]
        self.client_secret = os.environ["CLIENT_SECRET"]
        self.javascript_origins = os.environ["JAVASCRIPT_ORIGINS"].split(",")
        self.create_models = os.getenv("CREATE_MODELS", "false").lower() == "true"


env = Settings()
