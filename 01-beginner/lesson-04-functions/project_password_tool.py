"""
Mini Project: Password Generator & Validator

A comprehensive tool for generating secure passwords and validating password strength.
Demonstrates functions, parameters, return values, and string manipulation.
"""

import random
import string


# ============================================
# Password Generation Functions
# ============================================

def generate_password(length=12, use_uppercase=True, use_lowercase=True, 
                     use_digits=True, use_symbols=True):
    """
    Generate a random password with specified criteria.
    
    Args:
        length (int): Length of the password (default: 12)
        use_uppercase (bool): Include uppercase letters
        use_lowercase (bool): Include lowercase letters
        use_digits (bool): Include digits
        use_symbols (bool): Include special symbols
    
    Returns:
        str: Generated password
    """
    # Build character pool
    char_pool = ""
    
    if use_uppercase:
        char_pool += string.ascii_uppercase
    if use_lowercase:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation
    
    # Ensure at least one character type is selected
    if not char_pool:
        char_pool = string.ascii_letters + string.digits
    
    # Generate password
    password = ''.join(random.choice(char_pool) for _ in range(length))
    
    return password


def generate_memorable_password(num_words=4, separator="-", add_numbers=True):
    """
    Generate a memorable password using words.
    
    Args:
        num_words (int): Number of words to use
        separator (str): Character to separate words
        add_numbers (bool): Add numbers at the end
    
    Returns:
        str: Generated memorable password
    """
    word_list = [
        "dragon", "phoenix", "tiger", "eagle", "wolf",
        "ocean", "mountain", "forest", "river", "sky",
        "thunder", "lightning", "storm", "wind", "fire",
        "crystal", "diamond", "silver", "golden", "ruby"
    ]
    
    selected_words = random.sample(word_list, min(num_words, len(word_list)))
    
    # Capitalize first letter of each word
    selected_words = [word.capitalize() for word in selected_words]
    
    # Join with separator
    password = separator.join(selected_words)
    
    # Add numbers if requested
    if add_numbers:
        password += str(random.randint(10, 99))
    
    return password


# ============================================
# Password Validation Functions
# ============================================

def check_length(password, min_length=8):
    """Check if password meets minimum length requirement."""
    return len(password) >= min_length


def has_uppercase(password):
    """Check if password contains uppercase letters."""
    return any(char.isupper() for char in password)


def has_lowercase(password):
    """Check if password contains lowercase letters."""
    return any(char.islower() for char in password)


def has_digit(password):
    """Check if password contains digits."""
    return any(char.isdigit() for char in password)


def has_symbol(password):
    """Check if password contains special symbols."""
    return any(char in string.punctuation for char in password)


def calculate_password_strength(password):
    """
    Calculate password strength score.
    
    Args:
        password (str): Password to evaluate
    
    Returns:
        tuple: (score, strength_level, feedback)
    """
    score = 0
    feedback = []
    
    # Length check
    if check_length(password, 8):
        score += 20
    else:
        feedback.append("❌ Too short (minimum 8 characters)")
    
    if len(password) >= 12:
        score += 10
        feedback.append("✅ Good length")
    
    # Character variety
    if has_uppercase(password):
        score += 20
        feedback.append("✅ Has uppercase letters")
    else:
        feedback.append("❌ Missing uppercase letters")
    
    if has_lowercase(password):
        score += 20
        feedback.append("✅ Has lowercase letters")
    else:
        feedback.append("❌ Missing lowercase letters")
    
    if has_digit(password):
        score += 20
        feedback.append("✅ Has numbers")
    else:
        feedback.append("❌ Missing numbers")
    
    if has_symbol(password):
        score += 20
        feedback.append("✅ Has special symbols")
    else:
        feedback.append("⚠️  Consider adding special symbols")
    
    # Extra points for very long passwords
    if len(password) >= 16:
        score += 10
        feedback.append("✅ Excellent length!")
    
    # Determine strength level
    if score >= 90:
        strength = "🟢 VERY STRONG"
    elif score >= 70:
        strength = "🔵 STRONG"
    elif score >= 50:
        strength = "🟡 MODERATE"
    elif score >= 30:
        strength = "🟠 WEAK"
    else:
        strength = "🔴 VERY WEAK"
    
    return score, strength, feedback


# ============================================
# User Interface Functions
# ============================================

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")


def display_password(password, show_strength=True):
    """Display password with optional strength analysis."""
    print(f"\n🔑 Generated Password: {password}")
    print(f"   Length: {len(password)} characters")
    
    if show_strength:
        score, strength, feedback = calculate_password_strength(password)
        print(f"\n   Strength: {strength} ({score}/100)")


def get_int_input(prompt, default, min_val=1, max_val=100):
    """Get integer input from user with validation."""
    while True:
        try:
            user_input = input(f"{prompt} (default: {default}): ")
            if user_input == "":
                return default
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            print(f"❌ Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("❌ Please enter a valid number")


def get_yes_no(prompt, default=True):
    """Get yes/no input from user."""
    default_str = "Y/n" if default else "y/N"
    while True:
        response = input(f"{prompt} ({default_str}): ").lower()
        if response == "":
            return default
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print("❌ Please enter yes or no")


# ============================================
# Main Application
# ============================================

def password_generator_menu():
    """Interactive password generator."""
    print_header("🔐 PASSWORD GENERATOR")
    
    print("Choose password type:")
    print("1. Random password (secure)")
    print("2. Memorable password (easier to remember)")
    
    while True:
        choice = input("\nYour choice (1 or 2): ")
        if choice in ['1', '2']:
            break
        print("❌ Please enter 1 or 2")
    
    if choice == '1':
        # Random password options
        print("\n📋 Customize your password:\n")
        length = get_int_input("Password length", 12, 8, 64)
        use_uppercase = get_yes_no("Include uppercase letters?")
        use_lowercase = get_yes_no("Include lowercase letters?")
        use_digits = get_yes_no("Include digits?")
        use_symbols = get_yes_no("Include special symbols?")
        
        password = generate_password(length, use_uppercase, use_lowercase, 
                                    use_digits, use_symbols)
    
    else:
        # Memorable password options
        print("\n📋 Customize your password:\n")
        num_words = get_int_input("Number of words", 4, 2, 6)
        separator = input("Word separator (default: -): ") or "-"
        add_numbers = get_yes_no("Add numbers at the end?")
        
        password = generate_memorable_password(num_words, separator, add_numbers)
    
    display_password(password)
    
    return password


def password_validator_menu():
    """Interactive password validator."""
    print_header("✅ PASSWORD VALIDATOR")
    
    password = input("Enter password to validate: ")
    
    score, strength, feedback = calculate_password_strength(password)
    
    print(f"\n📊 Password Analysis:")
    print(f"   Password: {'*' * len(password)} ({len(password)} characters)")
    print(f"   Strength: {strength}")
    print(f"   Score: {score}/100")
    
    print(f"\n📋 Detailed Feedback:")
    for item in feedback:
        print(f"   {item}")
    
    # Suggestions
    print(f"\n💡 Suggestions:")
    if score < 70:
        print("   • Use a mix of uppercase, lowercase, numbers, and symbols")
        print("   • Make it at least 12 characters long")
        print("   • Avoid common words and patterns")


def main_menu():
    """Main application menu."""
    print("=" * 70)
    print("🔐  PASSWORD TOOL  🔐".center(70))
    print("=" * 70)
    print("\nYour all-in-one password security tool!")
    
    while True:
        print("\n" + "-" * 70)
        print("\n📌 MAIN MENU:")
        print("1. Generate Password")
        print("2. Validate Password")
        print("3. Generate Multiple Passwords")
        print("4. Exit")
        
        choice = input("\nYour choice: ")
        
        if choice == '1':
            password = password_generator_menu()
            
            # Ask to validate
            if get_yes_no("\nWould you like to validate this password?", False):
                score, strength, feedback = calculate_password_strength(password)
                print(f"\nStrength: {strength} ({score}/100)")
        
        elif choice == '2':
            password_validator_menu()
        
        elif choice == '3':
            print_header("🔐 MULTIPLE PASSWORD GENERATOR")
            count = get_int_input("How many passwords?", 5, 1, 20)
            length = get_int_input("Password length", 12, 8, 32)
            
            print(f"\n✨ Generated {count} passwords:\n")
            for i in range(count):
                password = generate_password(length)
                print(f"{i+1}. {password}")
        
        elif choice == '4':
            print("\n👋 Thank you for using Password Tool!")
            print("Stay secure! 🔒\n")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")


# ============================================
# Run the application
# ============================================

if __name__ == "__main__":
    main_menu()
