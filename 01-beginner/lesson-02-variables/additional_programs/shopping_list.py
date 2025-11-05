"""
Shopping List Program
This program demonstrates the use of variables and data types in a shopping context.
"""

def main():
    """Main function to manage a shopping list."""
    print("Shopping List Manager")
    print("-" * 20)
    
    # Initialize variables for shopping items and prices
    item1 = "Apples"
    price1 = 2.99
    quantity1 = 3
    
    item2 = "Bread"
    price2 = 1.50
    quantity2 = 2
    
    item3 = "Milk"
    price3 = 3.49
    quantity3 = 1
    
    # Calculate totals
    total1 = price1 * quantity1
    total2 = price2 * quantity2
    total3 = price3 * quantity3
    grand_total = total1 + total2 + total3
    
    # Display shopping list
    print("Your Shopping List:")
    print("-" * 30)
    print(f"{item1}: ${price1} x {quantity1} = ${total1:.2f}")
    print(f"{item2}: ${price2} x {quantity2} = ${total2:.2f}")
    print(f"{item3}: ${price3} x {quantity3} = ${total3:.2f}")
    print("-" * 30)
    print(f"Grand Total: ${grand_total:.2f}")
    
    # Demonstrate variable types
    print("\nVariable Types:")
    print(f"Item 1: {item1} (Type: {type(item1).__name__})")
    print(f"Price 1: {price1} (Type: {type(price1).__name__})")
    print(f"Quantity 1: {quantity1} (Type: {type(quantity1).__name__})")
    print(f"Total 1: {total1} (Type: {type(total1).__name__})")
    
    # Update shopping list
    print("\nUpdating shopping list...")
    discount = 0.10  # 10% discount
    discounted_total = grand_total * (1 - discount)
    print(f"Discount applied: {discount*100}%")
    print(f"Total after discount: ${discounted_total:.2f}")
    
    # Demonstrate boolean variable
    budget = 15.00
    within_budget = discounted_total <= budget
    print(f"\nBudget check:")
    print(f"Budget: ${budget:.2f}")
    print(f"Within budget: {within_budget}")

if __name__ == "__main__":
    main()