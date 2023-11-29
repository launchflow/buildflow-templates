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
        self.env = Environment(os.getenv("stack", "local"))
        self.gcp_service_account_info = os.getenv("GCP_SERVICE_ACCOUNT_INFO")
        self.gcp_project_id = os.getenv("GCP_PROJECT_ID")


env = Settings()
