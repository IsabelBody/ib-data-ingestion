from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import jsonschema
from datetime import datetime

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    quality_score: float = 1.0

class DataValidator:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        self.validator = jsonschema.Draft7Validator(schema)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate data against the schema and perform quality checks."""
        errors = []
        warnings = []
        
        # Schema validation
        try:
            self.validator.validate(data)
        except jsonschema.exceptions.ValidationError as e:
            errors.append(f"Schema validation error: {str(e)}")
        
        # Quality checks
        quality_score = self._calculate_quality_score(data)
        if quality_score < 0.8:
            warnings.append(f"Low quality score: {quality_score}")
        
        # Timestamp validation
        if 'source_timestamp' in data:
            try:
                datetime.fromisoformat(data['source_timestamp'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                errors.append("Invalid source_timestamp format")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            quality_score=quality_score
        )
    
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