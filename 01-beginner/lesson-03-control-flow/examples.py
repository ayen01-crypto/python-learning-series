"""
Lesson 03: Control Flow (if/else, loops)
Comprehensive Examples
"""

# ============================================
# 1. Basic if Statements
# ============================================

print("=== BASIC IF STATEMENTS ===\n")

age = 18

if age >= 18:
    print("You are an adult.")

# if-else
temperature = 25

if temperature > 30:
    print("It's hot outside!")
else:
    print("The weather is pleasant.")

# if-elif-else
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score}, Grade: {grade}")


# ============================================
# 2. Comparison Operators in Conditions
# ============================================

print("\n" + "="*50)
print("=== COMPARISON OPERATORS ===\n")

x, y = 10, 20

if x < y:
    print(f"{x} is less than {y}")

if x != y:
    print(f"{x} is not equal to {y}")

# Chained comparisons
age = 25
if 18 <= age < 65:
    print(f"Age {age} is in working age range (18-65)")


# ============================================
# 3. Logical Operators (and, or, not)
# ============================================

print("\n" + "="*50)
print("=== LOGICAL OPERATORS ===\n")

username = "admin"
password = "secret123"

if username == "admin" and password == "secret123":
    print("✅ Login successful!")
else:
    print("❌ Invalid credentials")

# OR operator
day = "Saturday"
if day == "Saturday" or day == "Sunday":
    print("It's the weekend! 🎉")

# NOT operator
is_raining = False
if not is_raining:
    print("No umbrella needed!")


# ============================================
# 4. Nested if Statements
# ============================================

print("\n" + "="*50)
print("=== NESTED IF STATEMENTS ===\n")

age = 20
has_license = True

if age >= 18:
    if has_license:
        print("You can drive!")
    else:
        print("You need a license to drive.")
else:
    print("You're too young to drive.")


# ============================================
# 5. Ternary Operator (Conditional Expression)
# ============================================

print("\n" + "="*50)
print("=== TERNARY OPERATOR ===\n")

age = 17
status = "Adult" if age >= 18 else "Minor"
print(f"Age: {age}, Status: {status}")

# Another example
x, y = 5, 10
max_value = x if x > y else y
print(f"Maximum of {x} and {y} is: {max_value}")


# ============================================
# 6. For Loops
# ============================================

print("\n" + "="*50)
print("=== FOR LOOPS ===\n")

# Loop through a list
fruits = ["apple", "banana", "cherry"]
print("Fruits:")
for fruit in fruits:
    print(f"  - {fruit}")

# Loop through a string
print("\nLetters in 'Python':")
for letter in "Python":
    print(letter, end=" ")
print()

# Loop with range
print("\nNumbers 1 to 5:")
for i in range(1, 6):
    print(i, end=" ")
print()

# Range with step
print("\nEven numbers 0 to 10:")
for i in range(0, 11, 2):
    print(i, end=" ")
print()


# ============================================
# 7. While Loops
# ============================================

print("\n" + "="*50)
print("=== WHILE LOOPS ===\n")

# Basic while loop
count = 1
print("Counting to 5:")
while count <= 5:
    print(count, end=" ")
    count += 1
print()

# While with condition
print("\nDoubling until > 100:")
number = 1
while number <= 100:
    print(number, end=" ")
    number *= 2
print()


# ============================================
# 8. Break Statement
# ============================================

print("\n" + "="*50)
print("=== BREAK STATEMENT ===\n")

print("Finding first number divisible by 7:")
for i in range(20, 50):
    if i % 7 == 0:
        print(f"Found it: {i}")
        break
    print(f"Checking {i}... not divisible")


# ============================================
# 9. Continue Statement
# ============================================

print("\n" + "="*50)
print("=== CONTINUE STATEMENT ===\n")

print("Odd numbers from 1 to 10:")
for i in range(1, 11):
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i, end=" ")
print()


# ============================================
# 10. Pass Statement
# ============================================

print("\n" + "="*50)
print("=== PASS STATEMENT ===\n")

# Placeholder for future code
for i in range(5):
    if i == 3:
        pass  # TODO: Add special handling later
    else:
        print(i, end=" ")
print()


# ============================================
# 11. Nested Loops
# ============================================

print("\n" + "="*50)
print("=== NESTED LOOPS ===\n")

# Multiplication table
print("3x3 Multiplication Table:")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i}x{j}={i*j:2}", end="  ")
    print()

# Pattern printing
print("\nTriangle pattern:")
for i in range(1, 6):
    for j in range(i):
        print("*", end="")
    print()


# ============================================
# 12. Loop with else Clause
# ============================================

print("\n" + "="*50)
print("=== LOOP WITH ELSE ===\n")

# The else clause executes if loop completes normally (no break)
print("Searching for number 7 in range 1-5:")
for i in range(1, 6):
    if i == 7:
        print("Found 7!")
        break
else:
    print("Number 7 not found in range")


# ============================================
# 13. enumerate() Function
# ============================================

print("\n" + "="*50)
print("=== ENUMERATE ===\n")

fruits = ["apple", "banana", "cherry"]
print("Fruits with index:")
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Starting index from 1
print("\nStarting from 1:")
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")


# ============================================
# 14. zip() Function
# ============================================

print("\n" + "="*50)
print("=== ZIP ===\n")

names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["New York", "London", "Paris"]

print("Combining multiple lists:")
for name, age, city in zip(names, ages, cities):
    print(f"{name} is {age} years old and lives in {city}")


# ============================================
# 15. Common Patterns
# ============================================

print("\n" + "="*50)
print("=== COMMON PATTERNS ===\n")

# Sum of numbers
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total += num
print(f"Sum of {numbers}: {total}")

# Find maximum
numbers = [45, 23, 67, 12, 89, 34]
max_num = numbers[0]
for num in numbers:
    if num > max_num:
        max_num = num
print(f"Maximum in {numbers}: {max_num}")

# Count occurrences
text = "hello world"
count_l = 0
for char in text:
    if char == 'l':
        count_l += 1
print(f"Letter 'l' appears {count_l} times in '{text}'")


# ============================================
# Practice Exercise
# ============================================

print("\n" + "="*50)
print("🎯 PRACTICE EXERCISE")
print("="*50)
print("""
Try these on your own:

1. FizzBuzz: Print numbers 1-100
   - Print "Fizz" for multiples of 3
   - Print "Buzz" for multiples of 5
   - Print "FizzBuzz" for multiples of both

2. Print a pyramid pattern:
   *
  ***
 *****
*******

3. Check if a number is prime

4. Reverse a string using a loop

5. Find all even numbers in a list
""")
