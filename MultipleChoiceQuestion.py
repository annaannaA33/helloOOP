from Question import Question


class MultipleChoiceQuestion(Question):
    def __init__(
        self,
        id,
        question_type,
        question_text,
        correct_answer,
        options,
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
            total_correct_percentage,
        )
        self.options = options


    def as_dict(self):
        return {
            "id": self.id,
            "question_type": self.question_type,
            "question_text": self.question_text,
            "correct_answer": self.correct_answer,
            "options": getattr(self, "options", None),
            "is_active": self.get_is_active(),
            "appearance_count": self.appearance_count,
            "correct_count": self.correct_count,
            "total_correct_percentage": self.total_correct_percentage,
        }

    def get_question_text(self):
        var_options = [self.correct_answer] + self.options
        return f"{super().get_question_text()} Answer Options: {', '.join(var_options)}"
