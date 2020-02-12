import databases

from core.config import DATABASE_URL

from . import base

database = databases.Database(DATABASE_URL)
