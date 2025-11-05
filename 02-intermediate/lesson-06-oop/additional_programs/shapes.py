"""
Shapes Program
This program demonstrates Object-Oriented Programming concepts with geometric shapes.
"""

import math

class Shape:
    """Abstract base class for all shapes."""
    
    def __init__(self, color="white"):
        """Initialize a shape with a color."""
        self.color = color
    
    def area(self):
        """Calculate the area of the shape."""
        raise NotImplementedError("Subclass must implement abstract method")
    
    def perimeter(self):
        """Calculate the perimeter of the shape."""
        raise NotImplementedError("Subclass must implement abstract method")
    
    def display_info(self):
        """Display information about the shape."""
        print(f"Shape: {self.__class__.__name__}")
        print(f"Color: {self.color}")
        print(f"Area: {self.area():.2f}")
        print(f"Perimeter: {self.perimeter():.2f}")


class Rectangle(Shape):
    """A class representing a rectangle."""
    
    def __init__(self, width, height, color="white"):
        """Initialize a rectangle."""
        super().__init__(color)
        self.width = width
        self.height = height
    
    def area(self):
        """Calculate the area of the rectangle."""
        return self.width * self.height
    
    def perimeter(self):
        """Calculate the perimeter of the rectangle."""
        return 2 * (self.width + self.height)
    
    def display_info(self):
        """Display information about the rectangle."""
        super().display_info()
        print(f"Width: {self.width}")
        print(f"Height: {self.height}")


class Circle(Shape):
    """A class representing a circle."""
    
    def __init__(self, radius, color="white"):
        """Initialize a circle."""
        super().__init__(color)
        self.radius = radius
    
    def area(self):
        """Calculate the area of the circle."""
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        """Calculate the perimeter (circumference) of the circle."""
        return 2 * math.pi * self.radius
    
    def display_info(self):
        """Display information about the circle."""
        super().display_info()
        print(f"Radius: {self.radius}")
        print(f"Diameter: {2 * self.radius}")


class Triangle(Shape):
    """A class representing a triangle."""
    
    def __init__(self, side1, side2, side3, color="white"):
        """Initialize a triangle."""
        super().__init__(color)
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
    
    def area(self):
        """Calculate the area of the triangle using Heron's formula."""
        # Semi-perimeter
        s = self.perimeter() / 2
        # Heron's formula
        area = math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))
        return area
    
    def perimeter(self):
        """Calculate the perimeter of the triangle."""
        return self.side1 + self.side2 + self.side3
    
    def display_info(self):
        """Display information about the triangle."""
        super().display_info()
        print(f"Side 1: {self.side1}")
        print(f"Side 2: {self.side2}")
        print(f"Side 3: {self.side3}")


class Square(Rectangle):
    """A class representing a square."""
    
    def __init__(self, side, color="white"):
        """Initialize a square."""
        super().__init__(side, side, color)
        self.side = side
    
    def display_info(self):
        """Display information about the square."""
        super().display_info()
        print(f"Side: {self.side}")


def main():
    """Main function to demonstrate the shapes program."""
    print("Shapes Program")
    print("=" * 15)
    
    # Create different shapes
    rectangle = Rectangle(5, 3, "red")
    circle = Circle(4, "blue")
    triangle = Triangle(3, 4, 5, "green")
    square = Square(6, "yellow")
    
    # Store shapes in a list
    shapes = [rectangle, circle, triangle, square]
    
    # Demonstrate polymorphism
    print("Shape Information:")
    print("=" * 30)
    for shape in shapes:
        shape.display_info()
        print("-" * 20)
    
    # Calculate total area and perimeter
    total_area = sum(shape.area() for shape in shapes)
    total_perimeter = sum(shape.perimeter() for shape in shapes)
    
    print(f"Total Area: {total_area:.2f}")
    print(f"Total Perimeter: {total_perimeter:.2f}")
    
    # Demonstrate specific shape operations
    print("\nSpecific Shape Operations:")
    print("=" * 30)
    
    # Rectangle operations
    print("Rectangle operations:")
    rectangle.display_info()
    print(f"Is it a square? {rectangle.width == rectangle.height}")
    
    # Circle operations
    print("\nCircle operations:")
    circle.display_info()
    print(f"Circumference: {circle.perimeter():.2f}")
    
    # Triangle operations
    print("\nTriangle operations:")
    triangle.display_info()
    # Check if it's a right triangle
    sides = sorted([triangle.side1, triangle.side2, triangle.side3])
    is_right = abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 0.0001
    print(f"Is it a right triangle? {is_right}")
    
    # Square operations
    print("\nSquare operations:")
    square.display_info()
    print(f"Diagonal length: {square.side * math.sqrt(2):.2f}")
    
    # Interactive shape creation
    print("\nInteractive Shape Creation:")
    while True:
        print("\nChoose a shape to create:")
        print("1. Rectangle")
        print("2. Circle")
        print("3. Triangle")
        print("4. Square")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ")
        
        if choice == '5':
            break
            
        if choice == '1':
            try:
                width = float(input("Enter width: "))
                height = float(input("Enter height: "))
                color = input("Enter color [white]: ") or "white"
                shape = Rectangle(width, height, color)
                shape.display_info()
            except ValueError:
                print("Invalid input. Please enter numbers for dimensions.")
        elif choice == '2':
            try:
                radius = float(input("Enter radius: "))
                color = input("Enter color [white]: ") or "white"
                shape = Circle(radius, color)
                shape.display_info()
            except ValueError:
                print("Invalid input. Please enter a number for radius.")
        elif choice == '3':
            try:
                side1 = float(input("Enter side 1: "))
                side2 = float(input("Enter side 2: "))
                side3 = float(input("Enter side 3: "))
                color = input("Enter color [white]: ") or "white"
                # Check if sides can form a triangle
                if (side1 + side2 > side3) and (side1 + side3 > side2) and (side2 + side3 > side1):
                    shape = Triangle(side1, side2, side3, color)
                    shape.display_info()
                else:
                    print("Invalid triangle. The sum of any two sides must be greater than the third side.")
            except ValueError:
                print("Invalid input. Please enter numbers for sides.")
        elif choice == '4':
            try:
                side = float(input("Enter side length: "))
                color = input("Enter color [white]: ") or "white"
                shape = Square(side, color)
                shape.display_info()
            except ValueError:
                print("Invalid input. Please enter a number for side length.")
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()