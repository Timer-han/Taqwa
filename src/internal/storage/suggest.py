from .mongo import MongoDatabase
from typing import Optional
import logging

from internal.models.suggest import Suggest


class SuggestRepository:
    def __init__(self, db: MongoDatabase):
        self.collection = db.get_collection("suggest")

    def create(self, suggest: Suggest):
        logging.info("creating suggest question: %s", suggest.dict(exclude_none=True))
        self.collection.insert_one(suggest.dict(exclude_none=True))

    def get_for_review(self) -> Optional[Suggest]:
        document = self.collection.find().sort({"created_at": -1}).limit(1)
        if document is None:
            return None
        
        suggest_data = {field: document.get(field) for field in Suggest.__annotations__.keys()}
        logging.info("getting suggest for review: %s", suggest_data)
        return Suggest(**suggest_data)
    