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
    
    def get_by_uuid(self, uuid: str):
        document = self.collection.find({"uuid": uuid})
        if document is None:
            return None

        values = list(document.clone())
        if len(values) != 1:
            logging.warning("there are not 1 value in suggestion by uuid: %s", uuid)
        
        suggest_data = {field: values[0].get(field) for field in Suggest.__annotations__.keys()}
        logging.info("getting suggest by uuid: %s", suggest_data)
        return Suggest(**suggest_data)

    def get_for_review(self) -> Optional[Suggest]:
        documents = self.collection.find().sort({"created_at": -1}).limit(1)
        if documents is None:
            return None
    
        values = list(documents.clone())
        if len(values) != 1:
            logging.warning("there are not 1 value in suggestion for review: %s", len(list(documents)))
            return None
        
        suggest_data = {field: values[0].get(field) for field in Suggest.__annotations__.keys()}
        logging.info("getting suggest for review: %s", suggest_data)
        return Suggest(**suggest_data)
    
    def update(self, suggest: Suggest):
        self.collection.replace_one({"uuid": suggest.uuid}, suggest.model_dump(exclude_none=True))
