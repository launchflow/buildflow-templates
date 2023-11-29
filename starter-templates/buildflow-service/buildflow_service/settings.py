"""This file defines any environment variables needed to run."""

import os
from enum import Enum

import dotenv


class Environment(Enum):
    DEV = "dev"
    PROD = "prod"
    LOCAL = "local"


class Settings:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.env = Environment(os.getenv("ENV", "local"))


env = Settings()
