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
        self.s3_bucket_name = os.environ["S3_BUCKET_NAME"]
        self.motherduck_token = os.getenv("MOTHERDUCK_TOKEN")


env = Settings()
