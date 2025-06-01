from typing import Dict, Any, List
from datetime import datetime
from utils.db import DatabaseManager
from utils.logger import logger

class DataLoader:
    """
    Loads raw data into the bronze layer database.
    
    This class handles the loading of raw data into the bronze layer, maintaining
    data fidelity and adding minimal metadata. It implements batch processing for
    efficiency and maintains comprehensive error logging.
    
    Attributes:
        source_name (str): The name of the data source being loaded.
    
    Example:
        >>> loader = DataLoader('my_source')
        >>> results = await loader.load([{'raw_data': {...}}])
    """
    
    def __init__(self, source_name: str):
        """
        Initialize the data loader.
        
        Args:
            source_name (str): The name of the data source being loaded.
        """
        self.source_name = source_name
    
    async def load(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Load raw data into the database.
        
        This method loads raw data into the bronze layer database:
        - Processes data in batches for efficiency
        - Adds minimal metadata (source, ingestion timestamp)
        - Maintains comprehensive error logging
        - Preserves data fidelity
        
        Args:
            data (List[Dict[str, Any]]): List of raw data items to load.
            
        Returns:
            Dict[str, Any]: Loading results including success/failure counts and errors.
            
        Note:
            - No data transformation is performed
            - Original data structure is preserved
            - Failed loads are logged but processing continues
        """
        start_time = datetime.utcnow()
        results = {
            'total_records': len(data),
            'successful_records': 0,
            'failed_records': 0,
            'errors': []
        }
        
        try:
            # Initialize database connection
            await DatabaseManager.initialize()
            
            # Process records in batches
            batch_size = 100
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                batch_results = await self._load_batch(batch)
                
                results['successful_records'] += batch_results['successful_records']
                results['failed_records'] += batch_results['failed_records']
                results['errors'].extend(batch_results['errors'])
            
            # Log results
            logger.info(
                "Data load completed",
                source=self.source_name,
                duration_seconds=(datetime.utcnow() - start_time).total_seconds(),
                **results
            )
            
            return results
            
        except Exception as e:
            logger.error(
                "Error during data load",
                source=self.source_name,
                error=str(e)
            )
            raise
            
        finally:
            await DatabaseManager.close()
    
    async def _load_batch(self, batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Load a batch of records into the database.
        
        This method loads a batch of records into the database:
        - Adds source information
        - Preserves raw data
        - Handles errors gracefully
        - Maintains error logging
        
        Args:
            batch (List[Dict[str, Any]]): Batch of records to load.
            
        Returns:
            Dict[str, Any]: Batch loading results including success/failure counts and errors.
        """
        results = {
            'successful_records': 0,
            'failed_records': 0,
            'errors': []
        }
        
        for record in batch:
            try:
                # Add source information
                record['source'] = self.source_name
                
                # Insert record
                await DatabaseManager.insert_bronze_data(self.source_name, record)
                results['successful_records'] += 1
                
            except Exception as e:
                results['failed_records'] += 1
                results['errors'].append({
                    'record_id': record.get('raw_id', 'unknown'),
                    'error': str(e)
                })
                
                logger.error(
                    "Error loading record",
                    source=self.source_name,
                    record_id=record.get('raw_id', 'unknown'),
                    error=str(e)
                )
        
        return results 