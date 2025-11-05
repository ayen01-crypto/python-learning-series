#!/usr/bin/env python3
"""
Robust Calculator
A calculator program with comprehensive error handling.
"""

import math
import re


class CalculatorError(Exception):
    """Custom exception for calculator-specific errors."""
    pass


class Calculator:
    """A robust calculator with comprehensive error handling."""
    
    def __init__(self):
        """Initialize calculator with history tracking."""
        self.history = []
    
    def add(self, a, b):
        """Add two numbers."""
        try:
            result = float(a) + float(b)
            self._record_operation(f"{a} + {b} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"Invalid input for addition: {e}")
    
    def subtract(self, a, b):
        """Subtract second number from first."""
        try:
            result = float(a) - float(b)
            self._record_operation(f"{a} - {b} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"Invalid input for subtraction: {e}")
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        try:
            result = float(a) * float(b)
            self._record_operation(f"{a} × {b} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"Invalid input for multiplication: {e}")
    
    def divide(self, a, b):
        """Divide first number by second."""
        try:
            divisor = float(b)
            if divisor == 0:
                raise CalculatorError("Division by zero is not allowed")
            result = float(a) / divisor
            self._record_operation(f"{a} ÷ {b} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"Invalid input for division: {e}")
    
    def power(self, base, exponent):
        """Raise base to the power of exponent."""
        try:
            result = pow(float(base), float(exponent))
            self._record_operation(f"{base} ^ {exponent} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"Invalid input for power operation: {e}")
        except OverflowError:
            raise CalculatorError("Result too large to calculate")
    
    def sqrt(self, x):
        """Calculate square root."""
        try:
            num = float(x)
            if num < 0:
                raise CalculatorError("Cannot calculate square root of negative number")
            result = math.sqrt(num)
            self._record_operation(f"√{x} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"Invalid input for square root: {e}")
    
    def evaluate_expression(self, expression):
        """
        Evaluate a mathematical expression string.
        
        Args:
            expression (str): Mathematical expression
            
        Returns:
            float: Result of evaluation
        """
        # Validate expression
        if not re.match(r'^[0-9+\-*/().\s]+$', expression):
            raise CalculatorError("Invalid characters in expression")
        
        try:
            # Replace ^ with ** for Python power operator
            expression = expression.replace('^', '**')
            result = eval(expression)
            self._record_operation(f"{expression} = {result}")
            return result
        except ZeroDivisionError:
            raise CalculatorError("Division by zero in expression")
        except SyntaxError:
            raise CalculatorError("Invalid expression syntax")
        except Exception as e:
            raise CalculatorError(f"Error evaluating expression: {e}")
    
    def _record_operation(self, operation):
        """Record operation in history."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{timestamp}] {operation}")
    
    def show_history(self):
        """Display calculation history."""
        if not self.history:
            print("No calculations performed yet.")
            return
        
        print("\n📜 Calculation History:")
        print("-" * 40)
        for entry in self.history:
            print(entry)
    
    def clear_history(self):
        """Clear calculation history."""
        self.history.clear()
        print("History cleared.")


def get_number_input(prompt):
    """Get a valid number from user input."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                raise CalculatorError("Input cannot be empty")
            float(value)  # Test if it's a valid number
            return value
        except ValueError:
            print("❌ Please enter a valid number.")
        except CalculatorError as e:
            print(f"❌ {e}")


def main():
    """Main calculator program."""
    calc = Calculator()
    
    print("🧮 Robust Calculator with Error Handling")
    print("This program demonstrates comprehensive error handling in Python.")
    
    while True:
        print("\n" + "=" * 40)
        print("🧮 CALCULATOR MENU")
        print("=" * 40)
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (×)")
        print("4. Division (÷)")
        print("5. Power (^)")
        print("6. Square Root (√)")
        print("7. Expression Evaluation")
        print("8. Show History")
        print("9. Clear History")
        print("10. Exit")
        
        choice = input("\nEnter your choice (1-10): ").strip()
        
        try:
            if choice == '1':
                a = get_number_input("Enter first number: ")
                b = get_number_input("Enter second number: ")
                result = calc.add(a, b)
                print(f"✅ Result: {a} + {b} = {result}")
            
            elif choice == '2':
                a = get_number_input("Enter first number: ")
                b = get_number_input("Enter second number: ")
                result = calc.subtract(a, b)
                print(f"✅ Result: {a} - {b} = {result}")
            
            elif choice == '3':
                a = get_number_input("Enter first number: ")
                b = get_number_input("Enter second number: ")
                result = calc.multiply(a, b)
                print(f"✅ Result: {a} × {b} = {result}")
            
            elif choice == '4':
                a = get_number_input("Enter dividend: ")
                b = get_number_input("Enter divisor: ")
                result = calc.divide(a, b)
                print(f"✅ Result: {a} ÷ {b} = {result}")
            
            elif choice == '5':
                base = get_number_input("Enter base: ")
                exponent = get_number_input("Enter exponent: ")
                result = calc.power(base, exponent)
                print(f"✅ Result: {base} ^ {exponent} = {result}")
            
            elif choice == '6':
                x = get_number_input("Enter number: ")
                result = calc.sqrt(x)
                print(f"✅ Result: √{x} = {result}")
            
            elif choice == '7':
                expr = input("Enter mathematical expression: ").strip()
                if expr:
                    result = calc.evaluate_expression(expr)
                    print(f"✅ Result: {expr} = {result}")
                else:
                    print("❌ Expression cannot be empty.")
            
            elif choice == '8':
                calc.show_history()
            
            elif choice == '9':
                calc.clear_history()
            
            elif choice == '10':
                print("Thank you for using Robust Calculator!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-10.")
        
        except CalculatorError as e:
            print(f"❌ Calculator Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main()