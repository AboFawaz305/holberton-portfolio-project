"""Database connection
"""
from os import environ

from pymongo import MongoClient


def get_db_connection(host=environ.get("MONGO_DB_HOST", "localhost")):
    """Connect to the database"""

    return MongoClient(host, 27017)


def get_engine_db():
    """Get an instance from the main database for the backend"""
    return get_db_connection().engine
