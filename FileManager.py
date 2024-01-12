from Question import Question
import datetime
from MultipleChoiceQuestion import MultipleChoiceQuestion
from FreeFormQuestion import FreeFormQuestion
from typing import Union
import os
import csv
import ast
from tabulate import tabulate
from colorama import Fore, Style
from datetime import date


class FileManager:
    def __init__(self):
        self.QUESTIONS_FILE = "questions.csv"

    def save_questions_to_csv(self, new_question_list):
        existing_questions = self.load_questions_from_csv()
        all_updated_questions = []

        for new_question in new_question_list:
            question_added = False  # Flag to check if the question has been added to all_updated_questions

            for existing_question in existing_questions:
                if new_question.question_text == existing_question.question_text:
                    existing_question.appearance_count += new_question.appearance_count
                    existing_question.correct_count += new_question.correct_count
                    question_added = (
                        True  # Set the flag since the question has already been processed
                    )
                    break

            if not question_added:
                # If the question has not been added, add it to all_updated_questions
                all_updated_questions.append(new_question)

        # Now add the remaining existing questions that have not been processed
        all_updated_questions.extend(
            existing_question
            for existing_question in existing_questions
            if existing_question not in all_updated_questions
        )

        # Reset unique identifiers
        for i, question in enumerate(all_updated_questions, start=1):
            question.id = i

        # Save the updated list of questions to the file
        self.save_prepeared_questions_to_file(all_updated_questions)

    def save_prepeared_questions_to_file(self, all_questions):
        with open(self.QUESTIONS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "id",
                    "question_type",
                    "question_text",
                    "correct_answer",
                    "options",
                    "is_active",
                    "appearance_count",
                    "correct_count",
                    "total_correct_percentage",
                ]
            )

            for question in all_questions:
                row_data = {
                    "id": question.id,
                    "question_type": question.question_type,
                    "question_text": question.get_question_text(),
                    "correct_answer": question.correct_answer,
                    "options": getattr(question, "options", None),
                    "is_active": question.get_is_active(),
                    "appearance_count": question.appearance_count,
                    "correct_count": question.correct_count,
                    "total_correct_percentage": question.total_correct_percentage,
                }

                writer.writerow([row_data[field] for field in row_data])

    def load_questions_from_csv(self):
        # Load questions from the file
        question_list = []

        with open(self.QUESTIONS_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                question_type = row["question_type"]
                if question_type not in [
                    "free_form_question_type",
                    "multiple_choice_question_type",
                ]:
                    print(f"Error: Unknown question type: {question_type}")
                    continue

                # Convert values to the required data types
                id = int(row["id"])
                question_type = row["question_type"]
                question_text = row["question_text"]
                correct_answer = row["correct_answer"]
                is_active = row["is_active"].lower() == "true"
                appearance_count = int(row["appearance_count"])
                correct_count = int(row["correct_count"])
                total_correct_percentage = round(float(row["total_correct_percentage"]))

                # Create a question object and add it to the list
                if row["question_type"] == "free_form_question_type":
                    question = FreeFormQuestion(
                        id=id,
                        question_type=question_type,
                        question_text=question_text,
                        correct_answer=correct_answer,
                        is_active=is_active,
                        appearance_count=appearance_count,
                        correct_count=correct_count,
                        total_correct_percentage=total_correct_percentage,
                    )
                    question_list.append(question)

                elif row["question_type"] == "multiple_choice_question_type":
                    options = ast.literal_eval(row["options"]) if row["options"] else []
                    question = MultipleChoiceQuestion(
                        id=id,
                        question_type=question_type,
                        question_text=question_text,
                        correct_answer=correct_answer,
                        options=options,
                        is_active=is_active,
                        appearance_count=appearance_count,
                        correct_count=correct_count,
                        total_correct_percentage=total_correct_percentage,
                    )
                    question_list.append(question)

        return question_list

    def print_questions_table(self, questions):
        # Prepare data for tabulation
        table_data = []
        for question in questions:
            # total_correct_percentage = question.total_correct_percentage
            correct_percentage = (
                (question.correct_count / question.appearance_count) * 100
                if question.appearance_count > 0
                else 0
            )

            # Use an empty string if the attribute is missing
            correct_answer = getattr(question, "correct_answer", "")
            options = ", ".join(getattr(question, "options", []))

            row = [
                question.id,
                question.question_type,
                "Yes" if question.is_active else "No",
                question.question_text,
                correct_answer,
                options,
                question.appearance_count,
                f"{correct_percentage:.2f} %",
                question.correct_count,
            ]

            table_data.append(row)

        # Table header
        headers = [
            "ID",
            "Type",
            "Active",
            "Question",
            "Correct\nanswer",
            "Options",
            "Appearance\n Count",
            "Correct %",
            "Total\n Correct",
        ]
        colored_headers = [
            f"{Fore.GREEN}{header}{Style.RESET_ALL}" for header in headers
        ]
        print(tabulate(table_data, headers=colored_headers, tablefmt="pretty"))

    def question_activity_control(self):
        question_list_print = []
        question_list_print = self.load_questions_from_csv()
        print("You are in the question activity management mode.")
        self.print_questions_table(question_list_print)

        while True:
            id_switch = input(
                "Write the ID of the question you want to enable, disable, or delete (or 'main_menu' to return to the main menu): "
            )

            if id_switch.lower() == "main_menu" or id_switch.lower() == "m":
                # Check for changes and save if there are any
                self.save_prepeared_questions_to_file(question_list_print)
                print("Changes have been successfully saved.")
                break

            try:
                id_switch = int(id_switch)
                selected_question = next(
                    (q for q in question_list_print if q.id == id_switch), None
                )

                if selected_question:
                    switch_command = input("Choose 'enable', 'disable', or 'delete': ")

                    if switch_command.lower() == "enable":
                        selected_question.is_active = True
                    elif switch_command.lower() == "disable":
                        selected_question.is_active = False
                    elif switch_command.lower() == "delete":
                        question_list_print.remove(selected_question)
                        print(f"Question with ID {id_switch} has been deleted.")

                    else:
                        print(
                            "Invalid command. Please enter 'enable', 'disable', or 'delete'."
                        )
                else:
                    print(
                        "Question not found. Enter a valid ID. To return to the main menu type 'm' or 'main_menu'"
                    )
            except ValueError:
                print(
                    "Invalid input. Please enter a valid ID or 'main_menu' to return to the main menu."
                )

    def save_test_results(self, result_string):
        with open("results.txt", "a") as file:
            timestamp = datetime.datetime.now().isoformat()
            file.write(f"{timestamp} - {result_string}\n")
