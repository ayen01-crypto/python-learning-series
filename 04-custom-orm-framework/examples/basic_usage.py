"""
Basic Usage Example
This script demonstrates basic usage of the custom ORM framework.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orm import Model, fields
from orm.database import Database


# Define a simple model
class User(Model):
    name = fields.CharField(max_length=100)
    email = fields.EmailField(unique=True)
    age = fields.IntegerField(min_value=0)
    is_active = fields.BooleanField(default=True)
    
    class Meta:
        table_name = 'users'


# Define another model with relationship
class Post(Model):
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    author = fields.ForeignKey('User')
    created_at = fields.DateTimeField()
    
    class Meta:
        table_name = 'posts'


def main():
    """Main function to demonstrate ORM usage."""
    print("Custom ORM Framework Demo")
    print("=" * 30)
    
    # Initialize database
    db = Database('sqlite:///example.db')
    db.connect()
    
    # Set database for models
    User.set_database(db)
    Post.set_database(db)
    
    # Create tables
    print("1. Creating tables...")
    db.create_tables([User, Post])
    print("   Tables created successfully")
    
    # Create users
    print("\n2. Creating users...")
    alice = User.objects.create(name='Alice', email='alice@example.com', age=25)
    bob = User.objects.create(name='Bob', email='bob@example.com', age=30)
    charlie = User.objects.create(name='Charlie', email='charlie@example.com', age=35)
    print(f"   Created users: {alice.name}, {bob.name}, {charlie.name}")
    
    # Query all users
    print("\n3. Querying all users...")
    all_users = User.objects.all()
    for user in all_users:
        print(f"   - {user.name} ({user.email}), age {user.age}")
    
    # Filter users
    print("\n4. Filtering users...")
    adults = User.objects.filter(age__gte=30)
    print(f"   Users aged 30 or older:")
    for user in adults:
        print(f"   - {user.name}, age {user.age}")
    
    # Get a specific user
    print("\n5. Getting specific user...")
    try:
        user = User.objects.get(email='alice@example.com')
        print(f"   Found user: {user.name}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Update a user
    print("\n6. Updating user...")
    user = User.objects.get(name='Alice')
    user.age = 26
    user.save()
    print(f"   Updated {user.name}'s age to {user.age}")
    
    # Create posts
    print("\n7. Creating posts...")
    post1 = Post.objects.create(
        title='Hello World',
        content='This is my first post!',
        author=user.id,
        created_at='2023-01-01 12:00:00'
    )
    print(f"   Created post: {post1.title}")
    
    # Query posts with filtering
    print("\n8. Querying posts...")
    posts = Post.objects.filter(author=user.id)
    for post in posts:
        print(f"   - {post.title} by user {post.author}")
    
    # Count records
    print("\n9. Counting records...")
    user_count = User.objects.count()
    post_count = Post.objects.count()
    print(f"   Users: {user_count}")
    print(f"   Posts: {post_count}")
    
    # Delete a user
    print("\n10. Deleting a user...")
    charlie = User.objects.get(name='Charlie')
    charlie.delete()
    remaining_users = User.objects.count()
    print(f"   Deleted Charlie. Remaining users: {remaining_users}")
    
    # Close database connection
    db.disconnect()
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    main()