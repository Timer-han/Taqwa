from pymongo import MongoClient

from config.config import DbConfig


class MongoDatabase:
    def __init__(self, cfg: DbConfig):
        client = MongoClient(f"mongodb://{cfg.username}:{cfg.password}@{cfg.host}:{cfg.port}/")
        self.db = client[cfg.database]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]
