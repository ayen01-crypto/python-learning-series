"""
Mini Project: Student Grade Manager

A comprehensive system to manage student records, calculate statistics,
and generate reports. Demonstrates lists, dictionaries, tuples, and sets.
"""

import statistics
from datetime import datetime


# ============================================
# Student Database (Global)
# ============================================

students_db = {}  # Dictionary of student records
course_list = ["Math", "Science", "English", "History", "Art"]


# ============================================
# Core Functions
# ============================================

def add_student(student_id, name, age, grade_level):
    """
    Add a new student to the database.
    
    Args:
        student_id (str): Unique student identifier
        name (str): Student's full name
        age (int): Student's age
        grade_level (int): Grade level (1-12)
    
    Returns:
        bool: True if successful, False if student already exists
    """
    if student_id in students_db:
        return False
    
    students_db[student_id] = {
        "name": name,
        "age": age,
        "grade_level": grade_level,
        "grades": {course: [] for course in course_list},
        "attendance": [],
        "registration_date": datetime.now().strftime("%Y-%m-%d")
    }
    return True


def add_grade(student_id, course, grade):
    """
    Add a grade for a student in a specific course.
    
    Args:
        student_id (str): Student identifier
        course (str): Course name
        grade (float): Grade value (0-100)
    
    Returns:
        bool: True if successful, False otherwise
    """
    if student_id not in students_db:
        return False
    
    if course not in students_db[student_id]["grades"]:
        students_db[student_id]["grades"][course] = []
    
    students_db[student_id]["grades"][course].append(grade)
    return True


def calculate_average(grades_list):
    """Calculate average from a list of grades."""
    if not grades_list:
        return 0.0
    return sum(grades_list) / len(grades_list)


def get_letter_grade(average):
    """Convert numeric average to letter grade."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def get_student_report(student_id):
    """
    Generate a comprehensive report for a student.
    
    Returns:
        dict: Student report with averages and statistics
    """
    if student_id not in students_db:
        return None
    
    student = students_db[student_id]
    report = {
        "student_id": student_id,
        "name": student["name"],
        "age": student["age"],
        "grade_level": student["grade_level"],
        "course_grades": {},
        "overall_average": 0.0,
        "letter_grade": ""
    }
    
    all_grades = []
    
    for course, grades in student["grades"].items():
        if grades:
            avg = calculate_average(grades)
            report["course_grades"][course] = {
                "grades": grades,
                "average": avg,
                "letter": get_letter_grade(avg)
            }
            all_grades.extend(grades)
    
    if all_grades:
        report["overall_average"] = calculate_average(all_grades)
        report["letter_grade"] = get_letter_grade(report["overall_average"])
    
    return report


def get_class_statistics():
    """Calculate statistics for the entire class."""
    all_averages = []
    
    for student_id in students_db:
        report = get_student_report(student_id)
        if report and report["overall_average"] > 0:
            all_averages.append(report["overall_average"])
    
    if not all_averages:
        return None
    
    return {
        "total_students": len(students_db),
        "class_average": calculate_average(all_averages),
        "highest_average": max(all_averages),
        "lowest_average": min(all_averages),
        "median": statistics.median(all_averages),
        "students_above_80": sum(1 for avg in all_averages if avg >= 80),
        "students_below_60": sum(1 for avg in all_averages if avg < 60)
    }


def get_top_students(n=3):
    """Get top N students by overall average."""
    student_averages = []
    
    for student_id in students_db:
        report = get_student_report(student_id)
        if report and report["overall_average"] > 0:
            student_averages.append((
                report["name"],
                report["overall_average"],
                report["letter_grade"]
            ))
    
    # Sort by average (descending)
    student_averages.sort(key=lambda x: x[1], reverse=True)
    
    return student_averages[:n]


def search_students(query, search_by="name"):
    """
    Search for students by name or ID.
    
    Returns:
        list: List of matching student IDs
    """
    results = []
    query_lower = query.lower()
    
    for student_id, student in students_db.items():
        if search_by == "name":
            if query_lower in student["name"].lower():
                results.append(student_id)
        elif search_by == "id":
            if query_lower in student_id.lower():
                results.append(student_id)
    
    return results


# ============================================
# Display Functions
# ============================================

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")


def display_student_report(student_id):
    """Display detailed student report."""
    report = get_student_report(student_id)
    
    if not report:
        print("❌ Student not found!")
        return
    
    print_header(f"📊 REPORT CARD - {report['name']}")
    
    print(f"Student ID: {report['student_id']}")
    print(f"Age: {report['age']}")
    print(f"Grade Level: {report['grade_level']}")
    print(f"Registration: {students_db[student_id]['registration_date']}")
    
    print("\n" + "-" * 70)
    print(f"{'COURSE':<15} {'GRADES':<30} {'AVERAGE':<10} {'LETTER'}")
    print("-" * 70)
    
    for course, data in report["course_grades"].items():
        grades_str = ", ".join(str(int(g)) for g in data["grades"])
        print(f"{course:<15} {grades_str:<30} {data['average']:>6.1f}    {data['letter']}")
    
    print("-" * 70)
    print(f"{'OVERALL AVERAGE':<45} {report['overall_average']:>6.1f}    {report['letter_grade']}")
    print("=" * 70)


def display_class_statistics():
    """Display class-wide statistics."""
    stats = get_class_statistics()
    
    if not stats:
        print("❌ No student data available!")
        return
    
    print_header("📈 CLASS STATISTICS")
    
    print(f"Total Students: {stats['total_students']}")
    print(f"Class Average: {stats['class_average']:.2f}")
    print(f"Median Score: {stats['median']:.2f}")
    print(f"Highest Average: {stats['highest_average']:.2f}")
    print(f"Lowest Average: {stats['lowest_average']:.2f}")
    print(f"\nStudents with A/B (≥80): {stats['students_above_80']}")
    print(f"Students at risk (<60): {stats['students_below_60']}")


def display_top_students():
    """Display top performing students."""
    print_header("🏆 TOP STUDENTS")
    
    top = get_top_students(5)
    
    if not top:
        print("No data available.")
        return
    
    for i, (name, average, letter) in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        print(f"{medal} {i}. {name:<20} Average: {average:>6.2f} ({letter})")


def list_all_students():
    """List all students in the database."""
    if not students_db:
        print("❌ No students in database!")
        return
    
    print_header("👥 ALL STUDENTS")
    
    print(f"{'ID':<10} {'NAME':<20} {'AGE':<5} {'LEVEL':<7} {'AVG':<8} {'GRADE'}")
    print("-" * 70)
    
    for student_id in sorted(students_db.keys()):
        student = students_db[student_id]
        report = get_student_report(student_id)
        
        if report:
            avg = f"{report['overall_average']:.1f}" if report['overall_average'] > 0 else "N/A"
            grade = report['letter_grade'] if report['letter_grade'] else "N/A"
        else:
            avg = "N/A"
            grade = "N/A"
        
        print(f"{student_id:<10} {student['name']:<20} {student['age']:<5} "
              f"{student['grade_level']:<7} {avg:<8} {grade}")


# ============================================
# User Interface
# ============================================

from typing import TypeVar, Type

T = TypeVar('T')

def get_input(prompt: str, input_type: Type[T] = str, required: bool = True) -> T | None:
    """Get validated input from user."""
    while True:
        try:
            value = input(prompt)
            if not value and required:
                print("❌ This field is required!")
                continue
            if not value and not required:
                return None
            if input_type == str:
                return value  # type: ignore
            return input_type(value)  # type: ignore
        except ValueError:
            print(f"❌ Please enter a valid value")


def add_student_interactive():
    """Interactive student addition."""
    print_header("➕ ADD NEW STUDENT")
    
    student_id = get_input("Student ID: ")
    
    if student_id in students_db:
        print("❌ Student ID already exists!")
        return
    
    name = get_input("Full Name: ")
    age = get_input("Age: ", int)
    grade_level = get_input("Grade Level (1-12): ", int)
    
    if add_student(student_id, name, age, grade_level):
        print(f"✅ Student {name} added successfully!")
    else:
        print("❌ Failed to add student!")


def add_grades_interactive():
    """Interactive grade entry."""
    print_header("📝 ADD GRADES")
    
    student_id = get_input("Student ID: ")
    
    if student_id not in students_db:
        print("❌ Student not found!")
        return
    
    student_name = students_db[student_id]["name"]
    print(f"\nAdding grades for: {student_name}")
    
    print(f"\nAvailable courses: {', '.join(course_list)}")
    course = get_input("Course: ")
    
    if course not in course_list:
        print("❌ Invalid course!")
        return
    
    grade_input = get_input("Grade (0-100): ", float)
    
    if grade_input is not None and isinstance(grade_input, (int, float)) and 0 <= grade_input <= 100:
        grade = float(grade_input)
        if add_grade(student_id, course, grade):
            print(f"✅ Grade {grade} added for {course}!")
        else:
            print("❌ Failed to add grade!")
    else:
        print("❌ Grade must be between 0 and 100!")


def search_interactive():
    """Interactive student search."""
    print_header("🔍 SEARCH STUDENTS")
    
    query = get_input("Search by name: ")
    results = search_students(query, "name")
    
    if results:
        print(f"\n✅ Found {len(results)} student(s):\n")
        for student_id in results:
            student = students_db[student_id]
            print(f"  ID: {student_id} - {student['name']}")
    else:
        print("❌ No students found!")


def load_sample_data():
    """Load sample student data for demonstration."""
    # Add sample students
    sample_students = [
        ("S001", "Alice Johnson", 16, 10),
        ("S002", "Bob Smith", 17, 11),
        ("S003", "Charlie Brown", 16, 10),
        ("S004", "Diana Prince", 15, 9),
        ("S005", "Ethan Hunt", 17, 11)
    ]
    
    for student_id, name, age, grade_level in sample_students:
        add_student(student_id, name, age, grade_level)
    
    # Add sample grades
    import random
    for student_id in students_db:
        for course in course_list:
            for _ in range(3):  # 3 grades per course
                grade = random.randint(70, 100)
                add_grade(student_id, course, grade)
    
    print("✅ Sample data loaded successfully!")


# ============================================
# Main Menu
# ============================================

def main_menu():
    """Main application menu."""
    print("=" * 70)
    print("📚  STUDENT GRADE MANAGER  📚".center(70))
    print("=" * 70)
    
    while True:
        print("\n" + "-" * 70)
        print("\n📌 MAIN MENU:")
        print("1. Add Student")
        print("2. Add Grades")
        print("3. View Student Report")
        print("4. List All Students")
        print("5. Class Statistics")
        print("6. Top Students")
        print("7. Search Students")
        print("8. Load Sample Data")
        print("9. Exit")
        
        choice = input("\nYour choice: ")
        
        if choice == '1':
            add_student_interactive()
        
        elif choice == '2':
            add_grades_interactive()
        
        elif choice == '3':
            student_id = get_input("\nEnter Student ID: ")
            display_student_report(student_id)
        
        elif choice == '4':
            list_all_students()
        
        elif choice == '5':
            display_class_statistics()
        
        elif choice == '6':
            display_top_students()
        
        elif choice == '7':
            search_interactive()
        
        elif choice == '8':
            load_sample_data()
        
        elif choice == '9':
            print("\n👋 Thank you for using Student Grade Manager!")
            print("=" * 70 + "\n")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")


# ============================================
# Run the application
# ============================================

if __name__ == "__main__":
    main_menu()
