import json
from typing import Dict, Any
from src.utils.db import get_db_connection
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GarminLoader:
    def load(self, data: Dict[str, Any]) -> None:
        """
        Load transformed data into the bronze layer.
        
        Args:
            data: Transformed data in bronze layer format
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    # Convert raw_data and metadata to JSONB
                    raw_data_json = json.dumps(data['raw_data'])
                    metadata_json = json.dumps(data['metadata'])
                    
                    # Insert into bronze_garmin table
                    cur.execute("""
                        INSERT INTO bronze_garmin (
                            source,
                            raw_data,
                            source_timestamp,
                            validation_status,
                            metadata,
                            data_type
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s
                        )
                    """, (
                        data['source'],
                        raw_data_json,
                        data['source_timestamp'],
                        data['validation_status'],
                        metadata_json,
                        data['data_type']
                    ))
                    
                    conn.commit()
                    logger.info(f"Successfully loaded {data['data_type']} data into bronze layer")
                    
        except Exception as e:
            logger.error(f"Failed to load data into bronze layer: {str(e)}")
            raise 