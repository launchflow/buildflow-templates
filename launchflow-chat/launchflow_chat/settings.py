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
        self.env = Environment(os.getenv("stack", "dev"))
        self.gcp_service_account_info = os.getenv("GCP_SERVICE_ACCOUNT_INFO")
        if self.env == Environment.DEV:
            self.gcp_project_id = os.environ["DEV_GCP_PROJECT_ID"]
        elif self.env == Environment.PROD:
            self.gcp_project_id = os.environ["PROD_GCP_PROJECT_ID"]
        elif self.env == Environment.LOCAL:
            self.gcp_project_id = os.environ["LOCAL_GCP_PROJECT_ID"]
        self.model_bucket_project = os.getenv(
            "MODEL_BUCKET_PROJECT", "launchflow-llama-models"
        )
        self.model_bucket_name = os.getenv(
            "MODEL_BUCKET_NAME", "launchflow-llama-models"
        )
        self.model_path = os.getenv("MODEL_PATH", "llama-2-7b-chat.ggmlv3.q2_K.bin")

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
