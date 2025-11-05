"""
Grade Calculator
This program demonstrates control flow with conditionals to calculate letter grades.
"""

def calculate_letter_grade(score):
    """Calculate letter grade based on numeric score."""
    if score >= 80:
        return "A"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "C+"
    elif score >=60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"

def calculate_gpa(grades):
    """Calculate GPA from letter grades."""
    grade_points = {
        "A": 4.4,
        "B+": 4.0,
        "B": 3.6,
        "C+": 3.0,
        "C": 2.5,
        "D": 2.0,
        "F": 0.0
    }
    
    total_points = 0
    for grade in grades:
        total_points += grade_points.get(grade.upper(), 0)
    
    if len(grades) > 0:
        return total_points / len(grades)
    else:
        return 0.0

def main():
    """Main function to calculate grades."""
    print("Grade Calculator")
    print("-" * 15)
    
    # Collect subject names and scores
    subjects = []
    scores = []
    
    while True:
        subject = input("Enter subject name (or 'done' to finish): ")
        if subject.lower() == 'done':
            break
            
        try:
            score = float(input(f"Enter score for {subject}: "))
            if 0 <= score <= 100:
                subjects.append(subject)
                scores.append(score)
            else:
                print("Please enter a score between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Calculate and display grades
    if subjects:
        print("\nGrade Report:")
        print("-" * 30)
        
        letter_grades = []
        for i in range(len(subjects)):
            letter_grade = calculate_letter_grade(scores[i])
            letter_grades.append(letter_grade)
            print(f"{subjects[i]}: {scores[i]:.1f}% - Grade: {letter_grade}")
        
        # Calculate average score
        average_score = sum(scores) / len(scores)
        overall_grade = calculate_letter_grade(average_score)
        gpa = calculate_gpa(letter_grades)
        
        print("\nSummary:")
        print("-" * 15)
        print(f"Average Score: {average_score:.1f}%")
        print(f"Overall Grade: {overall_grade}")
        print(f"GPA: {gpa:.2f}")
        
        # Provide feedback based on performance
        if average_score >= 90:
            print("Excellent work! Keep it up!")
        elif average_score >= 80:
            print("Good job! You're doing well!")
        elif average_score >= 70:
            print("Satisfactory performance. There's room for improvement.")
        elif average_score >= 60:
            print("You passed, but consider studying more.")
        else:
            print("You need to put in more effort to improve your grades.")
    else:
        print("No grades entered.")

if __name__ == "__main__":
    main()