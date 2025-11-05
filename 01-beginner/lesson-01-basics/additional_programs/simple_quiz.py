"""
Simple Quiz Program
This program demonstrates basic Python concepts through a simple quiz game.
"""

def ask_question(question, options, correct_answer):
    """Ask a question and check the answer."""
    print(question)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            answer = int(input("Enter your answer (1-4): "))
            if 1 <= answer <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    if answer == correct_answer:
        print("Correct!\n")
        return 1
    else:
        print(f"Wrong! The correct answer was {correct_answer}.\n")
        return 0

def main():
    """Main function to run the quiz."""
    print("Welcome to the Simple Quiz!")
    print("Answer the following questions:\n")
    
    score = 0
    total_questions = 5
    
    # Question 1
    question1 = "What is the capital of France?"
    options1 = ["London", "Berlin", "Paris", "Madrid"]
    score += ask_question(question1, options1, 3)
    
    # Question 2
    question2 = "Which planet is known as the Red Planet?"
    options2 = ["Venus", "Mars", "Jupiter", "Saturn"]
    score += ask_question(question2, options2, 2)
    
    # Question 3
    question3 = "What is 10 + 15?"
    options3 = ["20", "25", "30", "35"]
    score += ask_question(question3, options3, 2)
    
    # Question 4
    question4 = "Which programming language are we learning?"
    options4 = ["Java", "C++", "Python", "JavaScript"]
    score += ask_question(question4, options4, 3)
    
    # Question 5
    question5 = "How many days are in a week?"
    options5 = ["5", "6", "7", "8"]
    score += ask_question(question5, options5, 3)
    
    # Display final score
    print(f"Quiz completed! Your score: {score}/{total_questions}")
    
    # Give feedback based on score
    if score == total_questions:
        print("Excellent! You got all questions right!")
    elif score >= total_questions * 0.7:
        print("Good job! You did well!")
    elif score >= total_questions * 0.5:
        print("Not bad! Keep learning!")
    else:
        print("Keep practicing! You'll get better!")

if __name__ == "__main__":
    main()