"""
Tests for Base Model
"""

import unittest
import sys
import os
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orm import Model, fields
from orm.database import Database


class TestModel(Model):
    """Test model for testing purposes."""
    name = fields.CharField(max_length=100)
    age = fields.IntegerField(min_value=0)
    email = fields.EmailField(unique=True)
    
    class Meta:
        table_name = 'test_model'


class TestModelBase(unittest.TestCase):
    """Test base model functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary database
        self.db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db_file.close()
        
        self.db = Database(f'sqlite:///{self.db_file.name}')
        self.db.connect()
        
        # Set database for model
        TestModel.set_database(self.db)
        
        # Create table
        self.db.create_table(TestModel)

    def tearDown(self):
        """Tear down test fixtures."""
        self.db.disconnect()
        os.unlink(self.db_file.name)

    def test_model_creation(self):
        """Test creating a model instance."""
        instance = TestModel(name="Alice", age=25, email="alice@example.com")
        self.assertEqual(instance.name, "Alice")
        self.assertEqual(instance.age, 25)
        self.assertEqual(instance.email, "alice@example.com")

    def test_model_field_validation(self):
        """Test model field validation."""
        # Valid instance
        instance = TestModel(name="Bob", age=30, email="bob@example.com")
        instance.full_clean()  # Should not raise exception
        
        # Invalid age
        instance = TestModel(name="Charlie", age=-5, email="charlie@example.com")
        with self.assertRaises(Exception):
            instance.full_clean()

    def test_model_save(self):
        """Test saving a model instance."""
        instance = TestModel(name="David", age=35, email="david@example.com")
        instance.save()
        
        # Check that instance is saved
        self.assertTrue(instance._is_saved)
        
        # Retrieve instance from database
        retrieved = TestModel.objects.get(email="david@example.com")
        self.assertEqual(retrieved.name, "David")
        self.assertEqual(retrieved.age, 35)

    def test_model_update(self):
        """Test updating a model instance."""
        # Create instance
        instance = TestModel(name="Eve", age=28, email="eve@example.com")
        instance.save()
        
        # Update instance
        instance.age = 29
        instance.save()
        
        # Retrieve updated instance
        retrieved = TestModel.objects.get(email="eve@example.com")
        self.assertEqual(retrieved.age, 29)

    def test_model_delete(self):
        """Test deleting a model instance."""
        # Create instance
        instance = TestModel(name="Frank", age=40, email="frank@example.com")
        instance.save()
        
        # Delete instance
        instance.delete()
        
        # Check that instance is deleted
        self.assertFalse(instance._is_saved)
        
        # Try to retrieve deleted instance
        with self.assertRaises(Exception):
            TestModel.objects.get(email="frank@example.com")

    def test_model_to_dict(self):
        """Test converting model to dictionary."""
        instance = TestModel(name="Grace", age=32, email="grace@example.com")
        data = instance.to_dict()
        
        self.assertEqual(data['name'], "Grace")
        self.assertEqual(data['age'], 32)
        self.assertEqual(data['email'], "grace@example.com")


if __name__ == '__main__':
    unittest.main()