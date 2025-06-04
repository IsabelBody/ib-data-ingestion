from datetime import datetime
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GarminTransformer:
    def transform_activity(self, raw_activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw activity data into the bronze layer format.
        
        Args:
            raw_activity: Raw activity data from Garmin Connect
            
        Returns:
            Transformed activity data in bronze layer format
        """
        try:
            transformed = {
                'source': 'garmin',
                'data_type': 'activity',
                'source_timestamp': raw_activity['startTime'],
                'validation_status': 'valid',
                'raw_data': raw_activity,
                'metadata': {
                    'device': raw_activity.get('deviceName'),
                    'activity_type': raw_activity.get('activityType'),
                    'duration_seconds': raw_activity.get('duration'),
                    'distance_meters': raw_activity.get('distance'),
                    'calories': raw_activity.get('calories'),
                    'average_heart_rate': raw_activity.get('averageHeartRate'),
                    'max_heart_rate': raw_activity.get('maxHeartRate'),
                    'average_speed': raw_activity.get('averageSpeed'),
                    'max_speed': raw_activity.get('maxSpeed'),
                    'average_pace': raw_activity.get('averagePace'),
                    'max_pace': raw_activity.get('maxPace'),
                    'elevation_gain': raw_activity.get('elevationGain'),
                    'elevation_loss': raw_activity.get('elevationLoss')
                }
            }
            
            logger.info(f"Successfully transformed activity {raw_activity.get('activityId')}")
            return transformed
            
        except Exception as e:
            logger.error(f"Failed to transform activity: {str(e)}")
            raise
            
    def transform_sleep(self, raw_sleep: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw sleep data into the bronze layer format.
        
        Args:
            raw_sleep: Raw sleep data from Garmin Connect
            
        Returns:
            Transformed sleep data in bronze layer format
        """
        try:
            sleep_dto = raw_sleep['dailySleepDTO']
            
            transformed = {
                'source': 'garmin',
                'data_type': 'sleep',
                'source_timestamp': sleep_dto['sleepStartTimestampGMT'],
                'validation_status': 'valid',
                'raw_data': raw_sleep,
                'metadata': {
                    'date': sleep_dto['calendarDate'],
                    'total_sleep_seconds': sleep_dto['sleepTimeSeconds'],
                    'deep_sleep_seconds': sleep_dto['deepSleepSeconds'],
                    'light_sleep_seconds': sleep_dto['lightSleepSeconds'],
                    'rem_sleep_seconds': sleep_dto['remSleepSeconds'],
                    'awake_seconds': sleep_dto['awakeSleepSeconds'],
                    'sleep_start_gmt': sleep_dto['sleepStartTimestampGMT'],
                    'sleep_end_gmt': sleep_dto['sleepEndTimestampGMT'],
                    'sleep_start_local': sleep_dto['sleepStartTimestampLocal'],
                    'sleep_end_local': sleep_dto['sleepEndTimestampLocal'],
                    'average_sleep_stress': sleep_dto['averageSleepStress'],
                    'sleep_scores': sleep_dto['sleepScores']
                }
            }
            
            logger.info(f"Successfully transformed sleep data for {sleep_dto['calendarDate']}")
            return transformed
            
        except Exception as e:
            logger.error(f"Failed to transform sleep data: {str(e)}")
            raise 