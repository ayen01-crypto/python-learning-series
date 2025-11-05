"""
Vehicle System
This program demonstrates Object-Oriented Programming concepts with a vehicle management system.
"""

class Vehicle:
    """Abstract base class for all vehicles."""
    
    def __init__(self, make, model, year, color="white"):
        """Initialize a vehicle."""
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.is_running = False
        self.speed = 0
    
    def start_engine(self):
        """Start the vehicle's engine."""
        if not self.is_running:
            self.is_running = True
            print(f"The {self.year} {self.make} {self.model}'s engine is now running.")
        else:
            print(f"The {self.year} {self.make} {self.model}'s engine is already running.")
    
    def stop_engine(self):
        """Stop the vehicle's engine."""
        if self.is_running:
            self.is_running = False
            self.speed = 0
            print(f"The {self.year} {self.make} {self.model}'s engine has been turned off.")
        else:
            print(f"The {self.year} {self.make} {self.model}'s engine is already off.")
    
    def accelerate(self, speed_increase):
        """Accelerate the vehicle."""
        if self.is_running:
            self.speed += speed_increase
            print(f"The {self.year} {self.make} {self.model} is now traveling at {self.speed} mph.")
        else:
            print("You need to start the engine first!")
    
    def brake(self, speed_decrease):
        """Apply brakes to the vehicle."""
        if self.is_running:
            self.speed = max(0, self.speed - speed_decrease)
            print(f"The {self.year} {self.make} {self.model} slowed down to {self.speed} mph.")
        else:
            print("The vehicle is not moving.")
    
    def display_info(self):
        """Display information about the vehicle."""
        print(f"Vehicle: {self.year} {self.make} {self.model}")
        print(f"Color: {self.color}")
        print(f"Engine Status: {'Running' if self.is_running else 'Off'}")
        print(f"Current Speed: {self.speed} mph")


class Car(Vehicle):
    """A class representing a car."""
    
    def __init__(self, make, model, year, color="white", num_doors=4):
        """Initialize a car."""
        super().__init__(make, model, year, color)
        self.num_doors = num_doors
        self.fuel_level = 100  # Percentage
    
    def drive(self, distance):
        """Drive the car for a certain distance."""
        if self.is_running:
            fuel_consumed = distance * 0.1  # Simplified fuel consumption
            if self.fuel_level >= fuel_consumed:
                self.fuel_level -= fuel_consumed
                print(f"Drove {distance} miles. Fuel level is now {self.fuel_level:.1f}%.")
            else:
                print("Not enough fuel to drive that distance!")
        else:
            print("Start the engine first!")
    
    def refuel(self, amount=100):
        """Refuel the car."""
        self.fuel_level = min(100, self.fuel_level + amount)
        print(f"Refueled. Fuel level is now {self.fuel_level:.1f}%.")
    
    def display_info(self):
        """Display information about the car."""
        super().display_info()
        print(f"Number of Doors: {self.num_doors}")
        print(f"Fuel Level: {self.fuel_level:.1f}%")


class Motorcycle(Vehicle):
    """A class representing a motorcycle."""
    
    def __init__(self, make, model, year, color="black", engine_size=600):
        """Initialize a motorcycle."""
        super().__init__(make, model, year, color)
        self.engine_size = engine_size  # in cc
        self.has_sidecar = False
    
    def wheelie(self):
        """Perform a wheelie."""
        if self.is_running and self.speed > 20:
            print(f"The {self.year} {self.make} {self.model} pops a wheelie!")
        elif self.is_running:
            print("You need to go faster to pop a wheelie!")
        else:
            print("Start the engine first!")
    
    def add_sidecar(self):
        """Add a sidecar to the motorcycle."""
        self.has_sidecar = True
        print(f"A sidecar has been added to the {self.year} {self.make} {self.model}.")
    
    def display_info(self):
        """Display information about the motorcycle."""
        super().display_info()
        print(f"Engine Size: {self.engine_size}cc")
        print(f"Has Sidecar: {'Yes' if self.has_sidecar else 'No'}")


class Truck(Vehicle):
    """A class representing a truck."""
    
    def __init__(self, make, model, year, color="white", cargo_capacity=1000):
        """Initialize a truck."""
        super().__init__(make, model, year, color)
        self.cargo_capacity = cargo_capacity  # in pounds
        self.current_cargo = 0
    
    def load_cargo(self, weight):
        """Load cargo into the truck."""
        if self.current_cargo + weight <= self.cargo_capacity:
            self.current_cargo += weight
            print(f"Loaded {weight} pounds of cargo. Total cargo: {self.current_cargo} pounds.")
        else:
            print(f"Cannot load {weight} pounds. Exceeds capacity by {self.current_cargo + weight - self.cargo_capacity} pounds.")
    
    def unload_cargo(self, weight):
        """Unload cargo from the truck."""
        if weight <= self.current_cargo:
            self.current_cargo -= weight
            print(f"Unloaded {weight} pounds of cargo. Remaining cargo: {self.current_cargo} pounds.")
        else:
            print(f"Cannot unload {weight} pounds. Only {self.current_cargo} pounds of cargo available.")
    
    def display_info(self):
        """Display information about the truck."""
        super().display_info()
        print(f"Cargo Capacity: {self.cargo_capacity} pounds")
        print(f"Current Cargo: {self.current_cargo} pounds")
        print(f"Capacity Used: {self.current_cargo/self.cargo_capacity*100:.1f}%")


def main():
    """Main function to demonstrate the vehicle system."""
    print("Vehicle Management System")
    print("=" * 25)
    
    # Create different types of vehicles
    car = Car("Toyota", "Camry", 2022, "blue", 4)
    motorcycle = Motorcycle("Harley-Davidson", "Street 750", 2021, "black", 750)
    truck = Truck("Ford", "F-150", 2023, "red", 2000)
    
    # Store vehicles in a list
    vehicles = [car, motorcycle, truck]
    
    # Demonstrate vehicle operations
    print("Vehicle Operations:")
    print("=" * 20)
    
    for vehicle in vehicles:
        print(f"\nTesting {vehicle.__class__.__name__}:")
        vehicle.display_info()
        vehicle.start_engine()
        vehicle.accelerate(30)
        vehicle.brake(10)
        vehicle.stop_engine()
        print("-" * 15)
    
    # Demonstrate specific vehicle operations
    print("\nSpecific Vehicle Operations:")
    print("=" * 30)
    
    # Car operations
    print("Car operations:")
    car.display_info()
    car.drive(50)
    car.refuel(30)
    car.drive(100)
    
    # Motorcycle operations
    print("\nMotorcycle operations:")
    motorcycle.display_info()
    motorcycle.start_engine()
    motorcycle.accelerate(25)
    motorcycle.wheelie()
    motorcycle.accelerate(10)
    motorcycle.wheelie()
    motorcycle.add_sidecar()
    motorcycle.display_info()
    
    # Truck operations
    print("\nTruck operations:")
    truck.display_info()
    truck.load_cargo(800)
    truck.load_cargo(500)  # This should fail
    truck.load_cargo(300)
    truck.display_info()
    truck.unload_cargo(200)
    truck.display_info()
    
    # Interactive vehicle management
    print("\nInteractive Vehicle Management:")
    current_vehicle = car
    
    while True:
        print("\nChoose an operation:")
        print("1. Display vehicle info")
        print("2. Start engine")
        print("3. Stop engine")
        print("4. Accelerate")
        print("5. Brake")
        print("6. Switch vehicle")
        print("7. Specific operations (Car: drive/refuel, Motorcycle: wheelie/sidecar, Truck: load/unload)")
        print("8. Exit")
        
        choice = input("Enter choice (1-8): ")
        
        if choice == '8':
            break
            
        if choice == '1':
            current_vehicle.display_info()
        elif choice == '2':
            current_vehicle.start_engine()
        elif choice == '3':
            current_vehicle.stop_engine()
        elif choice == '4':
            try:
                speed = int(input("Enter speed increase: "))
                current_vehicle.accelerate(speed)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '5':
            try:
                speed = int(input("Enter speed decrease: "))
                current_vehicle.brake(speed)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '6':
            print("Available vehicles:")
            print("1. Toyota Camry (Car)")
            print("2. Harley-Davidson Street 750 (Motorcycle)")
            print("3. Ford F-150 (Truck)")
            vehicle_choice = input("Select vehicle (1-3): ")
            
            if vehicle_choice == '1':
                current_vehicle = car
                print("Switched to Toyota Camry")
            elif vehicle_choice == '2':
                current_vehicle = motorcycle
                print("Switched to Harley-Davidson Street 750")
            elif vehicle_choice == '3':
                current_vehicle = truck
                print("Switched to Ford F-150")
            else:
                print("Invalid choice.")
        elif choice == '7':
            if isinstance(current_vehicle, Car):
                print("Car specific operations:")
                print("1. Drive")
                print("2. Refuel")
                op_choice = input("Enter choice (1-2): ")
                if op_choice == '1':
                    try:
                        distance = float(input("Enter distance to drive (miles): "))
                        current_vehicle.drive(distance)
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                elif op_choice == '2':
                    try:
                        amount = float(input("Enter refuel amount [100]: ") or "100")
                        current_vehicle.refuel(amount)
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            elif isinstance(current_vehicle, Motorcycle):
                print("Motorcycle specific operations:")
                print("1. Wheelie")
                print("2. Add sidecar")
                op_choice = input("Enter choice (1-2): ")
                if op_choice == '1':
                    current_vehicle.wheelie()
                elif op_choice == '2':
                    current_vehicle.add_sidecar()
            elif isinstance(current_vehicle, Truck):
                print("Truck specific operations:")
                print("1. Load cargo")
                print("2. Unload cargo")
                op_choice = input("Enter choice (1-2): ")
                if op_choice == '1':
                    try:
                        weight = float(input("Enter cargo weight (pounds): "))
                        current_vehicle.load_cargo(weight)
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                elif op_choice == '2':
                    try:
                        weight = float(input("Enter cargo weight to unload (pounds): "))
                        current_vehicle.unload_cargo(weight)
                    except ValueError:
                        print("Invalid input. Please enter a number.")
        else:
            print("Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    main()