"""
Math Operations Program
This program demonstrates various mathematical functions.
"""

def add(x, y):
    """Add two numbers."""
    return x + y

def subtract(x, y):
    """Subtract two numbers."""
    return x - y

def multiply(x, y):
    """Multiply two numbers."""
    return x * y

def divide(x, y):
    """Divide two numbers."""
    if y != 0:
        return x / y
    else:
        return "Error: Division by zero"

def power(base, exponent):
    """Calculate base raised to the power of exponent."""
    return base ** exponent

def square_root(x):
    """Calculate the square root of a number."""
    if x >= 0:
        return x ** 0.5
    else:
        return "Error: Cannot calculate square root of negative number"

def factorial(n):
    """Calculate the factorial of a number."""
    if n < 0:
        return "Error: Factorial not defined for negative numbers"
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

def is_even(number):
    """Check if a number is even."""
    return number % 2 == 0

def is_odd(number):
    """Check if a number is odd."""
    return number % 2 != 0

def absolute_value(x):
    """Calculate the absolute value of a number."""
    if x < 0:
        return -x
    else:
        return x

def main():
    """Main function to demonstrate math operations."""
    print("Math Operations Program")
    print("=" * 25)
    
    # Demonstrate basic operations
    a = 10
    b = 3
    
    print(f"Numbers: a = {a}, b = {b}")
    print(f"Addition: {a} + {b} = {add(a, b)}")
    print(f"Subtraction: {a} - {b} = {subtract(a, b)}")
    print(f"Multiplication: {a} * {b} = {multiply(a, b)}")
    print(f"Division: {a} / {b} = {divide(a, b)}")
    print(f"Power: {a} ^ {b} = {power(a, b)}")
    
    # Demonstrate other operations
    c = 16
    d = -5
    e = 5
    
    print(f"\nSquare root of {c} = {square_root(c)}")
    print(f"Factorial of {e} = {factorial(e)}")
    print(f"Is {a} even? {is_even(a)}")
    print(f"Is {b} odd? {is_odd(b)}")
    print(f"Absolute value of {d} = {absolute_value(d)}")
    
    # Interactive section
    print("\nInteractive Calculator:")
    while True:
        print("\nChoose an operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Power")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ")
        
        if choice == '6':
            break
            
        if choice in ('1', '2', '3', '4', '5'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                
                if choice == '1':
                    print(f"Result: {add(num1, num2)}")
                elif choice == '2':
                    print(f"Result: {subtract(num1, num2)}")
                elif choice == '3':
                    print(f"Result: {multiply(num1, num2)}")
                elif choice == '4':
                    result = divide(num1, num2)
                    print(f"Result: {result}")
                elif choice == '5':
                    print(f"Result: {power(num1, num2)}")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
        else:
            print("Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()