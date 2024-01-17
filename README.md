tasks from sprint 3:
https://submit.cs50.io/users/annaannaA33/cs50/problems/2022/python/

task game  War (sprint 3, part2):
https://github.com/annaannaA33/task-card_war_game


# Learning_tool_app
About app:
Adding questions mode:
In this mode, users can add two types of questions: quiz questions and free-form text questions. A quiz question requires users to choose one correct answer from the provided options, while a free-form question requires users to enter a text response, which will be compared directly with the expected answer for correctness.

All added questions are saved in a file, ensuring persistence across program sessions. The system restricts users from entering practice or test modes until at least 5 questions have been added.

Statistics viewing mode:
This mode displays a comprehensive list of all questions currently within the system. Each question includes its unique ID number, active status, question text, appearance count during practices or tests, and the percentage of correct answers.

Disable/Enable Questions mode:
Users can input the ID of a question to disable or enable it. The system presents detailed information about the question, including its text and answer, and prompts the user for confirmation. Disabled questions do not appear in practice and test modes. The status of enabled/disabled questions is stored in a file, which may be the same as or different from the file containing the questions.

Practice mode:
Practice mode allows users to continuously answer questions, with a twist in the selection process. The system adjusts question probabilities based on user performance – correctly answered questions become less likely to appear, while incorrectly answered questions become more likely. Weighted random choices are utilized for this purpose. The probability adjustments persist between program restarts.

Test mode:
In this mode, users choose the number of questions for the test, ensuring it does not exceed the total number of questions available. Questions are randomly selected, with each question appearing only once at most. After completing the test, users receive a score, and the results, along with the date and time, are saved in a separate results.txt file. The score reflects the percentage of correct answers.

Main Menu Navigation:
The overall program management is centralized through the main menu. Users can seamlessly navigate between different modes by selecting the corresponding options in the main menu. This provides a user-friendly and intuitive interface, enabling users to switch effortlessly between adding questions, viewing statistics, managing question statuses, practicing, and taking tests.

Before entering the statistics or question management mode, it is advisable to reduce the scale, as the table of questions is extensive.

To exit the program, press 'stop' while in the main menu. Alternatively, you can use Ctrl + C, but this method does not guarantee data preservation.

Steps to take before starting:

Install the 'tabulate' package by running the command: pip install tabulate.
Open the terminal in full view.
pip install pytest

Application testing:
During the test I create and save a question in the list, so before restart the test it is important to delete the created question.

------
List of questions(For ease of adding new questions or tests, offer a questionnaire sheet):
id,question_type,question_text,correct_answer,options,is_active,appearance_count,correct_count,total_correct_percentage
d184bbf8-5d36-4f7b-8439-755281a38ddb,free_form_q_type,dddddddd,dddddddddd,,True,0,0,0
03a8908e-9a81-4b7e-8149-34399d06bc35,free_form_q_type,Which river is the longest in Africa?,Nile,,True,0,0,0
a847cdea-01e4-4f56-9f1b-80cff66a5c6d,free_form_q_type,Which river is the longest in Asia?,Yangtze,,True,0,0,0
d0bce567-049a-4194-807c-15a049f3615a,free_form_q_type,What is the capital of France?,Paris,,True,0,0,0
27bb3227-e3ca-4450-b2a5-592e6d1a1134,free_form_q_type,What is the capital of Lithuania?,Vilnius,,True,0,0,0
4c18b89c-d2c3-45c0-a0bf-c9ed612f9808,free_form_q_type,What is the chemical symbol for oxygen?,O,,True,0,0,0
46ad73e4-941c-44a9-ac6b-581f877ac963,free_form_q_type,Which river is the longest in the world?,Amazon,,True,0,0,0
57837ca2-68bb-4f76-86c8-6a6d6c0ff95c,multiple_choice_q_type,What is the name of the largest ocean in the world?,Pacific Ocean,"['Indian Ocean', 'Atlantic Ocean']",True,0,0,0
3bb470ec-0ef5-4f75-a315-05d3dcc000aa,multiple_choice_q_type,hat is the name of the tallest mountain in the world?,Everest,"['Kilimanjaro', 'Fuji']",True,0,0,0
aca08bf7-fb50-4be0-9ffd-cd1085725549,multiple_choice_q_type,What is the name of the largest ocean in the world?,Pacific Ocean,"['Indian Ocean', 'Arctic Ocean']",True,0,0,0
2906b42c-af59-45b0-b53c-0b8a9a13e1f0,multiple_choice_q_type,What is the name of the world's smallest ocean basin?,Arctic Ocean,"['Mediterranean Sea', 'Caribbean Sea']",True,0,0,0
37eef188-81f6-4e68-b98b-6d096b1974f1,multiple_choice_q_type,What is the largest continent in the world?,Asia,"['North America', 'Africa']",True,0,0,0
