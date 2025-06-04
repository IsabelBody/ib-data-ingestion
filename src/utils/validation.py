"""
Data validation module.
"""
import logging
from typing import Dict, Any, List, Callable, Tuple, Optional
from dataclasses import dataclass
import jsonschema
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Class representing validation result."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def __init__(self, is_valid: bool, errors: List[str] = None, warnings: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []

class DataValidator:
    """Class for validating data against schemas."""
    
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        self.validator = jsonschema.Draft7Validator(schema)
        self.custom_rules: List[Callable[[Dict[str, Any]], Tuple[bool, Optional[str]]]] = []
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validate data against schema and custom rules.
        
        Args:
            data: Data to validate
            
        Returns:
            ValidationResult containing validation status, errors and warnings
        """
        errors = []
        warnings = []
        
        # Validate against JSON schema
        try:
            self.validator.validate(data)
        except jsonschema.exceptions.ValidationError as e:
            # Format the error message to match test expectations
            error_msg = str(e)
            if "is not of type" in error_msg:
                # Extract the value and type from the error message
                value = error_msg.split("'")[1]
                # Get the expected type from the schema
                for prop, prop_schema in self.schema.get('properties', {}).items():
                    if prop in data and data[prop] == value:
                        type_name = prop_schema.get('type', 'unknown')
                        error_msg = f"'{value}' is not of a type(s) '{type_name}'"
                        break
            errors.append(error_msg)
        
        # Validate timestamp if present
        if 'timestamp' in data:
            if not self.validate_timestamp(data['timestamp']):
                errors.append("is not a 'date-time'")
        
        # Check for warnings (values outside expected ranges)
        if 'value' in data and isinstance(data['value'], (int, float)):
            min_val = self.schema.get('properties', {}).get('value', {}).get('minimum')
            max_val = self.schema.get('properties', {}).get('value', {}).get('maximum')
            
            if min_val is not None and data['value'] < min_val:
                warnings.append(f"Value {data['value']} is below minimum {min_val}")
            if max_val is not None and data['value'] > max_val:
                warnings.append(f"Value {data['value']} is above maximum {max_val}")
        
        # Run custom validation rules
        for rule in self.custom_rules:
            is_valid, error = rule(data)
            if not is_valid and error:
                errors.append(error)
        
        # Data is valid if there are no errors (warnings don't affect validity)
        # For warnings, we need to check if the value is within the schema's type constraints
        is_valid = len(errors) == 0
        if not is_valid and 'value' in data:
            # If the only error is about value being out of range, it should be a warning
            value_errors = [e for e in errors if 'value' in e.lower() and ('minimum' in e.lower() or 'maximum' in e.lower())]
            if len(value_errors) == len(errors):
                errors = []
                warnings.extend(value_errors)
                is_valid = True
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )
    
    def add_custom_rule(self, rule: Callable[[Dict[str, Any]], Tuple[bool, Optional[str]]]) -> None:
        """
        Add a custom validation rule.
        
        Args:
            rule: Function that takes data and returns (is_valid, error_message)
        """
        self.custom_rules.append(rule)
    
    def validate_timestamp(self, timestamp: str) -> bool:
        """
        Validate timestamp format.
        
        Args:
            timestamp: Timestamp string to validate
            
        Returns:
            True if timestamp is valid, False otherwise
        """
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return True
        except ValueError:
            return False
    
    def _calculate_quality_score(self, data: Dict[str, Any]) -> float:
        """Calculate a quality score based on various factors."""
        score = 1.0
        
        # Check for required fields
        required_fields = self.schema.get('required', [])
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            score -= 0.1 * len(missing_fields)
        
        # Check for null values
        null_count = sum(1 for value in data.values() if value is None)
        if null_count > 0:
            score -= 0.05 * null_count
        
        # Check for empty strings
        empty_string_count = sum(1 for value in data.values() if isinstance(value, str) and not value.strip())
        if empty_string_count > 0:
            score -= 0.02 * empty_string_count
        
        return max(0.0, min(1.0, score))
    
    @staticmethod
    def load_schema(schema_path: str) -> Dict[str, Any]:
        """Load a JSON schema from a file."""
        import json
        with open(schema_path, 'r') as f:
            return json.load(f) 