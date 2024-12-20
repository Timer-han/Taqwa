from internal.storage.question import QuestionRepository


class QuestionService:
    def __init__(self, repository: QuestionRepository) -> None:
        self.repository = repository
