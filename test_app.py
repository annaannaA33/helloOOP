import pytest
from app import Question
from FileManager import FileManager
from Question import Question
from QuestionManager import QuestionManager


def test_save_questions_to_csv():
    # Creating a free_form_question_type question for testing
    question1 = Question(
        id=1,
        question_type="free_form_question_type",
        question_text="What is your name?",
        correct_answer="Anya",
        is_active=True,
        appearance_count=10,
        correct_count=5,
    )

    # Creating an instance of the FileManager
    file_manager = FileManager()

    # Save the question to CSV
    file_manager.save_questions_to_csv([question1])

    # Load the questions from CSV to check if the saved data is correct
    loaded_questions = file_manager.load_questions_from_csv()

    # Assert that the loaded question matches the original question
    assert len(loaded_questions) == 10
    assert loaded_questions[0].id == 1
    assert loaded_questions[0].question_type == "free_form_question_type"
    assert loaded_questions[0].question_text == "What is your name?"
    assert loaded_questions[0].correct_answer == "Anya"
    assert loaded_questions[0].is_active is True
    assert loaded_questions[0].appearance_count == 10
    assert loaded_questions[0].correct_count == 5


def test_load_questions_from_csv():
    # Assuming 'questions.csv' contains valid data
    file_manager = FileManager()
    loaded_questions = file_manager.load_questions_from_csv()

    # Assert that the loaded questions list is not empty
    assert len(loaded_questions) > 0
    assert len(loaded_questions) == 10

    # Assert that each loaded question is an instance of the Question class
    for question in loaded_questions:
        assert isinstance(question, Question)

    # Check the details of specific questions in the loaded list
    assert loaded_questions[0].id == 1
    assert loaded_questions[0].question_type == "free_form_question_type"
    assert loaded_questions[0].question_text == "What is your name?"
    assert loaded_questions[0].correct_answer == "Anya"
    assert loaded_questions[0].is_active is True
    assert loaded_questions[0].appearance_count == 10
    assert loaded_questions[0].correct_count == 5
    assert loaded_questions[0].total_correct_percentage == 0


def test_create_free_form_question(monkeypatch):
    # Создаем объект QuestionManager
    question_manager = QuestionManager()

    # Подготавливаем тестовые данные
    question_type = "free_form_question_type"
    question_text = "What is your name?"
    correct_answer = "Anya"

    # Имитируем ввод пользователя
    inputs = ["Anya"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

    # Вызываем тестируемый метод
    new_question = question_manager.create_free_form_question(
        question_type, question_text
    )

    # Проверяем, что объект создан корректно
    assert new_question.id is not None
    assert new_question.question_type == question_type
    assert new_question.question_text == question_text
    assert new_question.correct_answer == correct_answer
