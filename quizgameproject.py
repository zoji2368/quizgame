import pandas as pd
import datetime
import time
import os

def get_teacher_input():
    num_questions = int(input("How many questions? "))
    num_options = int(input("How many options per question? "))
    time_limit = int(input("Set the time limit for the quiz (in minutes): "))
    questions = []
    correct_answers = []
    for i in range(num_questions):
        question = input(f"Enter question {i+1}: ")
        options = [input(f"Option {j+1}: ") for j in range(num_options)]
        correct_answer = input(f"Enter the correct answer: ")
        questions.append((question, options))
        correct_answers.append(correct_answer)
    return questions, correct_answers, time_limit

def get_student_info():
    name = input("Enter your name: ")
    student_id = input("Enter your ID: ")
    student_class = input("Enter your class: ")
    return name, student_id, student_class

def run_quiz(questions, correct_answers, time_limit):
    student_answers = []
    start_time = time.time()
    end_time = start_time + time_limit * 60

    print(f"\nThe quiz has started. You have {time_limit} minutes to complete it.\n")

    for question, options in questions:
        current_time = time.time()
        remaining_time = end_time - current_time

        if remaining_time <= 0:
            print("\nTime is up! The quiz will now end.")
            break

        # Display time left before the question
        minutes, seconds = divmod(int(remaining_time), 60)
        print(f"Time left: {minutes} minutes {seconds} seconds")
        print(question)

        for idx, option in enumerate(options):
            print(f"{idx + 1}. {option}")

        answer = input("Your answer: ")
        student_answers.append(answer)

        # Recalculate remaining time after the question
        remaining_time = end_time - time.time()

    return student_answers

def calculate_score(student_answers, correct_answers):
    score = sum(1 for student, correct in zip(student_answers, correct_answers) if student == correct)
    return score

def display_all_scores(students_data, export_option=None):
    if not students_data:
        print("No student data available.")
        return
    
    if export_option == "terminal":
        print("\nAll Students' Scores:")
        for student in students_data:
            print(f"Name: {student['Name']}, ID: {student['ID']}, Class: {student['Class']}, Score: {student['Score']}, Timestamp: {student['Timestamp']}")
    elif export_option == "excel":
        df = pd.DataFrame(students_data)
        df.to_excel("students_scores.xlsx", index=False)
        print("Scores have been saved to 'students_scores.xlsx'.")
        os.system("start students_scores.xlsx")

def main():
    students_data = []
    questions, correct_answers, time_limit = None, None, None
    
    while True:
        print("\nMain Menu:")
        print("1. Take a Quiz")
        print("2. View Student Quiz Marks")
        option = input("Choose an option (1 or 2): ").strip()
        
        if option == "1":
            if questions is None:
                questions, correct_answers, time_limit = get_teacher_input()
            
            name, student_id, student_class = get_student_info()
            timestamp = datetime.datetime.now()
            input("Press Enter to start the quiz...")
            student_answers = run_quiz(questions, correct_answers, time_limit)
            score = calculate_score(student_answers, correct_answers)
            print(f"\nStudent Score: {score}/{len(correct_answers)}")
            
            students_data.append({
                "Name": name,
                "ID": student_id,
                "Class": student_class,
                "Score": score,
                "Timestamp": timestamp
            })
        
        elif option == "2":
            if not students_data:
                print("No student data available to display.")
                continue
            
            print("\nHow would you like to view the scores?")
            print("1. In terminal")
            print("2. Open Excel")
            view_option = input("Choose an option (1 or 2): ").strip()
            
            if view_option == "1":
                display_all_scores(students_data, export_option="terminal")
            elif view_option == "2":
                display_all_scores(students_data, export_option="excel")
            else:
                print("Invalid option.")
        else:
            print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
