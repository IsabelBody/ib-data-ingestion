from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.pipelines.sources.garmin.extract import GarminExtractor
from src.pipelines.sources.garmin.transform import GarminTransformer
from src.pipelines.sources.garmin.load import GarminLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GarminPipeline:
    def __init__(self):
        self.extractor = GarminExtractor()
        self.transformer = GarminTransformer()
        self.loader = GarminLoader()
        
    def run(self, start_date: datetime = None, end_date: datetime = None) -> None:
        """
        Run the complete Garmin data pipeline.
        
        Args:
            start_date: Start date for data extraction (default: 7 days ago)
            end_date: End date for data extraction (default: today)
        """
        try:
            # Extract activities
            activities = self.extractor.extract_activities(start_date, end_date)
            logger.info(f"Extracted {len(activities)} activities")
            
            # Transform and load activities
            for activity in activities:
                transformed = self.transformer.transform_activity(activity)
                self.loader.load(transformed)
                
            # Extract, transform and load sleep data
            current_date = start_date if start_date else datetime.now() - timedelta(days=7)
            while current_date <= (end_date if end_date else datetime.now()):
                try:
                    sleep_data = self.extractor.extract_sleep(current_date)
                    transformed = self.transformer.transform_sleep(sleep_data)
                    self.loader.load(transformed)
                except Exception as e:
                    logger.warning(f"Failed to process sleep data for {current_date.date()}: {str(e)}")
                current_date += timedelta(days=1)
                
            logger.info("Garmin pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Garmin pipeline failed: {str(e)}")
            raise 