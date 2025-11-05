"""
Mini Project: Library Management System

A comprehensive Object-Oriented Programming system to manage a library.
Demonstrates classes, inheritance, encapsulation, and polymorphism.

Features:
- Book management (add, remove, search)
- Member management (register, view)
- Borrowing and returning books
- Fine calculation for late returns
- Different member types (Student, Faculty, Regular)
"""

from datetime import datetime, timedelta
from typing import List, Optional
from abc import ABC, abstractmethod


# ============================================
# Base Classes
# ============================================

class LibraryItem(ABC):
    """Abstract base class for all library items."""
    
    def __init__(self, item_id: str, title: str, author: str):
        self._item_id = item_id
        self._title = title
        self._author = author
        self._is_available = True
        self._borrowed_by: Optional['Member'] = None
        self._due_date: Optional[datetime] = None
    
    @property
    def item_id(self) -> str:
        return self._item_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def author(self) -> str:
        return self._author
    
    @property
    def is_available(self) -> bool:
        return self._is_available
    
    @abstractmethod
    def get_borrow_period(self) -> int:
        """Return the borrowing period in days."""
        pass
    
    @abstractmethod
    def get_info(self) -> str:
        """Return formatted item information."""
        pass
    
    def borrow(self, member: 'Member') -> bool:
        """Borrow the item."""
        if self._is_available:
            self._is_available = False
            self._borrowed_by = member
            self._due_date = datetime.now() + timedelta(days=self.get_borrow_period())
            return True
        return False
    
    def return_item(self) -> int:
        """Return the item and calculate fine if late."""
        if not self._is_available and self._due_date:
            days_late = (datetime.now() - self._due_date).days
            fine = max(0, days_late * 2)  # $2 per day late
            
            self._is_available = True
            self._borrowed_by = None
            self._due_date = None
            
            return fine
        return 0
    
    def __str__(self) -> str:
        status = "✓ Available" if self._is_available else "✗ Borrowed"
        return f"[{self._item_id}] {self._title} by {self._author} - {status}"


class Book(LibraryItem):
    """Book class - specific type of library item."""
    
    def __init__(self, item_id: str, title: str, author: str, isbn: str, genre: str):
        super().__init__(item_id, title, author)
        self.isbn = isbn
        self.genre = genre
    
    def get_borrow_period(self) -> int:
        """Books can be borrowed for 14 days."""
        return 14
    
    def get_info(self) -> str:
        """Get detailed book information."""
        status = "Available" if self._is_available else f"Due: {self._due_date.strftime('%Y-%m-%d')}"
        return f"""
📚 BOOK DETAILS
{'='*50}
ID:       {self._item_id}
Title:    {self._title}
Author:   {self._author}
ISBN:     {self.isbn}
Genre:    {self.genre}
Status:   {status}
"""


class Magazine(LibraryItem):
    """Magazine class - different borrowing rules."""
    
    def __init__(self, item_id: str, title: str, publisher: str, issue: str):
        super().__init__(item_id, title, publisher)
        self.issue = issue
    
    def get_borrow_period(self) -> int:
        """Magazines can be borrowed for 7 days."""
        return 7
    
    def get_info(self) -> str:
        """Get detailed magazine information."""
        status = "Available" if self._is_available else f"Due: {self._due_date.strftime('%Y-%m-%d')}"
        return f"""
📰 MAGAZINE DETAILS
{'='*50}
ID:        {self._item_id}
Title:     {self._title}
Publisher: {self._author}
Issue:     {self.issue}
Status:    {status}
"""


# ============================================
# Member Classes
# ============================================

class Member(ABC):
    """Abstract base class for library members."""
    
    def __init__(self, member_id: str, name: str, email: str):
        self._member_id = member_id
        self._name = name
        self._email = email
        self._borrowed_items: List[LibraryItem] = []
        self._total_fines = 0.0
        self._registration_date = datetime.now()
    
    @property
    def member_id(self) -> str:
        return self._member_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def borrowed_items(self) -> List[LibraryItem]:
        return self._borrowed_items
    
    @property
    def total_fines(self) -> float:
        return self._total_fines
    
    @abstractmethod
    def get_borrow_limit(self) -> int:
        """Return maximum number of items that can be borrowed."""
        pass
    
    @abstractmethod
    def get_member_type(self) -> str:
        """Return the member type."""
        pass
    
    def can_borrow(self) -> bool:
        """Check if member can borrow more items."""
        return len(self._borrowed_items) < self.get_borrow_limit()
    
    def borrow_item(self, item: LibraryItem) -> bool:
        """Borrow an item."""
        if self.can_borrow() and item.borrow(self):
            self._borrowed_items.append(item)
            return True
        return False
    
    def return_item(self, item: LibraryItem) -> int:
        """Return an item and pay fine if applicable."""
        if item in self._borrowed_items:
            fine = item.return_item()
            self._borrowed_items.remove(item)
            self._total_fines += fine
            return fine
        return 0
    
    def __str__(self) -> str:
        return f"{self.get_member_type()} - {self._name} ({self._member_id})"


class StudentMember(Member):
    """Student member with limited borrowing privileges."""
    
    def __init__(self, member_id: str, name: str, email: str, student_id: str):
        super().__init__(member_id, name, email)
        self.student_id = student_id
    
    def get_borrow_limit(self) -> int:
        return 3  # Students can borrow up to 3 items
    
    def get_member_type(self) -> str:
        return "🎓 Student"


class FacultyMember(Member):
    """Faculty member with extended privileges."""
    
    def __init__(self, member_id: str, name: str, email: str, department: str):
        super().__init__(member_id, name, email)
        self.department = department
    
    def get_borrow_limit(self) -> int:
        return 10  # Faculty can borrow up to 10 items
    
    def get_member_type(self) -> str:
        return "👨‍🏫 Faculty"


class RegularMember(Member):
    """Regular member with standard privileges."""
    
    def get_borrow_limit(self) -> int:
        return 5  # Regular members can borrow up to 5 items
    
    def get_member_type(self) -> str:
        return "👤 Regular"


# ============================================
# Library System
# ============================================

class Library:
    """Main library system managing all operations."""
    
    def __init__(self, name: str):
        self.name = name
        self._items: dict[str, LibraryItem] = {}
        self._members: dict[str, Member] = {}
        self._transaction_log: List[str] = []
    
    def add_item(self, item: LibraryItem) -> bool:
        """Add an item to the library."""
        if item.item_id not in self._items:
            self._items[item.item_id] = item
            self._log(f"Added item: {item.title}")
            return True
        return False
    
    def remove_item(self, item_id: str) -> bool:
        """Remove an item from the library."""
        if item_id in self._items:
            item = self._items[item_id]
            if item.is_available:
                del self._items[item_id]
                self._log(f"Removed item: {item.title}")
                return True
        return False
    
    def register_member(self, member: Member) -> bool:
        """Register a new member."""
        if member.member_id not in self._members:
            self._members[member.member_id] = member
            self._log(f"Registered member: {member.name}")
            return True
        return False
    
    def find_item(self, item_id: str) -> Optional[LibraryItem]:
        """Find an item by ID."""
        return self._items.get(item_id)
    
    def find_member(self, member_id: str) -> Optional[Member]:
        """Find a member by ID."""
        return self._members.get(member_id)
    
    def search_items(self, query: str) -> List[LibraryItem]:
        """Search items by title or author."""
        query_lower = query.lower()
        results = []
        for item in self._items.values():
            if query_lower in item.title.lower() or query_lower in item.author.lower():
                results.append(item)
        return results
    
    def borrow_item(self, member_id: str, item_id: str) -> tuple[bool, str]:
        """Process borrowing transaction."""
        member = self.find_member(member_id)
        item = self.find_item(item_id)
        
        if not member:
            return False, "Member not found!"
        
        if not item:
            return False, "Item not found!"
        
        if not item.is_available:
            return False, "Item is currently borrowed!"
        
        if not member.can_borrow():
            return False, f"Borrow limit reached ({member.get_borrow_limit()} items)!"
        
        if member.borrow_item(item):
            self._log(f"{member.name} borrowed {item.title}")
            return True, f"✅ Successfully borrowed: {item.title}"
        
        return False, "Borrowing failed!"
    
    def return_item(self, member_id: str, item_id: str) -> tuple[bool, str]:
        """Process return transaction."""
        member = self.find_member(member_id)
        item = self.find_item(item_id)
        
        if not member or not item:
            return False, "Member or item not found!"
        
        fine = member.return_item(item)
        
        if fine > 0:
            self._log(f"{member.name} returned {item.title} (Fine: ${fine})")
            return True, f"✅ Returned: {item.title}\n⚠️  Late fee: ${fine}"
        else:
            self._log(f"{member.name} returned {item.title}")
            return True, f"✅ Returned: {item.title}"
    
    def get_available_items(self) -> List[LibraryItem]:
        """Get all available items."""
        return [item for item in self._items.values() if item.is_available]
    
    def get_borrowed_items(self) -> List[LibraryItem]:
        """Get all borrowed items."""
        return [item for item in self._items.values() if not item.is_available]
    
    def get_statistics(self) -> dict:
        """Get library statistics."""
        total_items = len(self._items)
        available = len(self.get_available_items())
        borrowed = total_items - available
        
        return {
            "total_items": total_items,
            "available_items": available,
            "borrowed_items": borrowed,
            "total_members": len(self._members),
            "total_transactions": len(self._transaction_log)
        }
    
    def _log(self, message: str):
        """Log a transaction."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._transaction_log.append(f"[{timestamp}] {message}")


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
    print("1.  Add Book")
    print("2.  Add Magazine")
    print("3.  Register Member")
    print("4.  Borrow Item")
    print("5.  Return Item")
    print("6.  Search Items")
    print("7.  View All Items")
    print("8.  View Available Items")
    print("9.  View Member Info")
    print("10. View All Members")
    print("11. Library Statistics")
    print("12. Load Sample Data")
    print("13. Exit")


def add_book_interactive(library: Library):
    """Interactive book addition."""
    print_header("📚 ADD NEW BOOK")
    
    item_id = input("Book ID: ").strip()
    if library.find_item(item_id):
        print("❌ Book ID already exists!")
        return
    
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    isbn = input("ISBN: ").strip()
    genre = input("Genre: ").strip()
    
    book = Book(item_id, title, author, isbn, genre)
    if library.add_item(book):
        print(f"✅ Book '{title}' added successfully!")
    else:
        print("❌ Failed to add book!")


def add_magazine_interactive(library: Library):
    """Interactive magazine addition."""
    print_header("📰 ADD NEW MAGAZINE")
    
    item_id = input("Magazine ID: ").strip()
    if library.find_item(item_id):
        print("❌ Magazine ID already exists!")
        return
    
    title = input("Title: ").strip()
    publisher = input("Publisher: ").strip()
    issue = input("Issue: ").strip()
    
    magazine = Magazine(item_id, title, publisher, issue)
    if library.add_item(magazine):
        print(f"✅ Magazine '{title}' added successfully!")
    else:
        print("❌ Failed to add magazine!")


def register_member_interactive(library: Library):
    """Interactive member registration."""
    print_header("👤 REGISTER NEW MEMBER")
    
    member_id = input("Member ID: ").strip()
    if library.find_member(member_id):
        print("❌ Member ID already exists!")
        return
    
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    
    print("\nMember Types:")
    print("1. Student")
    print("2. Faculty")
    print("3. Regular")
    
    choice = input("Select type: ").strip()
    
    member: Optional[Member] = None
    
    if choice == '1':
        student_id = input("Student ID: ").strip()
        member = StudentMember(member_id, name, email, student_id)
    elif choice == '2':
        department = input("Department: ").strip()
        member = FacultyMember(member_id, name, email, department)
    elif choice == '3':
        member = RegularMember(member_id, name, email)
    else:
        print("❌ Invalid choice!")
        return
    
    if member and library.register_member(member):
        print(f"✅ Member '{name}' registered successfully!")
    else:
        print("❌ Failed to register member!")


def borrow_item_interactive(library: Library):
    """Interactive borrowing."""
    print_header("📤 BORROW ITEM")
    
    member_id = input("Member ID: ").strip()
    item_id = input("Item ID: ").strip()
    
    success, message = library.borrow_item(member_id, item_id)
    print(message)


def return_item_interactive(library: Library):
    """Interactive returning."""
    print_header("📥 RETURN ITEM")
    
    member_id = input("Member ID: ").strip()
    item_id = input("Item ID: ").strip()
    
    success, message = library.return_item(member_id, item_id)
    print(message)


def search_items_interactive(library: Library):
    """Interactive item search."""
    print_header("🔍 SEARCH ITEMS")
    
    query = input("Search (title or author): ").strip()
    results = library.search_items(query)
    
    if results:
        print(f"\n✅ Found {len(results)} item(s):\n")
        for item in results:
            print(f"  {item}")
    else:
        print("❌ No items found!")


def view_all_items(library: Library):
    """View all library items."""
    print_header("📚 ALL LIBRARY ITEMS")
    
    items = list(library._items.values())
    if not items:
        print("❌ No items in library!")
        return
    
    for item in items:
        print(item)


def view_available_items(library: Library):
    """View available items."""
    print_header("✓ AVAILABLE ITEMS")
    
    items = library.get_available_items()
    if not items:
        print("❌ No available items!")
        return
    
    for item in items:
        print(item)


def view_member_info(library: Library):
    """View member information."""
    print_header("👤 MEMBER INFORMATION")
    
    member_id = input("Member ID: ").strip()
    member = library.find_member(member_id)
    
    if not member:
        print("❌ Member not found!")
        return
    
    print(f"\n{member}")
    print(f"Email: {member.email}")
    print(f"Borrow Limit: {member.get_borrow_limit()}")
    print(f"Currently Borrowed: {len(member.borrowed_items)}")
    print(f"Total Fines: ${member.total_fines:.2f}")
    
    if member.borrowed_items:
        print("\nBorrowed Items:")
        for item in member.borrowed_items:
            print(f"  • {item.title}")


def view_all_members(library: Library):
    """View all members."""
    print_header("👥 ALL MEMBERS")
    
    members = list(library._members.values())
    if not members:
        print("❌ No members registered!")
        return
    
    print(f"{'ID':<12} {'NAME':<20} {'TYPE':<15} {'BORROWED':<10} {'FINES'}")
    print("-" * 70)
    
    for member in members:
        borrowed_count = len(member.borrowed_items)
        print(f"{member.member_id:<12} {member.name:<20} {member.get_member_type():<15} "
              f"{borrowed_count:<10} ${member.total_fines:.2f}")


def view_statistics(library: Library):
    """View library statistics."""
    print_header("📊 LIBRARY STATISTICS")
    
    stats = library.get_statistics()
    
    print(f"Total Items: {stats['total_items']}")
    print(f"  • Available: {stats['available_items']}")
    print(f"  • Borrowed: {stats['borrowed_items']}")
    print(f"\nTotal Members: {stats['total_members']}")
    print(f"Total Transactions: {stats['total_transactions']}")


def load_sample_data(library: Library):
    """Load sample data for testing."""
    # Add books
    books = [
        Book("B001", "Python Programming", "John Smith", "978-1234567890", "Technology"),
        Book("B002", "Data Science Basics", "Jane Doe", "978-0987654321", "Technology"),
        Book("B003", "The Great Novel", "Alice Johnson", "978-1111111111", "Fiction"),
        Book("B004", "History of Computing", "Bob Wilson", "978-2222222222", "History"),
    ]
    
    for book in books:
        library.add_item(book)
    
    # Add magazines
    magazines = [
        Magazine("M001", "Tech Monthly", "Tech Publishers", "2024-01"),
        Magazine("M002", "Science Today", "Science Press", "Vol 45"),
    ]
    
    for magazine in magazines:
        library.add_item(magazine)
    
    # Add members
    members = [
        StudentMember("S001", "Emma Watson", "emma@university.edu", "STU12345"),
        FacultyMember("F001", "Prof. Alan Turing", "turing@university.edu", "Computer Science"),
        RegularMember("R001", "John Public", "john@email.com"),
    ]
    
    for member in members:
        library.register_member(member)
    
    print("✅ Sample data loaded successfully!")
    print("   • 4 books, 2 magazines")
    print("   • 3 members (1 student, 1 faculty, 1 regular)")


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    library = Library("City Public Library")
    
    print("=" * 70)
    print(f"📚  {library.name.upper()}  📚".center(70))
    print("=" * 70)
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            add_book_interactive(library)
        elif choice == '2':
            add_magazine_interactive(library)
        elif choice == '3':
            register_member_interactive(library)
        elif choice == '4':
            borrow_item_interactive(library)
        elif choice == '5':
            return_item_interactive(library)
        elif choice == '6':
            search_items_interactive(library)
        elif choice == '7':
            view_all_items(library)
        elif choice == '8':
            view_available_items(library)
        elif choice == '9':
            view_member_info(library)
        elif choice == '10':
            view_all_members(library)
        elif choice == '11':
            view_statistics(library)
        elif choice == '12':
            load_sample_data(library)
        elif choice == '13':
            print("\n👋 Thank you for using the Library Management System!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
