import pytest
from unittest.mock import Mock, patch
from src.utils.validation import DataValidator
from datetime import datetime

@pytest.fixture
def validator(test_schema):
    return DataValidator(test_schema)

def test_valid_data(validator):
    data = {
        'id': 'test_1',
        'timestamp': datetime.utcnow().isoformat(),
        'value': 100
    }
    result = validator.validate(data)
    assert result.is_valid is True
    assert len(result.errors) == 0
    assert len(result.warnings) == 0

def test_invalid_data_missing_required(validator):
    data = {
        'id': 'test_1',
        'timestamp': datetime.utcnow().isoformat()
        # missing 'value' field
    }
    result = validator.validate(data)
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert "'value' is a required property" in str(result.errors[0])

def test_invalid_data_wrong_type(validator):
    data = {
        'id': 'test_1',
        'timestamp': datetime.utcnow().isoformat(),
        'value': 'not_a_number'  # should be a number
    }
    result = validator.validate(data)
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert "'not_a_number' is not of a type(s) 'number'" in str(result.errors[0])

def test_invalid_timestamp_format(validator):
    data = {
        'id': 'test_1',
        'timestamp': 'invalid_timestamp',
        'value': 100
    }
    result = validator.validate(data)
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert "is not a 'date-time'" in str(result.errors[0])

def test_validation_with_warnings(validator):
    # Add a warning rule to the schema
    validator.schema['properties']['value']['minimum'] = 0
    validator.schema['properties']['value']['maximum'] = 1000
    
    data = {
        'id': 'test_1',
        'timestamp': datetime.utcnow().isoformat(),
        'value': 2000  # Above maximum but not invalid
    }
    result = validator.validate(data)
    assert result.is_valid is True
    assert len(result.errors) == 0
    assert len(result.warnings) > 0

def test_validation_with_custom_rules(validator):
    # Add a custom validation rule
    def custom_rule(data):
        if data['value'] < 0:
            return False, "Value cannot be negative"
        return True, None
    
    validator.add_custom_rule(custom_rule)
    
    data = {
        'id': 'test_1',
        'timestamp': datetime.utcnow().isoformat(),
        'value': -100
    }
    result = validator.validate(data)
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert "Value cannot be negative" in str(result.errors[0])

def test_validation_with_multiple_errors(validator):
    data = {
        'id': 123,  # should be string
        'timestamp': 'invalid_timestamp',
        'value': 'not_a_number'
    }
    result = validator.validate(data)
    assert result.is_valid is False
    assert len(result.errors) > 1 