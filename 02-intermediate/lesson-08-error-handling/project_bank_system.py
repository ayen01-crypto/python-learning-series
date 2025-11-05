"""
Mini Project: Bank Account System

A robust banking system with comprehensive error handling and transaction management.
Demonstrates custom exceptions, validation, and defensive programming.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


# ============================================
# Custom Exceptions
# ============================================

class BankingError(Exception):
    """Base exception for all banking operations."""
    pass

class InsufficientFundsError(BankingError):
    """Raised when account has insufficient funds for a transaction."""
    def __init__(self, balance: float, amount: float, account_id: str):
        self.balance = balance
        self.amount = amount
        self.account_id = account_id
        super().__init__(
            f"Account {account_id}: Insufficient funds. "
            f"Balance: ${balance:.2f}, Requested: ${amount:.2f}"
        )

class InvalidAmountError(BankingError):
    """Raised when transaction amount is invalid."""
    def __init__(self, amount: float, reason: str):
        self.amount = amount
        self.reason = reason
        super().__init__(f"Invalid amount ${amount}: {reason}")

class AccountNotFoundError(BankingError):
    """Raised when account is not found."""
    def __init__(self, account_id: str):
        self.account_id = account_id
        super().__init__(f"Account {account_id} not found")

class TransactionError(BankingError):
    """Raised when transaction fails."""
    def __init__(self, transaction_id: str, reason: str):
        self.transaction_id = transaction_id
        self.reason = reason
        super().__init__(f"Transaction {transaction_id} failed: {reason}")


# ============================================
# Data Classes
# ============================================

class TransactionType(Enum):
    """Types of banking transactions."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"

class Transaction:
    """Represents a banking transaction."""
    
    def __init__(self, transaction_id: str, account_id: str, 
                 transaction_type: TransactionType, amount: float,
                 description: str = "", target_account: str = ""):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.target_account = target_account
        self.timestamp = datetime.now()
        self.status = "pending"
    
    def complete(self):
        """Mark transaction as completed."""
        self.status = "completed"
    
    def fail(self, reason: str):
        """Mark transaction as failed."""
        self.status = "failed"
        self.description = reason
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'transaction_id': self.transaction_id,
            'account_id': self.account_id,
            'transaction_type': self.transaction_type.value,
            'amount': self.amount,
            'description': self.description,
            'target_account': self.target_account,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status
        }

class Account:
    """Represents a bank account."""
    
    def __init__(self, account_id: str, owner: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self.owner = owner
        self.balance = initial_balance
        self.created_date = datetime.now()
        self.is_active = True
    
    def deposit(self, amount: float) -> float:
        """Deposit money into account."""
        if amount <= 0:
            raise InvalidAmountError(amount, "Deposit amount must be positive")
        
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount: float) -> float:
        """Withdraw money from account."""
        if amount <= 0:
            raise InvalidAmountError(amount, "Withdrawal amount must be positive")
        
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount, self.account_id)
        
        self.balance -= amount
        return self.balance
    
    def get_balance(self) -> float:
        """Get current balance."""
        return self.balance
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'account_id': self.account_id,
            'owner': self.owner,
            'balance': self.balance,
            'created_date': self.created_date.isoformat(),
            'is_active': self.is_active
        }


# ============================================
# Bank System
# ============================================

class Bank:
    """Main banking system."""
    
    def __init__(self, name: str):
        self.name = name
        self.accounts: Dict[str, Account] = {}
        self.transactions: List[Transaction] = []
        self._transaction_counter = 0
    
    def create_account(self, owner: str, initial_balance: float = 0.0) -> str:
        """Create a new bank account."""
        # Validate initial balance
        if initial_balance < 0:
            raise InvalidAmountError(initial_balance, "Initial balance cannot be negative")
        
        # Generate unique account ID
        account_id = self._generate_account_id()
        
        # Create account
        account = Account(account_id, owner, initial_balance)
        self.accounts[account_id] = account
        
        # Log creation
        logging.info(f"Account {account_id} created for {owner} with balance ${initial_balance:.2f}")
        
        return account_id
    
    def get_account(self, account_id: str) -> Account:
        """Get account by ID."""
        if account_id not in self.accounts:
            raise AccountNotFoundError(account_id)
        return self.accounts[account_id]
    
    def deposit(self, account_id: str, amount: float, description: str = "") -> str:
        """Make a deposit to an account."""
        account = self.get_account(account_id)
        
        try:
            # Perform deposit
            new_balance = account.deposit(amount)
            
            # Create transaction record
            transaction_id = self._create_transaction(
                account_id, TransactionType.DEPOSIT, amount, description
            )
            
            # Complete transaction
            self._complete_transaction(transaction_id)
            
            logging.info(f"Deposit: ${amount:.2f} to {account_id}. New balance: ${new_balance:.2f}")
            return transaction_id
            
        except BankingError:
            raise
        except Exception as e:
            transaction_id = self._create_transaction(
                account_id, TransactionType.DEPOSIT, amount, f"Failed: {str(e)}"
            )
            self._fail_transaction(transaction_id, str(e))
            raise TransactionError(transaction_id, str(e))
    
    def withdraw(self, account_id: str, amount: float, description: str = "") -> str:
        """Withdraw money from an account."""
        account = self.get_account(account_id)
        
        try:
            # Perform withdrawal
            new_balance = account.withdraw(amount)
            
            # Create transaction record
            transaction_id = self._create_transaction(
                account_id, TransactionType.WITHDRAWAL, amount, description
            )
            
            # Complete transaction
            self._complete_transaction(transaction_id)
            
            logging.info(f"Withdrawal: ${amount:.2f} from {account_id}. New balance: ${new_balance:.2f}")
            return transaction_id
            
        except BankingError:
            raise
        except Exception as e:
            transaction_id = self._create_transaction(
                account_id, TransactionType.WITHDRAWAL, amount, f"Failed: {str(e)}"
            )
            self._fail_transaction(transaction_id, str(e))
            raise TransactionError(transaction_id, str(e))
    
    def transfer(self, from_account_id: str, to_account_id: str, 
                 amount: float, description: str = "") -> str:
        """Transfer money between accounts."""
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        
        if from_account_id == to_account_id:
            raise TransactionError("", "Cannot transfer to the same account")
        
        try:
            # Perform withdrawal from source account
            from_account.withdraw(amount)
            
            # Perform deposit to target account
            to_account.deposit(amount)
            
            # Create transaction record
            transaction_id = self._create_transaction(
                from_account_id, TransactionType.TRANSFER, amount, 
                description, to_account_id
            )
            
            # Complete transaction
            self._complete_transaction(transaction_id)
            
            logging.info(
                f"Transfer: ${amount:.2f} from {from_account_id} to {to_account_id}"
            )
            return transaction_id
            
        except BankingError:
            # Rollback if needed
            if from_account.get_balance() < amount:
                # Withdrawal was successful but deposit failed
                to_account.withdraw(amount)  # Undo deposit
                from_account.deposit(amount)  # Restore funds
            
            raise
        except Exception as e:
            transaction_id = self._create_transaction(
                from_account_id, TransactionType.TRANSFER, amount, 
                f"Failed: {str(e)}", to_account_id
            )
            self._fail_transaction(transaction_id, str(e))
            raise TransactionError(transaction_id, str(e))
    
    def get_balance(self, account_id: str) -> float:
        """Get account balance."""
        account = self.get_account(account_id)
        return account.get_balance()
    
    def get_transaction_history(self, account_id: str) -> List[Transaction]:
        """Get transaction history for an account."""
        self.get_account(account_id)  # Validate account exists
        return [t for t in self.transactions if t.account_id == account_id]
    
    def get_failed_transactions(self) -> List[Transaction]:
        """Get all failed transactions."""
        return [t for t in self.transactions if t.status == "failed"]
    
    def get_statistics(self) -> Dict:
        """Get bank statistics."""
        total_accounts = len(self.accounts)
        active_accounts = sum(1 for acc in self.accounts.values() if acc.is_active)
        
        total_deposits = sum(t.amount for t in self.transactions 
                           if t.transaction_type == TransactionType.DEPOSIT 
                           and t.status == "completed")
        
        total_withdrawals = sum(t.amount for t in self.transactions 
                              if t.transaction_type == TransactionType.WITHDRAWAL 
                              and t.status == "completed")
        
        return {
            "total_accounts": total_accounts,
            "active_accounts": active_accounts,
            "total_deposits": total_deposits,
            "total_withdrawals": total_withdrawals,
            "total_transactions": len(self.transactions)
        }
    
    def _generate_account_id(self) -> str:
        """Generate unique account ID."""
        import uuid
        return f"ACC{str(uuid.uuid4())[:8].upper()}"
    
    def _create_transaction(self, account_id: str, transaction_type: TransactionType,
                          amount: float, description: str = "", 
                          target_account: str = "") -> str:
        """Create a new transaction record."""
        self._transaction_counter += 1
        transaction_id = f"TXN{self._transaction_counter:06d}"
        
        transaction = Transaction(
            transaction_id, account_id, transaction_type, amount, 
            description, target_account
        )
        self.transactions.append(transaction)
        
        return transaction_id
    
    def _complete_transaction(self, transaction_id: str):
        """Mark transaction as completed."""
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                transaction.complete()
                break
    
    def _fail_transaction(self, transaction_id: str, reason: str):
        """Mark transaction as failed."""
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                transaction.fail(reason)
                break


# ============================================
# User Interface
# ============================================

def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def print_menu():
    """Display main menu."""
    print("\n" + "-" * 70)
    print("\n📋 MAIN MENU:")
    print("1.  Create Account")
    print("2.  Check Balance")
    print("3.  Deposit")
    print("4.  Withdraw")
    print("5.  Transfer")
    print("6.  View Transaction History")
    print("7.  View Failed Transactions")
    print("8.  Bank Statistics")
    print("9.  Load Sample Data")
    print("10. Exit")


def create_account_interactive(bank: Bank):
    """Interactive account creation."""
    print_header("➕ CREATE NEW ACCOUNT")
    
    owner = input("Account owner name: ").strip()
    if not owner:
        print("❌ Owner name is required!")
        return
    
    try:
        initial_balance = float(input("Initial deposit (0): ") or "0")
        account_id = bank.create_account(owner, initial_balance)
        print(f"✅ Account created successfully! Account ID: {account_id}")
        print(f"   Current balance: ${initial_balance:.2f}")
    except InvalidAmountError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error creating account: {e}")


def check_balance_interactive(bank: Bank):
    """Interactive balance checking."""
    print_header("💰 CHECK BALANCE")
    
    account_id = input("Account ID: ").strip()
    
    try:
        balance = bank.get_balance(account_id)
        print(f"✅ Current balance: ${balance:.2f}")
    except AccountNotFoundError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error checking balance: {e}")


def deposit_interactive(bank: Bank):
    """Interactive deposit."""
    print_header("📥 DEPOSIT")
    
    account_id = input("Account ID: ").strip()
    try:
        amount = float(input("Amount: "))
        description = input("Description (optional): ").strip()
        
        transaction_id = bank.deposit(account_id, amount, description)
        balance = bank.get_balance(account_id)
        print(f"✅ Deposit successful! Transaction ID: {transaction_id}")
        print(f"   New balance: ${balance:.2f}")
    except (AccountNotFoundError, InvalidAmountError, InsufficientFundsError) as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error processing deposit: {e}")


def withdraw_interactive(bank: Bank):
    """Interactive withdrawal."""
    print_header("📤 WITHDRAW")
    
    account_id = input("Account ID: ").strip()
    try:
        amount = float(input("Amount: "))
        description = input("Description (optional): ").strip()
        
        transaction_id = bank.withdraw(account_id, amount, description)
        balance = bank.get_balance(account_id)
        print(f"✅ Withdrawal successful! Transaction ID: {transaction_id}")
        print(f"   New balance: ${balance:.2f}")
    except (AccountNotFoundError, InvalidAmountError, InsufficientFundsError) as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error processing withdrawal: {e}")


def transfer_interactive(bank: Bank):
    """Interactive transfer."""
    print_header("💱 TRANSFER")
    
    from_account = input("From Account ID: ").strip()
    to_account = input("To Account ID: ").strip()
    try:
        amount = float(input("Amount: "))
        description = input("Description (optional): ").strip()
        
        transaction_id = bank.transfer(from_account, to_account, amount, description)
        from_balance = bank.get_balance(from_account)
        to_balance = bank.get_balance(to_account)
        print(f"✅ Transfer successful! Transaction ID: {transaction_id}")
        print(f"   From account balance: ${from_balance:.2f}")
        print(f"   To account balance: ${to_balance:.2f}")
    except (AccountNotFoundError, InvalidAmountError, InsufficientFundsError, 
            TransactionError) as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error processing transfer: {e}")


def view_transaction_history_interactive(bank: Bank):
    """Interactive transaction history viewing."""
    print_header("📜 TRANSACTION HISTORY")
    
    account_id = input("Account ID: ").strip()
    
    try:
        transactions = bank.get_transaction_history(account_id)
        
        if not transactions:
            print("❌ No transactions found!")
            return
        
        print(f"\n✅ Found {len(transactions)} transaction(s):\n")
        print(f"{'ID':<12} {'TYPE':<12} {'AMOUNT':<12} {'STATUS':<10} {'TIMESTAMP'}")
        print("-" * 70)
        
        for transaction in sorted(transactions, key=lambda t: t.timestamp, reverse=True):
            timestamp = transaction.timestamp.strftime("%Y-%m-%d %H:%M")
            amount = f"${transaction.amount:.2f}"
            print(f"{transaction.transaction_id:<12} {transaction.transaction_type.value:<12} "
                  f"{amount:<12} {transaction.status:<10} {timestamp}")
            
            if transaction.description:
                print(f"           Description: {transaction.description}")
            if transaction.target_account:
                print(f"           To: {transaction.target_account}")
            print()
            
    except AccountNotFoundError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error retrieving transaction history: {e}")


def view_failed_transactions(bank: Bank):
    """View failed transactions."""
    print_header("❌ FAILED TRANSACTIONS")
    
    failed_transactions = bank.get_failed_transactions()
    
    if not failed_transactions:
        print("✅ No failed transactions!")
        return
    
    print(f"❌ Found {len(failed_transactions)} failed transaction(s):\n")
    for transaction in failed_transactions:
        timestamp = transaction.timestamp.strftime("%Y-%m-%d %H:%M")
        print(f"  {transaction.transaction_id}: {transaction.description}")
        print(f"    Account: {transaction.account_id}")
        print(f"    Amount: ${transaction.amount:.2f}")
        print(f"    Time: {timestamp}")
        print()


def view_statistics(bank: Bank):
    """View bank statistics."""
    print_header("📊 BANK STATISTICS")
    
    stats = bank.get_statistics()
    
    print(f"Total Accounts: {stats['total_accounts']}")
    print(f"Active Accounts: {stats['active_accounts']}")
    print(f"Total Transactions: {stats['total_transactions']}")
    print(f"\nTotal Deposits: ${stats['total_deposits']:.2f}")
    print(f"Total Withdrawals: ${stats['total_withdrawals']:.2f}")
    print(f"Net Flow: ${stats['total_deposits'] - stats['total_withdrawals']:.2f}")


def load_sample_data(bank: Bank):
    """Load sample data for testing."""
    try:
        # Create sample accounts
        alice_id = bank.create_account("Alice Johnson", 1000.00)
        bob_id = bank.create_account("Bob Smith", 500.00)
        charlie_id = bank.create_account("Charlie Brown", 250.00)
        
        # Perform sample transactions
        bank.deposit(alice_id, 200.00, "Salary deposit")
        bank.withdraw(alice_id, 150.00, "ATM withdrawal")
        bank.transfer(alice_id, bob_id, 300.00, "Money transfer")
        bank.deposit(charlie_id, 100.00, "Gift")
        
        print("✅ Sample data loaded successfully!")
        print(f"   • Created 3 accounts")
        print(f"   • Performed 4 transactions")
        
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bank_system.log'),
            logging.StreamHandler()
        ]
    )
    
    bank = Bank("SecureBank")
    
    print("=" * 70)
    print(f"🏦  {bank.name.upper()} SYSTEM  🏦".center(70))
    print("=" * 70)
    print("Robust banking system with comprehensive error handling!")
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            create_account_interactive(bank)
        elif choice == '2':
            check_balance_interactive(bank)
        elif choice == '3':
            deposit_interactive(bank)
        elif choice == '4':
            withdraw_interactive(bank)
        elif choice == '5':
            transfer_interactive(bank)
        elif choice == '6':
            view_transaction_history_interactive(bank)
        elif choice == '7':
            view_failed_transactions(bank)
        elif choice == '8':
            view_statistics(bank)
        elif choice == '9':
            load_sample_data(bank)
        elif choice == '10':
            print("\n👋 Thank you for using the Bank Account System!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
