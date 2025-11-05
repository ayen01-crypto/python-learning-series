"""
Tests for Field Definitions
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orm.fields import CharField, IntegerField, FloatField, BooleanField, EmailField
from orm.exceptions import ValidationError


class TestCharField(unittest.TestCase):
    """Test CharField functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.field = CharField(max_length=100, min_length=5)

    def test_valid_value(self):
        """Test valid string value."""
        value = "Hello World"
        result = self.field.validate(value)
        self.assertEqual(result, value)

    def test_too_short(self):
        """Test value that's too short."""
        with self.assertRaises(ValidationError):
            self.field.validate("Hi")

    def test_too_long(self):
        """Test value that's too long."""
        with self.assertRaises(ValidationError):
            self.field.validate("A" * 150)

    def test_none_value(self):
        """Test None value."""
        field = CharField(required=False)
        result = field.validate(None)
        self.assertIsNone(result)


class TestIntegerField(unittest.TestCase):
    """Test IntegerField functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.field = IntegerField(min_value=0, max_value=100)

    def test_valid_value(self):
        """Test valid integer value."""
        result = self.field.validate(50)
        self.assertEqual(result, 50)

    def test_string_conversion(self):
        """Test string to integer conversion."""
        result = self.field.validate("25")
        self.assertEqual(result, 25)

    def test_below_minimum(self):
        """Test value below minimum."""
        with self.assertRaises(ValidationError):
            self.field.validate(-1)

    def test_above_maximum(self):
        """Test value above maximum."""
        with self.assertRaises(ValidationError):
            self.field.validate(101)


class TestFloatField(unittest.TestCase):
    """Test FloatField functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.field = FloatField(min_value=0.0, max_value=100.0)

    def test_valid_value(self):
        """Test valid float value."""
        result = self.field.validate(50.5)
        self.assertEqual(result, 50.5)

    def test_integer_conversion(self):
        """Test integer to float conversion."""
        result = self.field.validate(25)
        self.assertEqual(result, 25.0)

    def test_string_conversion(self):
        """Test string to float conversion."""
        result = self.field.validate("33.33")
        self.assertEqual(result, 33.33)


class TestBooleanField(unittest.TestCase):
    """Test BooleanField functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.field = BooleanField()

    def test_true_values(self):
        """Test values that should be True."""
        true_values = [True, "true", "1", "yes", "on", 1]
        for value in true_values:
            result = self.field.validate(value)
            self.assertTrue(result)

    def test_false_values(self):
        """Test values that should be False."""
        false_values = [False, "false", "0", "no", "off", 0, None]
        for value in false_values:
            result = self.field.validate(value)
            self.assertFalse(result)


class TestEmailField(unittest.TestCase):
    """Test EmailField functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.field = EmailField()

    def test_valid_email(self):
        """Test valid email address."""
        email = "test@example.com"
        result = self.field.validate(email)
        self.assertEqual(result, email)

    def test_invalid_email(self):
        """Test invalid email address."""
        invalid_emails = ["invalid", "test@", "@example.com", "test@.com"]
        for email in invalid_emails:
            with self.assertRaises(ValidationError):
                self.field.validate(email)


if __name__ == '__main__':
    unittest.main()