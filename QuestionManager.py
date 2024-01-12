from random import shuffle
from FreeFormQuestion import FreeFormQuestion
from MultipleChoiceQuestion import MultipleChoiceQuestion
from FileManager import FileManager
from FreeFormQuestion import FreeFormQuestion
from MultipleChoiceQuestion import MultipleChoiceQuestion


class QuestionManager:
    def __init__(self):
        self.questions = []

    def create_free_form_question(self, question_type, question_text):
        # Ask for question_text and expected_answer, and if everything is ok
        # then save everything in the question_to_be_added list
        correct_answer = input("Enter the answer: ")

        new_question = FreeFormQuestion(
            id=id,
            question_type=question_type,
            question_text=question_text,
            correct_answer=correct_answer,
        )

        return new_question

    def craete_multiple_choice_question(self, question_type, question_text):
        while True:
            try:
                num_options = int(input("Enter the number of answer options (2-5): "))
                if 2 <= num_options <= 5:
                    break
                else:
                    print("Please enter a valid number between 2 and 5.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        options = [
            input(f"Enter incorrect option {i+1}: ") for i in range(num_options - 1)
        ]
        correct_answer = input("Now enter the correct option: ")

        new_question = MultipleChoiceQuestion(
            id=id,
            question_type=question_type,
            question_text=question_text,
            options=options,
            correct_answer=correct_answer,
        )

        print("You have prepared the question for saving.")
        return new_question

    def add_question_menu(self):
        question_to_be_added = []
        new_question = None

        while True:
            print("You are in the question saving menu")
            print(
                "To add questions, follow the instructions. Questions with answer options and free-form questions are available for addition."
            )
            print("To return to the main menu, type 'menu' or 'm'")
            question_type = input(
                "Enter the question type (1 for FreeFormQuestion, 2 for MultipleChoiceQuestion): "
            )
            if question_type == "1" or question_type == "2":
                question_text = input("Enter the question text: ")
                if not question_text or len(question_text) < 5:
                    print("Please, Enter the question")
                else:
                    if question_type == "1":
                        question_type = "free_form_question_type"
                        new_question = self.create_free_form_question(
                            question_type, question_text
                        )
                    elif question_type == "2":
                        question_type = "multiple_choice_question_type"
                        new_question = self.craete_multiple_choice_question(
                            question_type, question_text
                        )
                        # When the question is saved, exit the loop, but not the function. The user is prompted to enter a question again until they exit
                    question_to_be_added.append(new_question)
            elif question_type.lower() == "menu" or question_type.lower() == "m":
                if len(question_to_be_added) > 0:
                    # If at least one question was added to question_to_be_added, return question_to_be_added
                    return question_to_be_added
            else:
                print("Invalid question type.")
