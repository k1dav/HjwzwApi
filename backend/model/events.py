import asyncpg
from fastapi import FastAPI
from loguru import logger

from . import database


async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to {0}", repr(database.url))

    await database.connect()

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await database.disconnect()

    logger.info("Connection closed")
