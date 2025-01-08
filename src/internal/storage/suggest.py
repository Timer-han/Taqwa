from .mongo import MongoDatabase
from typing import Optional
import logging

from internal.models.suggest import Suggest
from internal.models.user import User


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

    def get_for_review(self, user: User) -> Optional[Suggest]:
        power_of_two = 15
        prev_limit = 0

        for power in range(4, power_of_two):
            curr_limit = 2 ** power

            documents = self.collection.find().sort({"created_at": -1}).limit(curr_limit)

            if documents is None:
                return None

            values = list(documents.clone())
            if len(values) == 0:
                logging.warning("there are 0 value in suggestion for review: %s", len(list(documents)))
                return None
            
            for question in range(prev_limit, min(curr_limit, len(values))):
                suggest_data = {field: values[question].get(field) for field in Suggest.__annotations__.keys()}
                logging.info("getting suggest for review: %s", suggest_data)

                telegram_id = user.telegram_id
                checking_array = []
                if suggest_data.get("marked_as_correct"): checking_array += suggest_data.get("marked_as_correct")
                if suggest_data.get("marked_as_improve"): checking_array += suggest_data.get("marked_as_improve")
                if suggest_data.get("marked_as_erroneous"): checking_array += suggest_data.get("marked_as_erroneous")

                flag = False
                for checking_user in checking_array:
                    if checking_user.get("telegram_id") and checking_user.get("telegram_id") == telegram_id:
                        flag = True
                        break
                if not flag:
                    logging.info(suggest_data)
                    return Suggest(**suggest_data)

            prev_limit = curr_limit
            if len(values) < curr_limit:
                break
        return None
    
    def update(self, suggest: Suggest):
        self.collection.replace_one({"uuid": suggest.uuid}, suggest.model_dump(exclude_none=True))
