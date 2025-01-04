import os
import time
import pandas as pd
import datetime
import pickle

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def save_quiz(questions, correct_answers, time_limit):
    """Saves the quiz data to a file for reuse."""
    with open("quiz_data.pkl", "wb") as file:
        pickle.dump((questions, correct_answers, time_limit), file)
    print("Quiz saved successfully.")

def load_quiz():
    """Loads the quiz data from a file."""
    if os.path.exists("quiz_data.pkl"):
        with open("quiz_data.pkl", "rb") as file:
            return pickle.load(file)
    else:
        print("No previously saved quiz found.")
        return None, None, None

def get_teacher_input():
    """Allows the teacher to input questions, options, and correct answers."""
    num_questions = int(input("How many questions? "))
    time_limit = int(input("Set the time limit for the quiz (in minutes): "))
    questions = []
    correct_answers = []
    
    for i in range(num_questions):
        print(f"\nAdding Question {i + 1}")
        print("1. Multiple Choice")
        print("2. True or False")
        print("3. Direct Question")
        question_type = input("Choose question type (1, 2, or 3): ").strip()
        
        if question_type == "1":
            question = input("Enter the question: ")
            num_options = int(input("How many options? "))
            options = [input(f"Option {j+1}: ") for j in range(num_options)]
            correct_answer = input("Enter the correct answer: ")
            questions.append((question, options, "multiple_choice"))
            correct_answers.append(correct_answer)
        
        elif question_type == "2":
            question = input("Enter the question: ")
            options = ["True", "False"]
            correct_answer = input("Enter the correct answer (True/False): ").strip()
            questions.append((question, options, "true_false"))
            correct_answers.append(correct_answer)
        
        elif question_type == "3":
            question = input("Enter the direct question: ")
            correct_answer = input("Enter the correct answer: ")
            questions.append((question, None, "direct"))
            correct_answers.append(correct_answer)
        
        else:
            print("Invalid choice. Skipping this question.")
    
    save_quiz(questions, correct_answers, time_limit)
    return questions, correct_answers, time_limit

def get_student_info():
    """Collects student information."""
    name = input("Enter your name: ")
    student_id = input("Enter your ID: ")
    student_class = input("Enter your class: ")
    return name, student_id, student_class

def run_quiz(questions, correct_answers, time_limit):
    """Runs the quiz for the student and collects their answers."""
    student_answers = []
    start_time = time.time()
    end_time = start_time + time_limit * 60

    print(f"\nThe quiz has started. You have {time_limit} minutes to complete it.\n")

    for idx, (question, options, q_type) in enumerate(questions):
        current_time = time.time()
        remaining_time = end_time - current_time

        if remaining_time <= 0:
            print("\nTime is up! The quiz will now end.")
            break

        # Display time left before the question
        minutes, seconds = divmod(int(remaining_time), 60)
        print(f"Time left: {minutes} minutes {seconds} seconds")
        print(f"Question {idx + 1}: {question}")

        if q_type == "multiple_choice" and options:
            for idx, option in enumerate(options):
                print(f"{idx + 1}. {option}")
            answer = input("Your answer: ")
        elif q_type == "true_false":
            print("1. True")
            print("2. False")
            answer = input("Your answer: ").strip()
            answer = "True" if answer == "1" else "False"
        elif q_type == "direct":
            answer = input("Your answer: ")
        else:
            print("Invalid question type. Skipping.")
            continue

        student_answers.append(answer)

    return student_answers

def calculate_score(student_answers, correct_answers):
    """Calculates the student's score."""
    score = sum(1 for student, correct in zip(student_answers, correct_answers) if student == correct)
    return score

def provide_feedback(questions, student_answers, correct_answers):
    """
    Provides feedback on the quiz, showing which answers were correct
    and which were wrong, along with the correct answers for wrong responses.
    """
    print("\nFeedback on your quiz:")
    for idx, ((question, options, q_type), student_answer, correct_answer) in enumerate(zip(questions, student_answers, correct_answers)):
        print(f"\nQuestion {idx + 1}: {question}")
        if options:
            print("Options:")
            for option in options:
                print(f" - {option}")
        print(f"Your Answer: {student_answer}")
        
        if student_answer == correct_answer:
            print("Result: ✅ Correct")
        else:
            print("Result: ❌ Wrong")
            print(f"The Correct Answer: {correct_answer}")

def show_feedback_option(questions, student_answers, correct_answers):
    """Allows the student to choose to see their feedback or skip."""
    while True:
        print("\nWould you like to review your answers?")
        print("1. View feedback")
        print("2. Skip")
        option = input("Choose an option (1 or 2): ").strip()

        if option == "1":
            provide_feedback(questions, student_answers, correct_answers)
            break
        elif option == "2":
            print("Feedback skipped.")
            break
        else:
            print("Invalid choice. Please choose 1 or 2.")

def display_all_scores(students_data, export_option=None):
    """Displays all students' scores."""
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
            print("\nQuiz Options:")
            print("1. Create a New Quiz")
            print("2. Use a Previously Created Quiz")
            quiz_option = input("Choose an option (1 or 2): ").strip()
            
            if quiz_option == "1":
                questions, correct_answers, time_limit = get_teacher_input()
            elif quiz_option == "2":
                questions, correct_answers, time_limit = load_quiz()
                if not questions:
                    print("No quiz found. Please create a new quiz.")
                    continue
            else:
                print("Invalid option.")
                continue
            
            clear_screen()  # Clear the screen to hide the questions and answers
            print("\nThe quiz setup is complete.")
            print("Now, let the student enter their details.")
            
            name, student_id, student_class = get_student_info()
            timestamp = datetime.datetime.now()
            input("Press Enter to start the quiz...")
            student_answers = run_quiz(questions, correct_answers, time_limit)
            score = calculate_score(student_answers, correct_answers)
            print(f"\nStudent Score: {score}/{len(correct_answers)}")
            show_feedback_option(questions, student_answers, correct_answers)  # Feedback option
            
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
