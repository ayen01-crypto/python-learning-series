"""
Bank Account System
This program demonstrates Object-Oriented Programming concepts with a bank account system.
"""

class BankAccount:
    """A class representing a bank account."""
    
    # Class variable (shared by all instances)
    bank_name = "Python National Bank"
    
    def __init__(self, account_holder, initial_balance=0):
        """Initialize a new bank account."""
        self.account_holder = account_holder  # Instance variable
        self.balance = initial_balance        # Instance variable
        self.transaction_history = []         # Instance variable
    
    def deposit(self, amount):
        """Deposit money into the account."""
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited ${amount:.2f}")
            return True
        else:
            print("Deposit amount must be positive.")
            return False
    
    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        elif amount > self.balance:
            print("Insufficient funds.")
            return False
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount:.2f}")
            return True
    
    def get_balance(self):
        """Get the current account balance."""
        return self.balance
    
    def display_account_info(self):
        """Display account information."""
        print(f"Bank: {self.bank_name}")
        print(f"Account Holder: {self.account_holder}")
        print(f"Balance: ${self.balance:.2f}")
    
    def display_transaction_history(self):
        """Display transaction history."""
        if not self.transaction_history:
            print("No transactions yet.")
        else:
            print("Transaction History:")
            for transaction in self.transaction_history:
                print(f"  {transaction}")


class SavingsAccount(BankAccount):
    """A class representing a savings account with interest."""
    
    def __init__(self, account_holder, initial_balance=0, interest_rate=0.02):
        """Initialize a new savings account."""
        super().__init__(account_holder, initial_balance)
        self.interest_rate = interest_rate  # Additional instance variable
    
    def apply_interest(self):
        """Apply interest to the account."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.transaction_history.append(f"Interest applied: ${interest:.2f}")
        print(f"Interest of ${interest:.2f} applied. New balance: ${self.balance:.2f}")
    
    def display_account_info(self):
        """Display savings account information."""
        super().display_account_info()
        print(f"Interest Rate: {self.interest_rate*100:.2f}%")


class CheckingAccount(BankAccount):
    """A class representing a checking account with overdraft protection."""
    
    def __init__(self, account_holder, initial_balance=0, overdraft_limit=100):
        """Initialize a new checking account."""
        super().__init__(account_holder, initial_balance)
        self.overdraft_limit = overdraft_limit  # Additional instance variable
    
    def withdraw(self, amount):
        """Withdraw money from the checking account with overdraft protection."""
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        elif amount > (self.balance + self.overdraft_limit):
            print("Transaction denied. Exceeds overdraft limit.")
            return False
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount:.2f}")
            return True
    
    def display_account_info(self):
        """Display checking account information."""
        super().display_account_info()
        print(f"Overdraft Limit: ${self.overdraft_limit:.2f}")


def main():
    """Main function to demonstrate the bank account system."""
    print("Bank Account System")
    print("=" * 20)
    
    # Create different types of accounts
    basic_account = BankAccount("Alice Johnson", 1000)
    savings_account = SavingsAccount("Bob Smith", 2000, 0.03)
    checking_account = CheckingAccount("Charlie Brown", 1500, 200)
    
    # Demonstrate basic account operations
    print("Basic Account Operations:")
    basic_account.display_account_info()
    basic_account.deposit(500)
    basic_account.withdraw(200)
    print(f"Updated balance: ${basic_account.get_balance():.2f}")
    basic_account.display_transaction_history()
    
    print("\n" + "="*50)
    
    # Demonstrate savings account operations
    print("Savings Account Operations:")
    savings_account.display_account_info()
    savings_account.deposit(300)
    savings_account.apply_interest()
    savings_account.display_transaction_history()
    
    print("\n" + "="*50)
    
    # Demonstrate checking account operations
    print("Checking Account Operations:")
    checking_account.display_account_info()
    checking_account.withdraw(1600)  # This should work due to overdraft
    checking_account.withdraw(300)   # This should be denied
    print(f"Updated balance: ${checking_account.get_balance():.2f}")
    checking_account.display_transaction_history()
    
    # Interactive banking system
    print("\nInteractive Banking System:")
    current_account = basic_account
    
    while True:
        print("\nChoose an operation:")
        print("1. Display account info")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Switch account")
        print("5. Apply interest (Savings only)")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ")
        
        if choice == '6':
            break
            
        if choice == '1':
            current_account.display_account_info()
            current_account.display_transaction_history()
        elif choice == '2':
            try:
                amount = float(input("Enter deposit amount: $"))
                if current_account.deposit(amount):
                    print(f"Deposit successful. New balance: ${current_account.get_balance():.2f}")
            except ValueError:
                print("Invalid amount. Please enter a number.")
        elif choice == '3':
            try:
                amount = float(input("Enter withdrawal amount: $"))
                if current_account.withdraw(amount):
                    print(f"Withdrawal successful. New balance: ${current_account.get_balance():.2f}")
            except ValueError:
                print("Invalid amount. Please enter a number.")
        elif choice == '4':
            print("Available accounts:")
            print("1. Alice Johnson (Basic)")
            print("2. Bob Smith (Savings)")
            print("3. Charlie Brown (Checking)")
            account_choice = input("Select account (1-3): ")
            
            if account_choice == '1':
                current_account = basic_account
                print("Switched to Alice Johnson's account")
            elif account_choice == '2':
                current_account = savings_account
                print("Switched to Bob Smith's account")
            elif account_choice == '3':
                current_account = checking_account
                print("Switched to Charlie Brown's account")
            else:
                print("Invalid choice.")
        elif choice == '5':
            if isinstance(current_account, SavingsAccount):
                current_account.apply_interest()
            else:
                print("Interest can only be applied to savings accounts.")
        else:
            print("Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()