import logging
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LoadResult:
    success: bool
    records_processed: int
    errors: List[str]

class DataLoader:
    def __init__(self, db_connection):
        self.db = db_connection
        self.table_name = "bronze_source_1"

    async def load(self, data: List[Dict]) -> LoadResult:
        """Load transformed data into the bronze layer."""
        logger.info(f"Loading {len(data)} records into {self.table_name}")
        
        errors = []
        records_processed = 0
        
        try:
            async with self.db.transaction() as transaction:
                for record in data:
                    try:
                        # Ensure partition exists
                        await self._ensure_partition(record['source_timestamp'])
                        
                        # Insert record
                        await self._insert_record(record)
                        records_processed += 1
                        
                    except Exception as e:
                        error_msg = f"Error loading record {record.get('raw_id')}: {str(e)}"
                        logger.error(error_msg)
                        errors.append(error_msg)
                        continue
            
            return LoadResult(
                success=len(errors) == 0,
                records_processed=records_processed,
                errors=errors
            )
            
        except Exception as e:
            error_msg = f"Error in load transaction: {str(e)}"
            logger.error(error_msg)
            return LoadResult(
                success=False,
                records_processed=records_processed,
                errors=[error_msg]
            )

    async def _ensure_partition(self, timestamp: str) -> None:
        """Ensure the partition for the given timestamp exists."""
        partition_date = datetime.fromisoformat(timestamp).date()
        await self.db.create_partition("source_1", partition_date.isoformat())

    async def _insert_record(self, record: Dict) -> None:
        """Insert a single record into the bronze layer."""
        query = f"""
        INSERT INTO {self.table_name} (
            source,
            raw_data,
            source_timestamp,
            raw_id,
            validation_status,
            metadata
        ) VALUES (
            $1, $2, $3, $4, $5, $6
        )
        """
        
        await self.db.execute(
            query,
            record['source'],
            record['raw_data'],
            record['source_timestamp'],
            record['raw_id'],
            record['validation_status'],
            record['metadata']
        ) 