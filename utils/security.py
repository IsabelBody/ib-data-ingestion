import os
from typing import Dict, Any
from pathlib import Path

class CredentialManager:
    def __init__(self, config_path: str = "configs/.env"):
        self.config_path = Path(config_path)
        self.credentials = {}
        self._load_credentials()

    def _load_credentials(self) -> None:
        """Load credentials from .env file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Credentials file not found: {self.config_path}")
        
        with open(self.config_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    self.credentials[key.strip()] = value.strip()

    def get_credentials(self, source: str) -> Dict[str, str]:
        """Get credentials for a specific source."""
        prefix = f"{source.upper()}_"
        return {
            k.replace(prefix, '').lower(): v 
            for k, v in self.credentials.items() 
            if k.startswith(prefix)
        }

    def validate_credentials(self, source: str) -> bool:
        """Validate that all required credentials are present for a source."""
        required_keys = {
            'client_id',
            'client_secret'
        }
        
        credentials = self.get_credentials(source)
        return all(key in credentials for key in required_keys)

    def rotate_credentials(self, source: str, new_credentials: Dict[str, str]) -> None:
        """Rotate credentials for a source."""
        prefix = f"{source.upper()}_"
        
        # Update credentials in memory
        for key, value in new_credentials.items():
            self.credentials[f"{prefix}{key.upper()}"] = value
        
        # Update credentials file
        with open(self.config_path, 'w') as f:
            for key, value in self.credentials.items():
                f.write(f"{key}={value}\n") 