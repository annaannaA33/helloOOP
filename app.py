from Player import Player, welcome_player
from FileManager import FileManager
from QuestionManager import QuestionManager
from Question import Question
from random import choices
import sys


def main():
    player = Player()
    file_manager = FileManager()
    question_manager = QuestionManager()
    welcome_player(player)
    main_menu(question_manager, file_manager)

def start_practice(load_question_list, active_questions_list):
    while True:
        if len(active_questions_list) < 5:
            print(
                "To start practicing, there should be at least 5 active questions. Please check the questions list."
            )
            break
        print("You are in practice mode")
        print("To return to the main menu type 'm'")
        one_question = Question.random_chose_question(active_questions_list)

        user_answer = input(f"{one_question.get_question_text()}:\n ")

        if user_answer.lower().strip() == "m":
            # Return to the main menu
            print("Testing mode aborted. Returning to the main menu.")
            break
        elif one_question.check_answer(one_question, user_answer) == True:
            print("Answer is correct")
            one_question.update_statistics(load_question_list, True)
        else:
            one_question.update_statistics(load_question_list, False)
            print(
                f"Answer is incorrect. Correct answer: {one_question.get_correct_answer()}"
            )


def check(questions_asked, active_questions_list):
    while True:
        one_question = Question.random_chose_question(active_questions_list)
        if one_question not in questions_asked:
            return one_question


def start_test(load_question_list, active_questions_list):
    correct = 0
    questions_asked = set()
    num_questions = 0
    print("You are in testing mode")
    print("To return to the main menu type 'm'")

    while True:
        if len(active_questions_list) < 5:
            print(
                "To start practicing, there should be at least 5 active questions. Please check the questions list."
            )
            break
        try:
            num_questions = int(input("Enter the number of questions for the test: "))
            if num_questions <= len(active_questions_list):
                break
        except ValueError:
            print("not anouth questions.")

    for _ in range(num_questions):
        one_question = check(questions_asked, active_questions_list)
        questions_asked.add(one_question)
        user_answer = input(f"{one_question.get_question_text()}:\n ").lower().strip()

        if user_answer.lower().strip() == "m":
            print("Testing mode aborted. Returning to the main menu.")
            break
        if one_question.check_answer(one_question, user_answer):
            correct += 1
            one_question.update_statistics(load_question_list, True)
        else:
            one_question.update_statistics(load_question_list, False)

    # Display test results
    accuracy_percentage = (correct / num_questions) * 100 if num_questions > 0 else 0
    result_string = f"{accuracy_percentage:.2f}%"
    if len(active_questions_list) > 5:
        print(
            f"Test completed. Correct answers: {correct}/{num_questions} ({result_string})"
        )

    return result_string


def print_ruls():
    print(
        "Welcome! Rules and instructions: The program will keep running until you choose to stop."
        "Program Usage:\n"
        "1. Adding Questions: Select '1' to add quiz or free-form text questions. Questions are saved for future sessions.\n"
        "2. View Statistics: Select '2' to see statistics for all questions, including ID, activity status, text, and performance percentages.\n"
        "3. Disable/Enable Questions: Select '3' to disable or enable specific questions by entering their ID.\n"
        "4. Practice Mode: Select '4' to practice questions. The program adapts, showing questions answered incorrectly more often.\n"
        "5. Test Mode: Select '5' to take a test. Choose the number of questions, and receive a score with percentages.\n"
        "Note: At least 5 questions must be added before entering practice or test modes.\n\n"
        "To stop type 'stop."
    )


def print_menu():
    menu_options = [
        "1. Adding questions",
        "2. Statistics viewing",
        "3. Disable/enable questions",
        "4. Practice mode",
        "5. Test mode",
    ]

    max_length = max(len(option) for option in menu_options)

    print(f"+{'-' * (max_length + 2)}+")
    for option in menu_options:
        padding = (max_length - len(option)) // 2
        print(f"|{' ' * padding}{option}{' ' * (max_length - len(option) - padding)}|")
    print(f"+{'-' * (max_length + 2)}+")


def main_menu(question_manager, file_manager):
    print_ruls()

    while True:
        print_menu()
        player_choice = input("Enter your choice: ")
        if player_choice.lower().strip() == "stop":
            sys.exit("Exiting the program. Goodbye!")

        # Add question, save question
        elif player_choice == "1":
            new_question_list = []
            new_question_list = question_manager.add_question_menu()
            if len(new_question_list) > 0:
                file_manager.save_new_questions(new_question_list)
                print("The list of questions has been successfully updated")
            else:
                print("You haven't saved any questions")

        # Print the questions from file manager with statistics
        elif player_choice == "2":
            load_question_list = []
            load_question_list = file_manager.load_questions_from_csv()
            file_manager.print_questions_table(load_question_list)
            total_questions = len(load_question_list)
            if total_questions == 0:
                return 0
            overall_percentage = Question.overall_performance(load_question_list)
            print(f"Overall Performance Across All Questions: {overall_percentage}%")
            print(f"Total_questions: {total_questions}")

        # Disable/Enable Questions
        elif player_choice == "3":
            # print the questions from file manager
            file_manager.question_activity_control()

        # Practice_mood
        elif player_choice == "4":
            load_question_list = []
            load_question_list = file_manager.load_questions_from_csv()
            active_questions_list = Question.find_active_questions(load_question_list)
            start_practice(load_question_list, active_questions_list)
            updated_load_question_list = load_question_list  # with updated statistics
            # Get the updated list with statistics and update file with questions
            file_manager.update_data(updated_load_question_list)
        # Test_mood
        elif player_choice == "5":
            load_question_list = []
            load_question_list = file_manager.load_questions_from_csv()
            active_questions_list = Question.find_active_questions(load_question_list)
            result_string = start_test(load_question_list, active_questions_list)

            updated_load_question_list = load_question_list
            # Save results using FileManager
            file_manager.save_test_results(result_string)
            file_manager.update_data(load_question_list)

        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()


#tasks from sprint 3: https://submit.cs50.io/users/annaannaA33/cs50/problems/2022/python/

#task game War (sprint 3, part2): https://github.com/annaannaA33/task-card_war_game
