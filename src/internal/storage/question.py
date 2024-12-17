from .mongo import MongoDatabase


class QuestionRepository:
    def __init__(self, db: MongoDatabase):
        self.collection = db.get_collection("question")
