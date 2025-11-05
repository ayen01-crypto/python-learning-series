"""
Lesson 06: Object-Oriented Programming (OOP)
Comprehensive Examples
"""

# ============================================
# 1. Basic Class Definition
# ============================================

print("=== BASIC CLASS ===\n")

class Dog:
    """A simple Dog class."""
    
    def __init__(self, name, age):
        """Constructor - initializes the object."""
        self.name = name
        self.age = age
    
    def bark(self):
        """Method to make the dog bark."""
        return f"{self.name} says Woof!"
    
    def get_info(self):
        """Return dog information."""
        return f"{self.name} is {self.age} years old"

# Creating objects
dog1 = Dog("Buddy", 3)
dog2 = Dog("Max", 5)

print(dog1.bark())
print(dog2.get_info())


# ============================================
# 2. Class Variables vs Instance Variables
# ============================================

print("\n" + "="*60)
print("=== CLASS VS INSTANCE VARIABLES ===\n")

class Cat:
    """Cat class demonstrating class and instance variables."""
    
    # Class variable (shared by all instances)
    species = "Felis catus"
    population = 0
    
    def __init__(self, name, color):
        # Instance variables (unique to each object)
        self.name = name
        self.color = color
        Cat.population += 1  # Increment class variable
    
    def meow(self):
        return f"{self.name} says Meow!"

cat1 = Cat("Whiskers", "orange")
cat2 = Cat("Shadow", "black")

print(f"Cat 1: {cat1.name}, {cat1.color}")
print(f"Cat 2: {cat2.name}, {cat2.color}")
print(f"Species: {Cat.species}")  # Same for all
print(f"Total cats: {Cat.population}")


# ============================================
# 3. Encapsulation - Private Attributes
# ============================================

print("\n" + "="*60)
print("=== ENCAPSULATION ===\n")

class BankAccount:
    """Bank account with private balance."""
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # Private attribute
    
    def deposit(self, amount):
        """Deposit money."""
        if amount > 0:
            self.__balance += amount
            return f"Deposited ${amount}. New balance: ${self.__balance}"
        return "Invalid amount"
    
    def withdraw(self, amount):
        """Withdraw money."""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.__balance}"
        return "Insufficient funds or invalid amount"
    
    def get_balance(self):
        """Get current balance."""
        return self.__balance

account = BankAccount("Alice", 1000)
print(account.deposit(500))
print(account.withdraw(200))
print(f"Current balance: ${account.get_balance()}")


# ============================================
# 4. Properties and Decorators
# ============================================

print("\n" + "="*60)
print("=== PROPERTIES ===\n")

class Person:
    """Person class with properties."""
    
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    @property
    def name(self):
        """Name getter."""
        return self._name
    
    @name.setter
    def name(self, value):
        """Name setter with validation."""
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string")
    
    @property
    def age(self):
        """Age getter."""
        return self._age
    
    @age.setter
    def age(self, value):
        """Age setter with validation."""
        if isinstance(value, int) and 0 <= value <= 150:
            self._age = value
        else:
            raise ValueError("Age must be between 0 and 150")
    
    def __str__(self):
        """String representation."""
        return f"Person(name='{self.name}', age={self.age})"

person = Person("Bob", 30)
print(person)
person.age = 31
print(f"Updated: {person}")


# ============================================
# 5. Inheritance
# ============================================

print("\n" + "="*60)
print("=== INHERITANCE ===\n")

class Animal:
    """Base class for all animals."""
    
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound
    
    def make_sound(self):
        """Make the animal's sound."""
        return f"{self.name} says {self.sound}"
    
    def move(self):
        """Generic move method."""
        return f"{self.name} is moving"

class Bird(Animal):
    """Bird class inheriting from Animal."""
    
    def __init__(self, name, sound, can_fly):
        super().__init__(name, sound)
        self.can_fly = can_fly
    
    def move(self):
        """Override move method."""
        if self.can_fly:
            return f"{self.name} is flying"
        return f"{self.name} is walking"

class Fish(Animal):
    """Fish class inheriting from Animal."""
    
    def __init__(self, name, sound="blub"):
        super().__init__(name, sound)
    
    def move(self):
        """Override move method."""
        return f"{self.name} is swimming"

parrot = Bird("Polly", "Squawk!", True)
penguin = Bird("Pingu", "Honk!", False)
goldfish = Fish("Goldie")

print(parrot.make_sound())
print(parrot.move())
print(penguin.move())
print(goldfish.move())


# ============================================
# 6. Multiple Inheritance
# ============================================

print("\n" + "="*60)
print("=== MULTIPLE INHERITANCE ===\n")

class Flyable:
    """Mixin for flying ability."""
    name: str
    
    def fly(self):
        return f"{self.name} is flying"

class Swimmable:
    """Mixin for swimming ability."""
    name: str
    
    def swim(self):
        return f"{self.name} is swimming"

class Duck(Animal, Flyable, Swimmable):
    """Duck can fly and swim."""
    
    def __init__(self, name):
        super().__init__(name, "Quack!")

duck = Duck("Donald")
print(duck.make_sound())
print(duck.fly())
print(duck.swim())


# ============================================
# 7. Special Methods (Magic/Dunder Methods)
# ============================================

print("\n" + "="*60)
print("=== SPECIAL METHODS ===\n")

class Vector:
    """2D Vector class with operator overloading."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        """String representation for users."""
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        """String representation for developers."""
        return f"Vector(x={self.x}, y={self.y})"
    
    def __add__(self, other):
        """Add two vectors."""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Subtract two vectors."""
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """Multiply vector by scalar."""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __eq__(self, other):
        """Check equality."""
        return self.x == other.x and self.y == other.y
    
    def __len__(self):
        """Return magnitude (rounded)."""
        return int((self.x**2 + self.y**2) ** 0.5)

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1: {v1}")
print(f"v2: {v2}")
print(f"v1 + v2: {v1 + v2}")
print(f"v1 - v2: {v1 - v2}")
print(f"v1 * 2: {v1 * 2}")
print(f"v1 == v2: {v1 == v2}")
print(f"len(v1): {len(v1)}")


# ============================================
# 8. Abstract Base Classes
# ============================================

print("\n" + "="*60)
print("=== ABSTRACT BASE CLASSES ===\n")

from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class for shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate area - must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate perimeter - must be implemented by subclasses."""
        pass

class Rectangle(Shape):
    """Rectangle implementation."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    """Circle implementation."""
    
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

rect = Rectangle(5, 10)
circle = Circle(7)

print(f"Rectangle: Area={rect.area()}, Perimeter={rect.perimeter()}")
print(f"Circle: Area={circle.area():.2f}, Perimeter={circle.perimeter():.2f}")


# ============================================
# 9. Class Methods and Static Methods
# ============================================

print("\n" + "="*60)
print("=== CLASS & STATIC METHODS ===\n")

class Employee:
    """Employee class with class and static methods."""
    
    raise_amount = 1.04  # Class variable
    num_employees = 0
    
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        Employee.num_employees += 1
    
    @property
    def email(self):
        """Generate email automatically."""
        return f"{self.first.lower()}.{self.last.lower()}@company.com"
    
    @property
    def fullname(self):
        """Get full name."""
        return f"{self.first} {self.last}"
    
    def apply_raise(self):
        """Apply raise to salary."""
        self.pay = int(self.pay * self.raise_amount)
    
    @classmethod
    def set_raise_amount(cls, amount):
        """Set raise amount for all employees."""
        cls.raise_amount = amount
    
    @classmethod
    def from_string(cls, emp_str):
        """Alternative constructor from string."""
        first, last, pay = emp_str.split('-')
        return cls(first, last, int(pay))
    
    @staticmethod
    def is_workday(day):
        """Check if it's a workday (0=Monday, 6=Sunday)."""
        return day not in (5, 6)
    
    def __str__(self):
        return f"{self.fullname} - ${self.pay}"

emp1 = Employee("John", "Doe", 50000)
emp2 = Employee.from_string("Jane-Smith-60000")

print(emp1)
print(f"Email: {emp1.email}")

emp1.apply_raise()
print(f"After raise: {emp1}")

print(f"\nTotal employees: {Employee.num_employees}")
print(f"Is Monday a workday? {Employee.is_workday(0)}")


# ============================================
# 10. Polymorphism
# ============================================

print("\n" + "="*60)
print("=== POLYMORPHISM ===\n")

def describe_animal(animal):
    """Function that works with any Animal subclass."""
    print(f"Name: {animal.name}")
    print(f"Sound: {animal.make_sound()}")
    print(f"Movement: {animal.move()}")
    print()

# Polymorphism in action - same function, different behaviors
animals = [
    Bird("Eagle", "Screech!", True),
    Fish("Salmon"),
    Duck("Daffy")
]

for animal in animals:
    describe_animal(animal)


# ============================================
# Practice Exercise
# ============================================

print("="*60)
print("🎯 PRACTICE EXERCISE")
print("="*60)
print("""
Create these classes:

1. Vehicle base class with Car, Truck, Motorcycle subclasses
2. Shopping cart system with Product and Cart classes
3. Game character hierarchy with different abilities
4. Temperature class with Celsius/Fahrenheit conversion
5. Fraction class with arithmetic operations
""")
