"""
Temperature Converter Program
This program converts temperatures between Celsius, Fahrenheit, and Kelvin.
"""

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15

def fahrenheit_to_kelvin(fahrenheit):
    """Convert Fahrenheit to Kelvin."""
    celsius = fahrenheit_to_celsius(fahrenheit)
    return celsius_to_kelvin(celsius)

def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit."""
    celsius = kelvin_to_celsius(kelvin)
    return celsius_to_fahrenheit(celsius)

def main():
    """Main function to run the temperature converter."""
    print("Temperature Converter")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    print("5. Fahrenheit to Kelvin")
    print("6. Kelvin to Fahrenheit")
    
    while True:
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            try:
                celsius = float(input("Enter temperature in Celsius: "))
                fahrenheit = celsius_to_fahrenheit(celsius)
                print(f"{celsius}°C = {fahrenheit:.2f}°F")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '2':
            try:
                fahrenheit = float(input("Enter temperature in Fahrenheit: "))
                celsius = fahrenheit_to_celsius(fahrenheit)
                print(f"{fahrenheit}°F = {celsius:.2f}°C")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '3':
            try:
                celsius = float(input("Enter temperature in Celsius: "))
                kelvin = celsius_to_kelvin(celsius)
                print(f"{celsius}°C = {kelvin:.2f}K")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '4':
            try:
                kelvin = float(input("Enter temperature in Kelvin: "))
                celsius = kelvin_to_celsius(kelvin)
                print(f"{kelvin}K = {celsius:.2f}°C")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '5':
            try:
                fahrenheit = float(input("Enter temperature in Fahrenheit: "))
                kelvin = fahrenheit_to_kelvin(fahrenheit)
                print(f"{fahrenheit}°F = {kelvin:.2f}K")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '6':
            try:
                kelvin = float(input("Enter temperature in Kelvin: "))
                fahrenheit = kelvin_to_fahrenheit(kelvin)
                print(f"{kelvin}K = {fahrenheit:.2f}°F")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
        
        continue_conversion = input("Do you want to perform another conversion? (yes/no): ")
        if continue_conversion.lower() != 'yes':
            break

if __name__ == "__main__":
    main()