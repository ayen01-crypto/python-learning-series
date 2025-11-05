"""
Simple Bank Program
This program demonstrates functions for banking operations.
"""

def create_account(initial_balance=0):
    """Create a new bank account with an initial balance."""
    return initial_balance

def deposit(balance, amount):
    """Deposit money into the account."""
    if amount > 0:
        return balance + amount
    else:
        print("Deposit amount must be positive.")
        return balance

def withdraw(balance, amount):
    """Withdraw money from the account."""
    if amount <= 0:
        print("Withdrawal amount must be positive.")
        return balance
    elif amount > balance:
        print("Insufficient funds.")
        return balance
    else:
        return balance - amount

def check_balance(balance):
    """Check the current account balance."""
    return balance

def transfer(from_balance, to_balance, amount):
    """Transfer money from one account to another."""
    if amount <= 0:
        print("Transfer amount must be positive.")
        return from_balance, to_balance
    elif amount > from_balance:
        print("Insufficient funds for transfer.")
        return from_balance, to_balance
    else:
        new_from_balance = from_balance - amount
        new_to_balance = to_balance + amount
        return new_from_balance, new_to_balance

def calculate_interest(balance, rate, time):
    """Calculate simple interest."""
    interest = balance * rate * time
    return interest

def apply_interest(balance, interest):
    """Apply interest to the account balance."""
    return balance + interest

def main():
    """Main function to run the bank program."""
    print("Simple Bank Program")
    print("=" * 20)
    
    # Create accounts
    account1 = create_account(1000.00)
    account2 = create_account(500.00)
    
    print(f"Account 1 initial balance: ${account1:.2f}")
    print(f"Account 2 initial balance: ${account2:.2f}")
    
    # Perform banking operations
    print("\nPerforming banking operations...")
    
    # Deposit money
    account1 = deposit(account1, 200.00)
    print(f"After deposit of $200: Account 1 = ${account1:.2f}")
    
    # Withdraw money
    account1 = withdraw(account1, 150.00)
    print(f"After withdrawal of $150: Account 1 = ${account1:.2f}")
    
    # Transfer money
    account1, account2 = transfer(account1, account2, 300.00)
    print(f"After transfer of $300:")
    print(f"  Account 1: ${account1:.2f}")
    print(f"  Account 2: ${account2:.2f}")
    
    # Check balances
    print(f"\nCurrent balances:")
    print(f"  Account 1: ${check_balance(account1):.2f}")
    print(f"  Account 2: ${check_balance(account2):.2f}")
    
    # Calculate and apply interest
    interest_rate = 0.05  # 5% annual interest
    time_period = 1  # 1 year
    
    interest1 = calculate_interest(account1, interest_rate, time_period)
    interest2 = calculate_interest(account2, interest_rate, time_period)
    
    account1 = apply_interest(account1, interest1)
    account2 = apply_interest(account2, interest2)
    
    print(f"\nAfter applying {interest_rate*100}% annual interest:")
    print(f"  Account 1 earned ${interest1:.2f}, new balance: ${account1:.2f}")
    print(f"  Account 2 earned ${interest2:.2f}, new balance: ${account2:.2f}")
    
    # Interactive banking
    print("\nInteractive Banking:")
    current_account = account1  # Start with account 1
    
    while True:
        print("\nChoose an operation:")
        print("1. Check balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Switch account")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ")
        
        if choice == '5':
            break
            
        if choice == '1':
            print(f"Current balance: ${check_balance(current_account):.2f}")
        elif choice == '2':
            try:
                amount = float(input("Enter deposit amount: $"))
                current_account = deposit(current_account, amount)
                print(f"New balance: ${current_account:.2f}")
            except ValueError:
                print("Invalid amount. Please enter a number.")
        elif choice == '3':
            try:
                amount = float(input("Enter withdrawal amount: $"))
                current_account = withdraw(current_account, amount)
                print(f"New balance: ${current_account:.2f}")
            except ValueError:
                print("Invalid amount. Please enter a number.")
        elif choice == '4':
            if current_account == account1:
                current_account = account2
                print("Switched to Account 2")
            else:
                current_account = account1
                print("Switched to Account 1")
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()