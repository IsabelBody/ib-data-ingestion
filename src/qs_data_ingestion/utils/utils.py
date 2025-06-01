"""
Configuration validation module for ensuring proper setup of the system.
"""
import os
import json
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path
import yaml
from jsonschema import validate, ValidationError

# Configure logging
logger = logging.getLogger(__name__)

class ConfigValidator:
    """Class for validating configuration files and environment variables."""
    
    def __init__(self, schema_path: str):
        self.schema_path = schema_path
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load the JSON schema for validation."""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load schema: {e}")
            raise
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """Validate configuration against schema."""
        errors = []
        try:
            validate(instance=config, schema=self.schema)
        except ValidationError as e:
            errors.append(str(e))
        return errors
    
    def validate_env_vars(self, required_vars: List[str]) -> List[str]:
        """Validate required environment variables."""
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        return missing_vars
    
    def validate_file_paths(self, paths: Dict[str, str]) -> List[str]:
        """Validate that required files exist."""
        missing_files = []
        for name, path in paths.items():
            if not Path(path).exists():
                missing_files.append(f"{name}: {path}")
        return missing_files
    
    def validate_yaml_config(self, yaml_path: str) -> List[str]:
        """Validate YAML configuration file."""
        errors = []
        try:
            with open(yaml_path, 'r') as f:
                config = yaml.safe_load(f)
            errors.extend(self.validate_config(config))
        except Exception as e:
            errors.append(f"Failed to load YAML config: {e}")
        return errors
    
    def validate_all(self, 
                    config: Dict[str, Any],
                    required_env_vars: List[str],
                    required_files: Dict[str, str]) -> Dict[str, List[str]]:
        """Perform all validations and return results."""
        return {
            'config_errors': self.validate_config(config),
            'missing_env_vars': self.validate_env_vars(required_env_vars),
            'missing_files': self.validate_file_paths(required_files)
        }
    
    def is_valid(self, validation_results: Dict[str, List[str]]) -> bool:
        """Check if all validations passed."""
        return all(not errors for errors in validation_results.values())
    
    def get_validation_summary(self, validation_results: Dict[str, List[str]]) -> str:
        """Get a human-readable summary of validation results."""
        summary = []
        for category, errors in validation_results.items():
            if errors:
                summary.append(f"{category}:")
                for error in errors:
                    summary.append(f"  - {error}")
        return "\n".join(summary) if summary else "All validations passed" 