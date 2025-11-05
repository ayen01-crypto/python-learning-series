"""
Personal Information Program
This program demonstrates the use of variables to store personal information.
"""

def main():
    """Main function to collect and display personal information."""
    print("Personal Information Form")
    print("-" * 25)
    
    # Collect personal information using variables
    name = input("Enter your full name: ")
    age = int(input("Enter your age: "))
    city = input("Enter your city: ")
    country = input("Enter your country: ")
    occupation = input("Enter your occupation: ")
    hobby = input("Enter your favorite hobby: ")
    
    # Display the collected information
    print("\nYour Personal Information:")
    print("-" * 25)
    print(f"Name: {name}")
    print(f"Age: {age} years old")
    print(f"Location: {city}, {country}")
    print(f"Occupation: {occupation}")
    print(f"Favorite Hobby: {hobby}")
    
    # Calculate and display additional information
    birth_year = 2025 - age  # Assuming current year is 2025
    print(f"Estimated Birth Year: {birth_year}")
    
    # Demonstrate variable reassignment
    print(f"\nUpdating your information...")
    new_city = input("Did you move to a new city? Enter new city (or press Enter to skip): ")
    if new_city:
        city = new_city
        print(f"Updated city: {city}")
    
    # Demonstrate string concatenation
    full_location = city + ", " + country
    print(f"Full location: {full_location}")

if __name__ == "__main__":
    main()