"""
Mini Project: Contact Manager

A comprehensive contact management system with file persistence.
Demonstrates file I/O, JSON handling, and data persistence.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


# ============================================
# Contact Class
# ============================================

class Contact:
    """Represents a contact with personal information."""
    
    def __init__(self, contact_id: str, name: str, phone: str, email: str, 
                 address: str = "", notes: str = ""):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.notes = notes
        self.created_date = datetime.now().isoformat()
        self.last_modified = self.created_date
    
    def update(self, **kwargs):
        """Update contact fields."""
        for key, value in kwargs.items():
            if hasattr(self, key) and key != 'contact_id':
                setattr(self, key, value)
        self.last_modified = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert contact to dictionary."""
        return {
            'contact_id': self.contact_id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'notes': self.notes,
            'created_date': self.created_date,
            'last_modified': self.last_modified
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        """Create contact from dictionary."""
        contact = cls(
            data['contact_id'],
            data['name'],
            data['phone'],
            data['email'],
            data.get('address', ''),
            data.get('notes', '')
        )
        contact.created_date = data.get('created_date', contact.created_date)
        contact.last_modified = data.get('last_modified', contact.last_modified)
        return contact
    
    def __str__(self) -> str:
        return f"[{self.contact_id}] {self.name} - {self.phone}"


# ============================================
# Contact Manager
# ============================================

class ContactManager:
    """Manages contacts with file persistence."""
    
    def __init__(self, data_file: str = "contacts.json"):
        self.data_file = data_file
        self.contacts: Dict[str, Contact] = {}
        self.load_contacts()
    
    def add_contact(self, name: str, phone: str, email: str, 
                   address: str = "", notes: str = "") -> str:
        """Add a new contact."""
        # Generate unique ID
        contact_id = self._generate_id()
        
        # Create contact
        contact = Contact(contact_id, name, phone, email, address, notes)
        self.contacts[contact_id] = contact
        
        # Save to file
        self.save_contacts()
        
        return contact_id
    
    def update_contact(self, contact_id: str, **kwargs) -> bool:
        """Update an existing contact."""
        if contact_id in self.contacts:
            self.contacts[contact_id].update(**kwargs)
            self.save_contacts()
            return True
        return False
    
    def delete_contact(self, contact_id: str) -> bool:
        """Delete a contact."""
        if contact_id in self.contacts:
            del self.contacts[contact_id]
            self.save_contacts()
            return True
        return False
    
    def get_contact(self, contact_id: str) -> Optional[Contact]:
        """Get a contact by ID."""
        return self.contacts.get(contact_id)
    
    def search_contacts(self, query: str) -> List[Contact]:
        """Search contacts by name, phone, or email."""
        query_lower = query.lower()
        results = []
        
        for contact in self.contacts.values():
            if (query_lower in contact.name.lower() or 
                query_lower in contact.phone.lower() or 
                query_lower in contact.email.lower() or
                query_lower in contact.address.lower()):
                results.append(contact)
        
        return results
    
    def list_contacts(self) -> List[Contact]:
        """Get all contacts."""
        return list(self.contacts.values())
    
    def save_contacts(self):
        """Save contacts to file."""
        try:
            data = {cid: contact.to_dict() for cid, contact in self.contacts.items()}
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=2)
        except Exception as e:
            print(f"❌ Error saving contacts: {e}")
    
    def load_contacts(self):
        """Load contacts from file."""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.contacts = {cid: Contact.from_dict(contact_data) 
                               for cid, contact_data in data.items()}
        except Exception as e:
            print(f"❌ Error loading contacts: {e}")
            self.contacts = {}
    
    def export_contacts(self, filename: str) -> bool:
        """Export contacts to CSV file."""
        try:
            import csv
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                # Header
                writer.writerow(['ID', 'Name', 'Phone', 'Email', 'Address', 'Notes'])
                # Data
                for contact in self.contacts.values():
                    writer.writerow([
                        contact.contact_id,
                        contact.name,
                        contact.phone,
                        contact.email,
                        contact.address,
                        contact.notes
                    ])
            return True
        except Exception as e:
            print(f"❌ Error exporting contacts: {e}")
            return False
    
    def import_contacts(self, filename: str) -> int:
        """Import contacts from CSV file."""
        try:
            import csv
            count = 0
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Skip if contact ID already exists
                    if row['ID'] in self.contacts:
                        continue
                    
                    contact = Contact(
                        row['ID'],
                        row['Name'],
                        row['Phone'],
                        row['Email'],
                        row['Address'],
                        row['Notes']
                    )
                    self.contacts[contact.contact_id] = contact
                    count += 1
            
            self.save_contacts()
            return count
        except Exception as e:
            print(f"❌ Error importing contacts: {e}")
            return 0
    
    def get_statistics(self) -> Dict:
        """Get contact statistics."""
        total = len(self.contacts)
        if total == 0:
            return {"total": 0}
        
        # Count contacts by domain
        domains = {}
        for contact in self.contacts.values():
            if '@' in contact.email:
                domain = contact.email.split('@')[1]
                domains[domain] = domains.get(domain, 0) + 1
        
        return {
            "total": total,
            "domains": domains,
            "top_domain": max(domains.items(), key=lambda x: x[1]) if domains else None
        }
    
    def _generate_id(self) -> str:
        """Generate a unique contact ID."""
        import uuid
        return str(uuid.uuid4())[:8]


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
    print("1.  Add Contact")
    print("2.  View Contact")
    print("3.  Edit Contact")
    print("4.  Delete Contact")
    print("5.  Search Contacts")
    print("6.  List All Contacts")
    print("7.  Import Contacts (CSV)")
    print("8.  Export Contacts (CSV)")
    print("9.  View Statistics")
    print("10. Load Sample Data")
    print("11. Exit")


def add_contact_interactive(manager: ContactManager):
    """Interactive contact addition."""
    print_header("➕ ADD NEW CONTACT")
    
    name = input("Name: ").strip()
    if not name:
        print("❌ Name is required!")
        return
    
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    address = input("Address (optional): ").strip()
    notes = input("Notes (optional): ").strip()
    
    contact_id = manager.add_contact(name, phone, email, address, notes)
    print(f"✅ Contact '{name}' added successfully! (ID: {contact_id})")


def view_contact_interactive(manager: ContactManager):
    """Interactive contact viewing."""
    print_header("👁️  VIEW CONTACT")
    
    contact_id = input("Contact ID: ").strip()
    contact = manager.get_contact(contact_id)
    
    if not contact:
        print("❌ Contact not found!")
        return
    
    print(f"\n🆔 ID: {contact.contact_id}")
    print(f"👤 Name: {contact.name}")
    print(f"📞 Phone: {contact.phone}")
    print(f"📧 Email: {contact.email}")
    print(f"🏠 Address: {contact.address}")
    print(f"📝 Notes: {contact.notes}")
    print(f"📅 Created: {contact.created_date}")
    print(f"🔄 Modified: {contact.last_modified}")


def edit_contact_interactive(manager: ContactManager):
    """Interactive contact editing."""
    print_header("✏️  EDIT CONTACT")
    
    contact_id = input("Contact ID: ").strip()
    contact = manager.get_contact(contact_id)
    
    if not contact:
        print("❌ Contact not found!")
        return
    
    print(f"\nEditing: {contact.name}")
    print("Leave blank to keep current value")
    
    name = input(f"Name ({contact.name}): ").strip()
    phone = input(f"Phone ({contact.phone}): ").strip()
    email = input(f"Email ({contact.email}): ").strip()
    address = input(f"Address ({contact.address}): ").strip()
    notes = input(f"Notes ({contact.notes}): ").strip()
    
    # Update only non-empty values
    updates = {}
    if name: updates['name'] = name
    if phone: updates['phone'] = phone
    if email: updates['email'] = email
    if address: updates['address'] = address
    if notes: updates['notes'] = notes
    
    if updates:
        if manager.update_contact(contact_id, **updates):
            print("✅ Contact updated successfully!")
        else:
            print("❌ Failed to update contact!")
    else:
        print("ℹ️  No changes made.")


def delete_contact_interactive(manager: ContactManager):
    """Interactive contact deletion."""
    print_header("🗑️  DELETE CONTACT")
    
    contact_id = input("Contact ID: ").strip()
    contact = manager.get_contact(contact_id)
    
    if not contact:
        print("❌ Contact not found!")
        return
    
    print(f"Deleting: {contact.name}")
    confirm = input("Are you sure? (y/N): ").strip().lower()
    
    if confirm == 'y':
        if manager.delete_contact(contact_id):
            print("✅ Contact deleted successfully!")
        else:
            print("❌ Failed to delete contact!")
    else:
        print("ℹ️  Deletion cancelled.")


def search_contacts_interactive(manager: ContactManager):
    """Interactive contact search."""
    print_header("🔍 SEARCH CONTACTS")
    
    query = input("Search (name, phone, email, address): ").strip()
    if not query:
        print("❌ Search query is required!")
        return
    
    results = manager.search_contacts(query)
    
    if not results:
        print("❌ No contacts found!")
        return
    
    print(f"\n✅ Found {len(results)} contact(s):\n")
    print(f"{'ID':<10} {'Name':<20} {'Phone':<15} {'Email'}")
    print("-" * 70)
    
    for contact in results:
        print(f"{contact.contact_id:<10} {contact.name:<20} {contact.phone:<15} {contact.email}")


def list_all_contacts(manager: ContactManager):
    """List all contacts."""
    print_header("📇 ALL CONTACTS")
    
    contacts = manager.list_contacts()
    
    if not contacts:
        print("❌ No contacts found!")
        return
    
    print(f"{'ID':<10} {'Name':<20} {'Phone':<15} {'Email'}")
    print("-" * 70)
    
    for contact in sorted(contacts, key=lambda c: c.name):
        print(f"{contact.contact_id:<10} {contact.name:<20} {contact.phone:<15} {contact.email}")


def import_contacts_interactive(manager: ContactManager):
    """Interactive contact import."""
    print_header("📥 IMPORT CONTACTS")
    
    filename = input("CSV filename: ").strip()
    if not filename:
        print("❌ Filename is required!")
        return
    
    if not os.path.exists(filename):
        print("❌ File not found!")
        return
    
    count = manager.import_contacts(filename)
    print(f"✅ Imported {count} contact(s)!")


def export_contacts_interactive(manager: ContactManager):
    """Interactive contact export."""
    print_header("📤 EXPORT CONTACTS")
    
    filename = input("CSV filename (default: contacts_export.csv): ").strip()
    if not filename:
        filename = "contacts_export.csv"
    
    if manager.export_contacts(filename):
        print(f"✅ Contacts exported to '{filename}'!")
    else:
        print("❌ Failed to export contacts!")


def view_statistics(manager: ContactManager):
    """View contact statistics."""
    print_header("📊 CONTACT STATISTICS")
    
    stats = manager.get_statistics()
    
    print(f"Total Contacts: {stats['total']}")
    
    if stats['total'] > 0:
        domains = stats['domains']
        if domains:
            print(f"\n📧 Email Domains:")
            for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {domain}: {count}")
            
            top_domain, count = stats['top_domain']
            print(f"\n🏆 Most Common Domain: {top_domain} ({count} contacts)")


def load_sample_data(manager: ContactManager):
    """Load sample contacts for testing."""
    sample_contacts = [
        ("Alice Johnson", "555-0101", "alice@email.com", "123 Main St", "Work colleague"),
        ("Bob Smith", "555-0102", "bob@gmail.com", "456 Oak Ave", "Friend from college"),
        ("Charlie Brown", "555-0103", "charlie@company.com", "789 Pine Rd", "Gym partner"),
        ("Diana Prince", "555-0104", "diana@university.edu", "321 Elm St", "Professor"),
        ("Ethan Hunt", "555-0105", "ethan@agency.gov", "654 Maple Dr", "Secret agent")
    ]
    
    added_count = 0
    for name, phone, email, address, notes in sample_contacts:
        contact_id = manager.add_contact(name, phone, email, address, notes)
        if contact_id:
            added_count += 1
    
    print(f"✅ Loaded {added_count} sample contacts!")


# ============================================
# Main Application
# ============================================

def main():
    """Main application loop."""
    manager = ContactManager()
    
    print("=" * 70)
    print("📇  CONTACT MANAGER  📇".center(70))
    print("=" * 70)
    print("Your personal contact management system!")
    
    while True:
        print_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            add_contact_interactive(manager)
        elif choice == '2':
            view_contact_interactive(manager)
        elif choice == '3':
            edit_contact_interactive(manager)
        elif choice == '4':
            delete_contact_interactive(manager)
        elif choice == '5':
            search_contacts_interactive(manager)
        elif choice == '6':
            list_all_contacts(manager)
        elif choice == '7':
            import_contacts_interactive(manager)
        elif choice == '8':
            export_contacts_interactive(manager)
        elif choice == '9':
            view_statistics(manager)
        elif choice == '10':
            load_sample_data(manager)
        elif choice == '11':
            print("\n👋 Thank you for using Contact Manager!")
            print("=" * 70 + "\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
