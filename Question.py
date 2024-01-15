from random import choices
import uuid


class Question:
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
        self.id = id
        self.question_type = question_type
        self.question_text = question_text
        self.correct_answer = correct_answer
        self.is_active = is_active
        self.appearance_count = appearance_count  # How many times it has been displayed during testing + practice
        self.correct_count = (
            correct_count  # Total number of correct answers for this question
        )
        self.total_correct_percentage = total_correct_percentage  # Overall percentage of correct answers for this question in practice and test mood
        self.overall_percentage = 0  # Overall Performance Across All Questions
        self.total_questions = 0  # Total number of questions

    def get_question_text(self):
        return self.question_text

    def get_is_active(self):
        return self.is_active

    def get_total_questions(self):
        return self.total_questions

    def generate_id(self):
        self.id = uuid.uuid4()
        return self.id

    def get_weight(self):
        incorrect_attempts = self.appearance_count - self.correct_count
        return incorrect_attempts + 100 / (self.correct_count + 100)

    def update_statistics(self, load_question_list, is_correct):
        for idx, question in enumerate(load_question_list):
            if question.id == self.id:
                question.appearance_count += 1
                # If the answer is correct, update statistics
                if is_correct:
                    self.correct_count += 1
                # Return the updated list of questions
                return load_question_list

        # If the question is not found, return the original list
        return load_question_list

    def get_correct_answer(self):
        return self.correct_answer

    @classmethod
    def overall_performance(cls, question_list):
        total_correct = sum(question.correct_count for question in question_list)
        total_appearances = sum(question.appearance_count for question in question_list)
        overall_percentage = (
            (total_correct / total_appearances) * 100 if total_appearances > 0 else 0
        )
        return round(overall_percentage, 2)

    @classmethod
    def find_active_questions(cls, load_question_list):
        active_questions_list = [
            question for question in load_question_list if question.is_active
        ]
        # Iterate through all questions and select the active ones
        # adding them to the list
        return active_questions_list

    def check_answer(self, question, user_answer):
        return user_answer.lower().strip() == question.correct_answer.lower().strip()

    @classmethod
    def random_chose_question(cls, active_questions_list):
        if not active_questions_list:
            return None
        weights = [q.get_weight() for q in active_questions_list]
        randon_chosen_question = choices(
            active_questions_list, weights=weights, k=1
        ).pop()
        return randon_chosen_question

    def as_dict(self):
        return {
            "id": self.id,
            "question_type": self.question_type,
            "question_text": self.question_text,
            "correct_answer": self.correct_answer,
            "is_active": self.is_active,
            "appearance_count": self.appearance_count,
            "correct_count": self.correct_count,
            "total_correct_percentage": self.total_correct_percentage,
        }
