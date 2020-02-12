import logging
import sys
from os import environ
from typing import List

from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from .logging import InterceptHandler

config: Config = Config(".env")

VERSION: str = "0.0.1"
API_PREFIX: str = "/api"

DEBUG: bool = config("DEBUG", cast=bool, default=False)
PROJECT_NAME: str = config("PROJECT_NAME")
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
ALLOWED_HOSTS: List[str] = ["*"]


DB_CONNECTION: str = (
    f"postgresql://{environ.get('POSTGRES_USER')}:{environ.get('POSTGRES_PASSWORD')}"
    f"@hjwzw_postgres_mac:5432/hjwzw"
)
DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL, default=DB_CONNECTION)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)


# logging configuratio
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
