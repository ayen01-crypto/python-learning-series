"""
Lesson 08: Error Handling & Exceptions
Comprehensive Examples
"""

import logging
import traceback
from typing import Union


# ============================================
# 1. Basic Exception Handling
# ============================================

print("=== BASIC EXCEPTION HANDLING ===\n")

# Simple try/except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("❌ Cannot divide by zero!")

# Multiple exceptions
try:
    value = int("abc")
except ValueError:
    print("❌ Invalid number format!")
except TypeError:
    print("❌ Wrong type!")

# Catch all exceptions
try:
    # This will raise an exception
    undefined_variable
except NameError as e:
    print(f"❌ NameError: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")


# ============================================
# 2. Try/Except/Else/Finally
# ============================================

print("\n" + "="*60)
print("=== TRY/EXCEPT/ELSE/FINALLY ===\n")

def divide_numbers(a: float, b: float) -> Union[float, None]:
    """Divide two numbers with proper error handling."""
    try:
        result = a / b
    except ZeroDivisionError:
        print("❌ Cannot divide by zero!")
        return None
    except TypeError:
        print("❌ Invalid input types!")
        return None
    else:
        print("✅ Division successful!")
        return result
    finally:
        print("🔄 Cleanup completed")

# Test the function
print("Testing divide_numbers:")
print(f"10 / 2 = {divide_numbers(10, 2)}")
print(f"10 / 0 = {divide_numbers(10, 0)}")
print(f"'10' / 2 = {divide_numbers('10', 2)}")


# ============================================
# 3. Raising Exceptions
# ============================================

print("\n" + "="*60)
print("=== RAISING EXCEPTIONS ===\n")

def validate_age(age: int) -> bool:
    """Validate age with custom exceptions."""
    if age < 0:
        raise ValueError("Age cannot be negative!")
    if age > 150:
        raise ValueError("Age seems unrealistic!")
    return True

# Test validation
test_ages = [-5, 25, 200]

for age in test_ages:
    try:
        validate_age(age)
        print(f"✅ Age {age} is valid")
    except ValueError as e:
        print(f"❌ Invalid age {age}: {e}")


# ============================================
# 4. Custom Exceptions
# ============================================

print("\n" + "="*60)
print("=== CUSTOM EXCEPTIONS ===\n")

class BankError(Exception):
    """Base exception for banking operations."""
    pass

class InsufficientFundsError(BankError):
    """Raised when account has insufficient funds."""
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Insufficient funds: ${balance} available, ${amount} requested")

class InvalidAmountError(BankError):
    """Raised when amount is invalid."""
    pass

class Account:
    """Simple bank account with custom exceptions."""
    
    def __init__(self, initial_balance: float = 0):
        self.balance = initial_balance
    
    def deposit(self, amount: float):
        """Deposit money."""
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount: float):
        """Withdraw money."""
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance

# Test custom exceptions
account = Account(100)

operations = [
    ("deposit", 50),
    ("withdraw", 30),
    ("withdraw", 200),  # Should raise InsufficientFundsError
    ("deposit", -10),   # Should raise InvalidAmountError
]

for operation, amount in operations:
    try:
        if operation == "deposit":
            result = account.deposit(amount)
            print(f"✅ Deposited ${amount}. Balance: ${result}")
        elif operation == "withdraw":
            result = account.withdraw(amount)
            print(f"✅ Withdrew ${amount}. Balance: ${result}")
    except InsufficientFundsError as e:
        print(f"❌ {e}")
    except InvalidAmountError as e:
        print(f"❌ {e}")
    except BankError as e:
        print(f"❌ Banking error: {e}")


# ============================================
# 5. Exception Chaining
# ============================================

print("\n" + "="*60)
print("=== EXCEPTION CHAINING ===\n")

def process_data(data):
    """Process data that might raise exceptions."""
    try:
        return int(data) * 2
    except ValueError as e:
        raise TypeError("Data processing failed") from e

try:
    result = process_data("abc")
except TypeError as e:
    print(f"❌ TypeError: {e}")
    print("Caused by:")
    print(f"  {e.__cause__}")


# ============================================
# 6. Logging Exceptions
# ============================================

print("\n" + "="*60)
print("=== LOGGING EXCEPTIONS ===\n")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def risky_operation(value):
    """Operation that might fail."""
    try:
        return 100 / value
    except ZeroDivisionError as e:
        logging.error(f"Division by zero attempted with value: {value}")
        logging.debug("Traceback:", exc_info=True)
        raise

# Test with logging
try:
    risky_operation(0)
except ZeroDivisionError:
    print("❌ Error handled and logged")


# ============================================
# 7. Context Managers for Exception Handling
# ============================================

print("\n" + "="*60)
print("=== CONTEXT MANAGERS ===\n")

class DatabaseConnection:
    """Simulated database connection with context manager."""
    
    def __init__(self, host: str):
        self.host = host
        self.connected = False
    
    def __enter__(self):
        print(f"🔌 Connecting to {self.host}")
        self.connected = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"🔌 Disconnecting from {self.host}")
        self.connected = False
        if exc_type:
            print(f"❌ Exception occurred: {exc_type.__name__}: {exc_val}")
            # Return False to propagate exception
            return False
        return True
    
    def execute_query(self, query: str):
        """Execute a database query."""
        if not self.connected:
            raise Exception("Not connected to database")
        if "error" in query.lower():
            raise Exception("Query execution failed")
        return f"Results for: {query}"

# Using context manager
try:
    with DatabaseConnection("localhost") as db:
        result = db.execute_query("SELECT * FROM users")
        print(f"✅ Query result: {result}")
        
        # This will raise an exception
        db.execute_query("error query")
except Exception as e:
    print(f"❌ Caught exception: {e}")


# ============================================
# 8. Defensive Programming
# ============================================

print("\n" + "="*60)
print("=== DEFENSIVE PROGRAMMING ===\n")

def safe_divide(a, b):
    """Safely divide two numbers with comprehensive error handling."""
    # Input validation
    if not isinstance(a, (int, float)):
        raise TypeError(f"First argument must be a number, got {type(a).__name__}")
    
    if not isinstance(b, (int, float)):
        raise TypeError(f"Second argument must be a number, got {type(b).__name__}")
    
    # Prevent division by zero
    if b == 0:
        raise ValueError("Cannot divide by zero")
    
    # Perform division
    try:
        return a / b
    except Exception as e:
        # Log unexpected errors
        logging.error(f"Unexpected error in division: {e}")
        raise

# Test defensive programming
test_cases = [
    (10, 2),      # Normal case
    (10, 0),      # Division by zero
    ("10", 2),    # Wrong type
    (10, "2"),    # Wrong type
]

for a, b in test_cases:
    try:
        result = safe_divide(a, b)
        print(f"✅ {a} / {b} = {result}")
    except (TypeError, ValueError) as e:
        print(f"❌ {e}")


# ============================================
# 9. Exception Best Practices
# ============================================

print("\n" + "="*60)
print("=== EXCEPTION BEST PRACTICES ===\n")

# 1. Be specific with exceptions
try:
    with open("nonexistent.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("❌ File not found - specific handling")
except PermissionError:
    print("❌ Permission denied - specific handling")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

# 2. Don't catch and ignore exceptions
def bad_example():
    """Example of bad exception handling."""
    try:
        result = 10 / 0
    except:  # Bad: catches everything silently
        pass   # Bad: does nothing

def good_example():
    """Example of good exception handling."""
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        logging.error(f"Division error: {e}")
        raise  # Re-raise if cannot handle

# 3. Use exception handling for control flow when appropriate
def find_user(users, user_id):
    """Find user with proper exception handling."""
    try:
        return users[user_id]
    except KeyError:
        raise ValueError(f"User {user_id} not found")

users = {"alice": {"name": "Alice"}, "bob": {"name": "Bob"}}

try:
    user = find_user(users, "charlie")
except ValueError as e:
    print(f"❌ {e}")


# ============================================
# 10. Performance Considerations
# ============================================

print("\n" + "="*60)
print("=== PERFORMANCE CONSIDERATIONS ===\n")

import time

# Exception handling has overhead - use appropriately
def with_exception_handling(value):
    """Function using exception handling."""
    try:
        return int(value)
    except ValueError:
        return None

def with_validation(value):
    """Function using validation."""
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None

# Test performance difference
test_value = "123"
iterations = 100000

# Test exception handling approach
start = time.time()
for _ in range(iterations):
    result = with_exception_handling(test_value)
end = time.time()
print(f"Exception handling: {end - start:.4f} seconds")

# Test validation approach
start = time.time()
for _ in range(iterations):
    result = with_validation(test_value)
end = time.time()
print(f"Validation approach: {end - start:.4f} seconds")

print("💡 Use validation for expected cases, exceptions for exceptional cases")


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Try these exercises:

1. Create a calculator class with custom exceptions for math errors
2. Build a file processor that handles various file operation errors
3. Implement a retry mechanism with exponential backoff
4. Create a configuration manager with validation and error reporting
5. Design a network client with timeout and connection error handling
""")
