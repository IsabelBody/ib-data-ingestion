import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import garminconnect
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GarminExtractor:
    def __init__(self):
        self.client = self._initialize_client()
        
    def _initialize_client(self) -> garminconnect.Garmin:
        """Initialize the Garmin Connect client with credentials from environment variables."""
        email = os.getenv('GARMIN_EMAIL')
        password = os.getenv('GARMIN_PASSWORD')
        
        if not email or not password:
            raise ValueError("Garmin credentials not found in environment variables")
            
        try:
            client = garminconnect.Garmin(email, password)
            client.login()
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Garmin client: {str(e)}")
            raise
            
    def extract_activities(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict[str, Any]]:
        """
        Extract activities from Garmin Connect.
        
        Args:
            start_date: Start date for activity extraction (default: 7 days ago)
            end_date: End date for activity extraction (default: today)
            
        Returns:
            List of activity data dictionaries
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=7)
        if not end_date:
            end_date = datetime.now()
            
        try:
            activities = self.client.get_activities(start_date, end_date)
            logger.info(f"Successfully extracted {len(activities)} activities")
            return activities
        except Exception as e:
            logger.error(f"Failed to extract activities: {str(e)}")
            raise
            
    def extract_sleep(self, date: datetime = None) -> Dict[str, Any]:
        """
        Extract sleep data from Garmin Connect.
        
        Args:
            date: Date to extract sleep data for (default: yesterday)
            
        Returns:
            Dictionary containing sleep data
        """
        if not date:
            date = datetime.now() - timedelta(days=1)
            
        try:
            sleep_data = self.client.get_sleep_data(date)
            logger.info(f"Successfully extracted sleep data for {date.date()}")
            return sleep_data
        except Exception as e:
            logger.error(f"Failed to extract sleep data: {str(e)}")
            raise 