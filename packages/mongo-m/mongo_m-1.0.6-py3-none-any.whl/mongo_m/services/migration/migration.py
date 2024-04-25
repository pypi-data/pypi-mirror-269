import pymongo, logging
from pymongo.database import Database
from mongo_m.core import MongoDB, get_config
from mongo_m.repository import collections

__all__ = ['connect_to_mongo', 'get_collections', 'get_database', 'delete_fields', 'add_fields']


def connect_to_mongo() -> pymongo.MongoClient:
    """
    Connects to a MongoDB database using environment variables for configuration.

    Returns:
    - pymongo.database.Database: The connected MongoDB database.
    """
    config = get_config()
    return MongoDB(config.get("MONGO", "host"),
                   int(config.get("MONGO", "port")),
                   config.get("MONGO", "user"),
                   config.get("MONGO", "password"))


def get_collections(client: pymongo.MongoClient):
    db = get_database(client)
    return collections.get_fields_collections(db)


def get_database(client: pymongo.MongoClient):
    config = get_config()
    db_name = config.get("MONGO", "database")
    db = collections.find_collections(client, db_name)
    return db


def delete_fields(db: Database, collection_name: str, params):
    if params.empty:
        return
    collections = db.get_collection(collection_name)
    try:
        collections.update_many({"$or": params.query}, {"$unset": params.fields}, upsert=True)
    except Exception as e:
        print(e)


def add_fields(db: Database, collection_name: str, params):
    if params.empty:
        return
    collections = db.get_collection(collection_name)
    try:
        collections.update_many({"$or": params.query}, {"$set": params.fields}, upsert=True)
    except Exception as e:
        print(e)