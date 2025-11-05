"""
Field Definitions
This module defines various field types for the ORM framework.
"""

import re
from typing import Any, Optional, Callable
from .exceptions import ValidationError


class Field:
    """Base class for all fields."""
    
    def __init__(self, required: bool = False, default: Any = None, 
                 validators: Optional[list] = None, unique: bool = False):
        self.required = required
        self.default = default
        self.validators = validators or []
        self.unique = unique
    
    def validate(self, value: Any) -> Any:
        """Validate the field value."""
        # Check if required
        if self.required and value is None:
            raise ValidationError("This field is required.")
        
        # Check if None and not required
        if value is None:
            return value
        
        # Run custom validators
        for validator in self.validators:
            if isinstance(validator, Callable):
                try:
                    validator(value)
                except Exception as e:
                    raise ValidationError(str(e))
        
        return value


class CharField(Field):
    """String field."""
    
    def __init__(self, max_length: int = 255, min_length: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length
        self.min_length = min_length
    
    def validate(self, value: Any) -> str:
        value = super().validate(value)
        
        if value is None:
            return value
        
        # Convert to string
        value = str(value)
        
        # Check length
        if len(value) < self.min_length:
            raise ValidationError(f"Value must be at least {self.min_length} characters long.")
        
        if len(value) > self.max_length:
            raise ValidationError(f"Value must be no more than {self.max_length} characters long.")
        
        return value


class IntegerField(Field):
    """Integer field."""
    
    def __init__(self, min_value: Optional[int] = None, max_value: Optional[int] = None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any) -> int:
        value = super().validate(value)
        
        if value is None:
            return value
        
        # Convert to integer
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError("Value must be an integer.")
        
        # Check range
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"Value must be at least {self.min_value}.")
        
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"Value must be no more than {self.max_value}.")
        
        return value


class FloatField(Field):
    """Float field."""
    
    def __init__(self, min_value: Optional[float] = None, max_value: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any) -> float:
        value = super().validate(value)
        
        if value is None:
            return value
        
        # Convert to float
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValidationError("Value must be a number.")
        
        # Check range
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"Value must be at least {self.min_value}.")
        
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"Value must be no more than {self.max_value}.")
        
        return value


class BooleanField(Field):
    """Boolean field."""
    
    def validate(self, value: Any) -> bool:
        value = super().validate(value)
        
        if value is None:
            return value
        
        # Convert to boolean
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        else:
            return bool(value)


class EmailField(CharField):
    """Email field with validation."""
    
    def __init__(self, **kwargs):
        # Set reasonable defaults for email field
        kwargs.setdefault('max_length', 254)
        super().__init__(**kwargs)
    
    def validate(self, value: Any) -> str:
        value = super().validate(value)
        
        if value is None:
            return value
        
        # Email validation regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValidationError("Enter a valid email address.")
        
        return value


class DateTimeField(Field):
    """DateTime field."""
    
    def validate(self, value: Any) -> str:
        value = super().validate(value)
        
        if value is None:
            return value
        
        # For simplicity, we'll just convert to string
        # In a real implementation, you'd use datetime objects
        return str(value)


class ForeignKey(Field):
    """Foreign key field."""
    
    def __init__(self, to_model: str, **kwargs):
        super().__init__(**kwargs)
        self.to_model = to_model
    
    def validate(self, value: Any) -> int:
        value = super().validate(value)
        
        if value is None:
            return value
        
        # Convert to integer (foreign key is typically an ID)
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError("Foreign key must be an integer.")
        
        # In a real implementation, you'd check if the referenced object exists
        return value


# Convenience functions for common field types
def AutoField(**kwargs):
    """Auto-incrementing integer field."""
    kwargs['required'] = False
    return IntegerField(**kwargs)


def TextField(**kwargs):
    """Text field (unlimited length string)."""
    kwargs.setdefault('max_length', 65535)
    return CharField(**kwargs)


def URLField(**kwargs):
    """URL field."""
    def validate_url(value):
        url_regex = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
        if not re.match(url_regex, value):
            raise ValidationError("Enter a valid URL.")
    
    validators = kwargs.get('validators', [])
    validators.append(validate_url)
    kwargs['validators'] = validators
    return CharField(**kwargs)