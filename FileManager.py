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

    def save_new_questions(self, new_question_list):
        header = [
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
        if (
            not os.path.isfile(self.QUESTIONS_FILE)
            or os.path.getsize(self.QUESTIONS_FILE) == 0
        ):
            with open(self.QUESTIONS_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()

        with open(self.QUESTIONS_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "id",
                    "question_type",
                    "question_text",
                    "correct_answer",
                    "options",
                    "is_active",
                    "appearance_count",
                    "correct_count",
                    "total_correct_percentage",
                ],
            )
            for question in new_question_list:
                writer.writerow(question.as_dict())

    def update_data(self, new_question_list):
        all_updated_questions = new_question_list
        for update_question in new_question_list:
            update_question.total_correct_percentage = (
                update_question.correct_count / update_question.appearance_count
                if update_question.appearance_count > 0
                else 0
            ) * 100
            self.save(all_updated_questions)

    # save new data to the file
    def save(self, all_questions):
        header = [
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
        with open(self.QUESTIONS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for question in all_questions:
                writer.writerow(question.as_dict())

    def load_questions_from_csv(self):
        # Load questions from the file
        question_list = []

        with open(self.QUESTIONS_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                question_type = row["question_type"]
                if question_type not in [
                    "free_form_q_type",
                    "multiple_choice_q_type",
                ]:
                    print(f"Unknown question type: {question_type}")
                    continue

                # Convert values to the required data types
                id = row["id"]
                question_type = row["question_type"]
                question_text = row["question_text"]
                correct_answer = row["correct_answer"]
                is_active = row["is_active"].lower() == "true"
                appearance_count = int(row["appearance_count"])
                correct_count = (
                    int(row["correct_count"]) if row["correct_count"] is not None else 0
                )
                total_correct_percentage = (
                    float(row["total_correct_percentage"])
                    if row["total_correct_percentage"] is not None
                    else 0
                )

                # Create a question object and add it to the list
                if row["question_type"] == "free_form_q_type":
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

                elif row["question_type"] == "multiple_choice_q_type":
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
            # Use an empty string if the attribute is missing
            # options = ", ".join(getattr(question, "options", []))

            row = [
                question.id,
                question.question_type,
                "Yes" if question.is_active else "No",
                question.question_text,
                question.correct_answer,
                question.appearance_count,
                question.correct_count,
                f"{question.total_correct_percentage :.2f} %",
            ]

            table_data.append(row)

        # Table header
        headers = [
            "ID",
            "Type",
            "Active",
            "Question",
            "Correct\nanswer",
            "Appearance\n Count",
            "Total\n Correct",
            "Correct %",
        ]
        colored_headers = [
            f"{Fore.GREEN}{header}{Style.RESET_ALL}" for header in headers
        ]
        print(tabulate(table_data, headers=colored_headers, tablefmt="pretty"))

    def print_question(self, question):
        print(f"ID: {question.id}")
        print(f"Question Text: {question.question_text}")
        print(f"Answer: {question.correct_answer}")

    def question_activity_control(self):
        question_list_print = []
        question_list_print = self.load_questions_from_csv()
        print("You are in the question activity mode.")
        self.print_questions_table(question_list_print)

        while True:
            id_switch = input(
                "Write the ID of the question you want to enable, disable, or delete (or 'm' to return to the main menu): "
            )

            if id_switch.lower().strip() == "m":
                # Check for changes and save if there are any
                self.save(question_list_print)
                print("Changes have been successfully saved.")
                break

            try:
                id_switch = id_switch
                selected_question = next(
                    (q for q in question_list_print if q.id == id_switch), None
                )

                if selected_question:
                    switch_command = input("Choose 'enable', 'disable', or 'delete': ")

                    if switch_command.lower().strip() == "enable":
                        self.print_question(selected_question)
                        confirm = input(
                            f"Are you sure you want to activate question {selected_question.id}? (y/n): "
                        )
                        if confirm.lower().strip() == "y":
                            selected_question.is_active = True
                            print(
                                f"Question {selected_question.id} successfully activated."
                            )
                        else:
                            print("Activation canceled.")
                    elif switch_command.lower().strip() == "disable":
                        self.print_question(selected_question)
                        confirm = input(
                            f"Are you sure you want to deactivate the question {selected_question.id}? (y/n): "
                        )
                        if confirm.lower().strip() == "y":
                            selected_question.is_active = False
                            print(
                                f"Question {selected_question.id} successfully deactivated."
                            )
                        else:
                            print("Deactivation canceled.")
                    elif switch_command.lower().strip() == "delete":
                        self.print_question(selected_question)
                        confirm = input(
                            f"Are you sure you want to delete the question {selected_question.id}? (y/n): "
                        )
                        if confirm.lower().strip() == "y":
                            question_list_print.remove(selected_question)
                            print(
                                f"Question {selected_question.id} successfully has been deleted."
                            )
                        else:
                            print("Deletion canceled.")
                    else:
                        print(
                            "Invalid command. Please enter 'enable', 'disable', or 'delete'."
                        )
                else:
                    print(
                        "Question not found. Enter a valid ID. To return to the main menu type 'm'."
                    )
            except ValueError:
                print(
                    "Invalid input. Please enter a valid ID or 'm' to return to the main menu."
                )

    def save_test_results(self, result_string):
        with open("results.txt", "a") as file:
            timestamp = datetime.datetime.now().isoformat()
            file.write(f"{timestamp} - {result_string}\n")
