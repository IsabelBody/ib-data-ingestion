import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path

class StructuredLogger:
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create formatters
        self.json_formatter = logging.Formatter(
            '%(message)s'
        )
        self.console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(self.json_formatter)
            self.logger.addHandler(file_handler)
    
    def _log(self, level: int, message: str, **kwargs):
        """Internal logging method with structured data."""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'message': message,
            'level': logging.getLevelName(level),
            **kwargs
        }
        
        if level >= logging.ERROR:
            self.logger.error(json.dumps(log_data))
        elif level >= logging.WARNING:
            self.logger.warning(json.dumps(log_data))
        elif level >= logging.INFO:
            self.logger.info(json.dumps(log_data))
        else:
            self.logger.debug(json.dumps(log_data))
    
    def info(self, message: str, **kwargs):
        """Log info level message with structured data."""
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning level message with structured data."""
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error level message with structured data."""
        self._log(logging.ERROR, message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug level message with structured data."""
        self._log(logging.DEBUG, message, **kwargs)
    
    def exception(self, message: str, exc_info: Any = True, **kwargs):
        """Log exception with structured data."""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'message': message,
            'level': 'ERROR',
            'exception': str(exc_info),
            **kwargs
        }
        self.logger.error(json.dumps(log_data), exc_info=exc_info)

# Create default logger instance
logger = StructuredLogger('data_ingestion', 'logs/data_ingestion.log') 