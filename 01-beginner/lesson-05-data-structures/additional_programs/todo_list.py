"""
To-Do List Program
This program demonstrates the use of lists, dictionaries, and tuples for managing a to-do list.
"""

def add_task(todo_list, task, priority="Medium", category="General"):
    """Add a new task to the to-do list."""
    todo_list.append({
        'task': task,
        'priority': priority,
        'category': category,
        'completed': False
    })

def remove_task(todo_list, task_index):
    """Remove a task from the to-do list by index."""
    if 0 <= task_index < len(todo_list):
        return todo_list.pop(task_index)
    else:
        return None

def mark_completed(todo_list, task_index):
    """Mark a task as completed."""
    if 0 <= task_index < len(todo_list):
        todo_list[task_index]['completed'] = True
        return True
    else:
        return False

def update_task(todo_list, task_index, task=None, priority=None, category=None):
    """Update task details."""
    if 0 <= task_index < len(todo_list):
        if task is not None:
            todo_list[task_index]['task'] = task
        if priority is not None:
            todo_list[task_index]['priority'] = priority
        if category is not None:
            todo_list[task_index]['category'] = category
        return True
    else:
        return False

def list_tasks(todo_list):
    """List all tasks in the to-do list."""
    if not todo_list:
        print("To-do list is empty.")
        return
    
    print("To-Do List:")
    print("=" * 50)
    for i, task_info in enumerate(todo_list):
        status = "✓" if task_info['completed'] else "○"
        print(f"{i+1}. [{status}] {task_info['task']}")
        print(f"   Priority: {task_info['priority']} | Category: {task_info['category']}")
        print()

def list_tasks_by_priority(todo_list, priority):
    """List tasks filtered by priority."""
    filtered_tasks = [task for task in todo_list if task['priority'] == priority]
    
    if not filtered_tasks:
        print(f"No tasks with {priority} priority.")
        return
    
    print(f"{priority} Priority Tasks:")
    print("=" * 30)
    for i, task_info in enumerate(filtered_tasks):
        status = "✓" if task_info['completed'] else "○"
        print(f"{i+1}. [{status}] {task_info['task']}")
        print(f"   Category: {task_info['category']}")
        print()

def list_tasks_by_category(todo_list, category):
    """List tasks filtered by category."""
    filtered_tasks = [task for task in todo_list if task['category'] == category]
    
    if not filtered_tasks:
        print(f"No tasks in {category} category.")
        return
    
    print(f"{category} Category Tasks:")
    print("=" * 30)
    for i, task_info in enumerate(filtered_tasks):
        status = "✓" if task_info['completed'] else "○"
        print(f"{i+1}. [{status}] {task_info['task']}")
        print(f"   Priority: {task_info['priority']}")
        print()

def get_task_statistics(todo_list):
    """Get statistics about the to-do list."""
    total_tasks = len(todo_list)
    completed_tasks = sum(1 for task in todo_list if task['completed'])
    pending_tasks = total_tasks - completed_tasks
    
    # Count by priority
    priority_counts = {}
    for task in todo_list:
        priority = task['priority']
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    # Count by category
    category_counts = {}
    for task in todo_list:
        category = task['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    return {
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'priority_counts': priority_counts,
        'category_counts': category_counts
    }

def main():
    """Main function to run the to-do list program."""
    print("To-Do List Manager")
    print("=" * 20)
    
    # Initialize to-do list
    todo_list = []
    
    # Add some initial tasks
    add_task(todo_list, "Complete Python basics tutorial", "High", "Learning")
    add_task(todo_list, "Buy groceries", "Medium", "Personal")
    add_task(todo_list, "Call dentist for appointment", "Low", "Health")
    add_task(todo_list, "Write project report", "High", "Work")
    add_task(todo_list, "Go for a run", "Medium", "Fitness")
    
    print("Initial to-do list created.")
    list_tasks(todo_list)
    
    # Demonstrate to-do list operations
    print("Performing to-do list operations...")
    
    # Mark a task as completed
    mark_completed(todo_list, 0)  # Mark first task as completed
    print("Marked 'Complete Python basics tutorial' as completed.")
    
    # Add a new task
    add_task(todo_list, "Read Python book Chapter 5", "Medium", "Learning")
    print("Added 'Read Python book Chapter 5' to the list.")
    
    # Update a task
    update_task(todo_list, 2, priority="High")  # Increase priority of "Call dentist"
    print("Increased priority of 'Call dentist for appointment' to High.")
    
    # Display updated to-do list
    print("\nUpdated To-Do List:")
    list_tasks(todo_list)
    
    # Show tasks by priority
    print("\nHigh Priority Tasks:")
    list_tasks_by_priority(todo_list, "High")
    
    # Show tasks by category
    print("\nLearning Category Tasks:")
    list_tasks_by_category(todo_list, "Learning")
    
    # Show statistics
    stats = get_task_statistics(todo_list)
    print("To-Do List Statistics:")
    print("=" * 25)
    print(f"Total tasks: {stats['total']}")
    print(f"Completed tasks: {stats['completed']}")
    print(f"Pending tasks: {stats['pending']}")
    print("\nTasks by Priority:")
    for priority, count in stats['priority_counts'].items():
        print(f"  {priority}: {count}")
    print("\nTasks by Category:")
    for category, count in stats['category_counts'].items():
        print(f"  {category}: {count}")
    
    # Interactive to-do list management
    print("\nInteractive To-Do List Management:")
    while True:
        print("\nChoose an operation:")
        print("1. Add task")
        print("2. Remove task")
        print("3. Mark task as completed")
        print("4. Update task")
        print("5. List all tasks")
        print("6. List tasks by priority")
        print("7. List tasks by category")
        print("8. Show statistics")
        print("9. Exit")
        
        choice = input("Enter choice (1-9): ")
        
        if choice == '9':
            break
            
        if choice == '1':
            task = input("Enter task description: ")
            priority = input("Enter priority (High/Medium/Low) [Medium]: ") or "Medium"
            category = input("Enter category [General]: ") or "General"
            add_task(todo_list, task, priority, category)
            print("Task added to to-do list.")
        elif choice == '2':
            list_tasks(todo_list)
            try:
                task_index = int(input("Enter task number to remove: ")) - 1
                removed_task = remove_task(todo_list, task_index)
                if removed_task:
                    print(f"Removed task: {removed_task['task']}")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '3':
            list_tasks(todo_list)
            try:
                task_index = int(input("Enter task number to mark as completed: ")) - 1
                if mark_completed(todo_list, task_index):
                    print("Task marked as completed.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '4':
            list_tasks(todo_list)
            try:
                task_index = int(input("Enter task number to update: ")) - 1
                if 0 <= task_index < len(todo_list):
                    task = input(f"Enter new task description [{todo_list[task_index]['task']}]: ") or None
                    priority = input(f"Enter new priority [{todo_list[task_index]['priority']}]: ") or None
                    category = input(f"Enter new category [{todo_list[task_index]['category']}]: ") or None
                    update_task(todo_list, task_index, task, priority, category)
                    print("Task updated.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '5':
            list_tasks(todo_list)
        elif choice == '6':
            priority = input("Enter priority (High/Medium/Low): ")
            list_tasks_by_priority(todo_list, priority)
        elif choice == '7':
            category = input("Enter category: ")
            list_tasks_by_category(todo_list, category)
        elif choice == '8':
            stats = get_task_statistics(todo_list)
            print("\nTo-Do List Statistics:")
            print("=" * 25)
            print(f"Total tasks: {stats['total']}")
            print(f"Completed tasks: {stats['completed']}")
            print(f"Pending tasks: {stats['pending']}")
            print("\nTasks by Priority:")
            for priority, count in stats['priority_counts'].items():
                print(f"  {priority}: {count}")
            print("\nTasks by Category:")
            for category, count in stats['category_counts'].items():
                print(f"  {category}: {count}")
        else:
            print("Invalid choice. Please enter 1-9.")

if __name__ == "__main__":
    main()