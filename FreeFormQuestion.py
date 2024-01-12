from Question import Question


class FreeFormQuestion(Question):
    def __init__(
        self,
        id,
        question_type,
        question_text,
        correct_answer,
        is_active=True,
        appearance_count=0,
        correct_count=0,
        total_correct_percentage=0,
    ):
        super().__init__(
            id,
            question_type,
            question_text,
            correct_answer,
            is_active,
            appearance_count,
            correct_count,
            total_correct_percentage=0,
        )

    def get_correct_answer(self):
        return self.correct_answer

    def as_dict(self):
        return {
            "id": self.id,
            "question_type": self.question_type,
            "question_text": self.question_text,
            "correct_answer": self.correct_answer,
            "is_active": self.get_is_active(),
            "appearance_count": self.appearance_count,
            "correct_count": self.correct_count,
            "total_correct_percentage": self.total_correct_percentage,
        }
