#!/usr/bin/env python3
"""
Note Taking Application
A simple note-taking app that demonstrates file I/O operations.
"""

import os
from datetime import datetime


def create_note():
    """Create a new note with a title and content."""
    title = input("Enter note title: ").strip()
    if not title:
        print("Title cannot be empty!")
        return
    
    content = input("Enter note content (press Enter twice to finish):\n")
    # Allow multiline input
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    content = "\n".join(lines)
    
    # Create filename based on title
    filename = f"{title.replace(' ', '_').lower()}.txt"
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Write note to file
    try:
        with open(filename, 'w') as file:
            file.write(f"Title: {title}\n")
            file.write(f"Created: {timestamp}\n")
            file.write("-" * 40 + "\n")
            file.write(content)
        print(f"Note '{title}' saved as {filename}")
    except Exception as e:
        print(f"Error saving note: {e}")


def view_notes():
    """List all available notes."""
    notes = [f for f in os.listdir('.') if f.endswith('.txt')]
    if not notes:
        print("No notes found.")
        return
    
    print("\nAvailable Notes:")
    print("-" * 30)
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note}")
    
    choice = input("\nEnter note number to view (or press Enter to cancel): ")
    if choice.isdigit() and 1 <= int(choice) <= len(notes):
        filename = notes[int(choice) - 1]
        try:
            with open(filename, 'r') as file:
                print("\n" + "=" * 50)
                print(file.read())
                print("=" * 50)
        except Exception as e:
            print(f"Error reading note: {e}")
    elif choice:
        print("Invalid selection.")


def search_notes():
    """Search for notes containing specific text."""
    search_term = input("Enter search term: ").lower()
    if not search_term:
        print("Search term cannot be empty!")
        return
    
    matching_notes = []
    notes = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    for note in notes:
        try:
            with open(note, 'r') as file:
                content = file.read().lower()
                if search_term in content:
                    matching_notes.append(note)
        except Exception as e:
            print(f"Error reading {note}: {e}")
    
    if matching_notes:
        print(f"\nFound {len(matching_notes)} note(s) containing '{search_term}':")
        print("-" * 40)
        for note in matching_notes:
            print(f"- {note}")
    else:
        print(f"No notes found containing '{search_term}'")


def delete_note():
    """Delete a note file."""
    notes = [f for f in os.listdir('.') if f.endswith('.txt')]
    if not notes:
        print("No notes found.")
        return
    
    print("\nAvailable Notes:")
    print("-" * 30)
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note}")
    
    choice = input("\nEnter note number to delete (or press Enter to cancel): ")
    if choice.isdigit() and 1 <= int(choice) <= len(notes):
        filename = notes[int(choice) - 1]
        confirm = input(f"Are you sure you want to delete '{filename}'? (y/N): ")
        if confirm.lower() == 'y':
            try:
                os.remove(filename)
                print(f"Note '{filename}' deleted successfully.")
            except Exception as e:
                print(f"Error deleting note: {e}")
        else:
            print("Deletion cancelled.")
    elif choice:
        print("Invalid selection.")


def main():
    """Main program loop."""
    print("📝 Welcome to Note Taking App!")
    print("This app demonstrates file I/O operations in Python.")
    
    while True:
        print("\n" + "=" * 40)
        print("📋 NOTE TAKING MENU")
        print("=" * 40)
        print("1. Create New Note")
        print("2. View Notes")
        print("3. Search Notes")
        print("4. Delete Note")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            create_note()
        elif choice == '2':
            view_notes()
        elif choice == '3':
            search_notes()
        elif choice == '4':
            delete_note()
        elif choice == '5':
            print("Thank you for using Note Taking App!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()