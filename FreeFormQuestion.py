from Question import Question


class FreeFormQuestion(Question):
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
