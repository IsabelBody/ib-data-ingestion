"""
Alert management module for monitoring system.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

class AlertManager:
    """Class for managing system alerts."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.alerts: List[Dict[str, Any]] = []
    
    def create_alert(self, source: str, level: str, message: str) -> Dict[str, Any]:
        """
        Create a new alert.
        
        Args:
            source: Source of the alert
            level: Alert level (info, warning, error)
            message: Alert message
            
        Returns:
            Dictionary containing alert details
        """
        alert = {
            'source': source,
            'level': level,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.alerts.append(alert)
        logger.warning(f"Alert created: {alert}")
        return alert
    
    def get_alerts(self, level: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all alerts, optionally filtered by level.
        
        Args:
            level: Optional alert level to filter by
            
        Returns:
            List of alert dictionaries
        """
        if level:
            return [a for a in self.alerts if a['level'] == level]
        return self.alerts
    
    def clear_alerts(self) -> None:
        """Clear all alerts."""
        self.alerts = []
        logger.info("All alerts cleared") 