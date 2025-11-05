"""
Inventory Manager Program
This program demonstrates the use of lists, dictionaries, and tuples for inventory management.
"""

def add_item(inventory, item_name, quantity, price):
    """Add an item to the inventory."""
    inventory[item_name] = {
        'quantity': quantity,
        'price': price
    }

def remove_item(inventory, item_name):
    """Remove an item from the inventory."""
    if item_name in inventory:
        del inventory[item_name]
        return True
    else:
        return False

def update_quantity(inventory, item_name, new_quantity):
    """Update the quantity of an item."""
    if item_name in inventory:
        inventory[item_name]['quantity'] = new_quantity
        return True
    else:
        return False

def update_price(inventory, item_name, new_price):
    """Update the price of an item."""
    if item_name in inventory:
        inventory[item_name]['price'] = new_price
        return True
    else:
        return False

def get_item_info(inventory, item_name):
    """Get information about an item."""
    if item_name in inventory:
        return inventory[item_name]
    else:
        return None

def list_all_items(inventory):
    """List all items in the inventory."""
    if not inventory:
        print("Inventory is empty.")
        return
    
    print("Current Inventory:")
    print("-" * 40)
    for item_name, details in inventory.items():
        print(f"Item: {item_name}")
        print(f"  Quantity: {details['quantity']}")
        print(f"  Price: ${details['price']:.2f}")
        print(f"  Total Value: ${details['quantity'] * details['price']:.2f}")
        print()

def calculate_total_value(inventory):
    """Calculate the total value of all items in inventory."""
    total = 0
    for details in inventory.values():
        total += details['quantity'] * details['price']
    return total

def find_low_stock_items(inventory, threshold):
    """Find items with quantity below the threshold."""
    low_stock = []
    for item_name, details in inventory.items():
        if details['quantity'] < threshold:
            low_stock.append((item_name, details['quantity']))
    return low_stock

def main():
    """Main function to run the inventory manager."""
    print("Inventory Manager")
    print("=" * 20)
    
    # Initialize inventory with some items
    inventory = {}
    
    # Add some initial items
    add_item(inventory, "Apples", 50, 0.50)
    add_item(inventory, "Bananas", 30, 0.30)
    add_item(inventory, "Oranges", 40, 0.60)
    add_item(inventory, "Bread", 20, 2.00)
    add_item(inventory, "Milk", 15, 3.50)
    
    print("Initial inventory created.")
    list_all_items(inventory)
    
    # Demonstrate inventory operations
    print("Performing inventory operations...")
    
    # Add a new item
    add_item(inventory, "Eggs", 25, 2.50)
    print("Added Eggs to inventory.")
    
    # Update quantity
    update_quantity(inventory, "Apples", 60)
    print("Updated Apples quantity to 60.")
    
    # Update price
    update_price(inventory, "Bananas", 0.35)
    print("Updated Bananas price to $0.35.")
    
    # Remove an item
    remove_item(inventory, "Bread")
    print("Removed Bread from inventory.")
    
    # Display updated inventory
    print("\nUpdated Inventory:")
    list_all_items(inventory)
    
    # Calculate total value
    total_value = calculate_total_value(inventory)
    print(f"Total inventory value: ${total_value:.2f}")
    
    # Find low stock items
    low_stock = find_low_stock_items(inventory, 20)
    if low_stock:
        print("\nLow stock items (quantity < 20):")
        for item_name, quantity in low_stock:
            print(f"  {item_name}: {quantity} units")
    else:
        print("\nNo low stock items.")
    
    # Interactive inventory management
    print("\nInteractive Inventory Management:")
    while True:
        print("\nChoose an operation:")
        print("1. Add item")
        print("2. Remove item")
        print("3. Update quantity")
        print("4. Update price")
        print("5. View item details")
        print("6. List all items")
        print("7. Exit")
        
        choice = input("Enter choice (1-7): ")
        
        if choice == '7':
            break
            
        if choice == '1':
            item_name = input("Enter item name: ")
            try:
                quantity = int(input("Enter quantity: "))
                price = float(input("Enter price: $"))
                add_item(inventory, item_name, quantity, price)
                print(f"Added {item_name} to inventory.")
            except ValueError:
                print("Invalid input. Please enter valid numbers for quantity and price.")
        elif choice == '2':
            item_name = input("Enter item name to remove: ")
            if remove_item(inventory, item_name):
                print(f"Removed {item_name} from inventory.")
            else:
                print(f"Item {item_name} not found in inventory.")
        elif choice == '3':
            item_name = input("Enter item name: ")
            try:
                new_quantity = int(input("Enter new quantity: "))
                if update_quantity(inventory, item_name, new_quantity):
                    print(f"Updated {item_name} quantity to {new_quantity}.")
                else:
                    print(f"Item {item_name} not found in inventory.")
            except ValueError:
                print("Invalid input. Please enter a valid number for quantity.")
        elif choice == '4':
            item_name = input("Enter item name: ")
            try:
                new_price = float(input("Enter new price: $"))
                if update_price(inventory, item_name, new_price):
                    print(f"Updated {item_name} price to ${new_price:.2f}.")
                else:
                    print(f"Item {item_name} not found in inventory.")
            except ValueError:
                print("Invalid input. Please enter a valid number for price.")
        elif choice == '5':
            item_name = input("Enter item name: ")
            info = get_item_info(inventory, item_name)
            if info:
                print(f"\n{item_name}:")
                print(f"  Quantity: {info['quantity']}")
                print(f"  Price: ${info['price']:.2f}")
                print(f"  Total Value: ${info['quantity'] * info['price']:.2f}")
            else:
                print(f"Item {item_name} not found in inventory.")
        elif choice == '6':
            list_all_items(inventory)
        else:
            print("Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    main()