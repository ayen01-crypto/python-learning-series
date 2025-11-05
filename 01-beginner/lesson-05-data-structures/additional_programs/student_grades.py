"""
Student Grades Program
This program demonstrates the use of lists, dictionaries, and tuples for managing student grades.
"""

def add_student(gradebook, student_name):
    """Add a new student to the gradebook."""
    gradebook[student_name] = []

def add_grade(gradebook, student_name, grade):
    """Add a grade for a student."""
    if student_name in gradebook:
        if 0 <= grade <= 100:
            gradebook[student_name].append(grade)
            return True
        else:
            print("Grade must be between 0 and 100.")
            return False
    else:
        print(f"Student {student_name} not found in gradebook.")
        return False

def remove_student(gradebook, student_name):
    """Remove a student from the gradebook."""
    if student_name in gradebook:
        del gradebook[student_name]
        return True
    else:
        return False

def calculate_average(grades):
    """Calculate the average of a list of grades."""
    if not grades:
        return 0
    return sum(grades) / len(grades)

def get_letter_grade(average):
    """Convert numeric average to letter grade."""
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    elif average >= 60:
        return 'D'
    else:
        return 'F'

def get_student_info(gradebook, student_name):
    """Get information about a student's grades."""
    if student_name in gradebook:
        grades = gradebook[student_name]
        if grades:
            average = calculate_average(grades)
            letter_grade = get_letter_grade(average)
            return {
                'grades': grades,
                'average': average,
                'letter_grade': letter_grade
            }
        else:
            return {
                'grades': [],
                'average': 0,
                'letter_grade': 'N/A'
            }
    else:
        return None

def list_all_students(gradebook):
    """List all students and their grades."""
    if not gradebook:
        print("Gradebook is empty.")
        return
    
    print("Class Grade Report:")
    print("=" * 40)
    for student_name, grades in gradebook.items():
        info = get_student_info(gradebook, student_name)
        print(f"Student: {student_name}")
        if info and info['grades']:
            print(f"  Grades: {info['grades']}")
            print(f"  Average: {info['average']:.2f}")
            print(f"  Letter Grade: {info['letter_grade']}")
        else:
            print("  No grades recorded.")
        print()

def find_highest_average(gradebook):
    """Find the student with the highest average."""
    highest_avg = -1
    top_student = None
    
    for student_name in gradebook:
        info = get_student_info(gradebook, student_name)
        if info and info['average'] > highest_avg:
            highest_avg = info['average']
            top_student = student_name
    
    return top_student, highest_avg

def find_lowest_average(gradebook):
    """Find the student with the lowest average."""
    if not gradebook:
        return None, 0
    
    lowest_avg = 101
    bottom_student = None
    
    for student_name in gradebook:
        info = get_student_info(gradebook, student_name)
        if info and info['average'] < lowest_avg:
            lowest_avg = info['average']
            bottom_student = student_name
    
    return bottom_student, lowest_avg

def main():
    """Main function to run the student grades program."""
    print("Student Grades Manager")
    print("=" * 25)
    
    # Initialize gradebook
    gradebook = {}
    
    # Add some initial students
    students = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    for student in students:
        add_student(gradebook, student)
    
    # Add some initial grades
    add_grade(gradebook, "Alice", 85)
    add_grade(gradebook, "Alice", 92)
    add_grade(gradebook, "Alice", 78)
    
    add_grade(gradebook, "Bob", 76)
    add_grade(gradebook, "Bob", 81)
    add_grade(gradebook, "Bob", 88)
    
    add_grade(gradebook, "Charlie", 95)
    add_grade(gradebook, "Charlie", 89)
    add_grade(gradebook, "Charlie", 91)
    
    add_grade(gradebook, "Diana", 68)
    add_grade(gradebook, "Diana", 74)
    add_grade(gradebook, "Diana", 72)
    
    add_grade(gradebook, "Eve", 88)
    add_grade(gradebook, "Eve", 85)
    add_grade(gradebook, "Eve", 90)
    
    print("Initial gradebook created.")
    list_all_students(gradebook)
    
    # Demonstrate gradebook operations
    print("Performing gradebook operations...")
    
    # Add a new student
    add_student(gradebook, "Frank")
    add_grade(gradebook, "Frank", 82)
    add_grade(gradebook, "Frank", 79)
    print("Added Frank to gradebook with initial grades.")
    
    # Add grades for existing students
    add_grade(gradebook, "Alice", 88)
    print("Added a new grade for Alice.")
    
    # Display updated gradebook
    print("\nUpdated Gradebook:")
    list_all_students(gradebook)
    
    # Find top and bottom students
    top_student, top_avg = find_highest_average(gradebook)
    bottom_student, bottom_avg = find_lowest_average(gradebook)
    
    print(f"Highest Average: {top_student} with {top_avg:.2f}")
    print(f"Lowest Average: {bottom_student} with {bottom_avg:.2f}")
    
    # Interactive gradebook management
    print("\nInteractive Gradebook Management:")
    while True:
        print("\nChoose an operation:")
        print("1. Add student")
        print("2. Remove student")
        print("3. Add grade")
        print("4. View student grades")
        print("5. List all students")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ")
        
        if choice == '6':
            break
            
        if choice == '1':
            student_name = input("Enter student name: ")
            add_student(gradebook, student_name)
            print(f"Added {student_name} to gradebook.")
        elif choice == '2':
            student_name = input("Enter student name to remove: ")
            if remove_student(gradebook, student_name):
                print(f"Removed {student_name} from gradebook.")
            else:
                print(f"Student {student_name} not found in gradebook.")
        elif choice == '3':
            student_name = input("Enter student name: ")
            try:
                grade = float(input("Enter grade (0-100): "))
                if add_grade(gradebook, student_name, grade):
                    print(f"Added grade {grade} for {student_name}.")
                else:
                    print("Failed to add grade.")
            except ValueError:
                print("Invalid input. Please enter a valid number for grade.")
        elif choice == '4':
            student_name = input("Enter student name: ")
            info = get_student_info(gradebook, student_name)
            if info:
                print(f"\n{student_name}:")
                if info['grades']:
                    print(f"  Grades: {info['grades']}")
                    print(f"  Average: {info['average']:.2f}")
                    print(f"  Letter Grade: {info['letter_grade']}")
                else:
                    print("  No grades recorded.")
            else:
                print(f"Student {student_name} not found in gradebook.")
        elif choice == '5':
            list_all_students(gradebook)
        else:
            print("Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()