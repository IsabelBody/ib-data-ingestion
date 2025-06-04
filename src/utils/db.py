"""
Database management module.
"""
import logging
from typing import Dict, Any, List, Optional
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import json

# Configure logging
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Class for managing database connections and operations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
        self.cursor = None
    
    async def connect(self) -> None:
        """Establish database connection."""
        try:
            self.connection = psycopg2.connect(**self.config)
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    async def insert_bronze_data(self, data: List[Dict[str, Any]], source: str) -> Dict[str, Any]:
        """Insert data into bronze layer."""
        try:
            results = {
                'total_records': len(data),
                'successful_records': 0,
                'failed_records': 0,
                'errors': []
            }
            
            for record in data:
                try:
                    # Add metadata
                    record['_metadata'] = {
                        'ingested_at': datetime.utcnow().isoformat(),
                        'source': source
                    }
                    
                    # Insert record
                    query = """
                        INSERT INTO bronze_data (data, source, ingested_at)
                        VALUES (%s, %s, %s)
                    """
                    self.cursor.execute(
                        query,
                        (json.dumps(record), source, datetime.utcnow())
                    )
                    results['successful_records'] += 1
                    
                except Exception as e:
                    results['failed_records'] += 1
                    results['errors'].append(str(e))
            
            self.connection.commit()
            return results
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Failed to insert bronze data: {e}")
            raise
    
    async def get_bronze_data(
        self,
        source: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """Get data from bronze layer with optional filtering."""
        try:
            query = "SELECT * FROM bronze_data WHERE 1=1"
            params = {}
            
            if source:
                query += " AND source = %s"
                params['source'] = source
            
            if start_time:
                query += " AND ingested_at >= %s"
                params['start_time'] = start_time
            
            if end_time:
                query += " AND ingested_at <= %s"
                params['end_time'] = end_time
            
            query += f" ORDER BY ingested_at DESC LIMIT {limit}"
            
            return await self.execute_query(query, params)
            
        except Exception as e:
            logger.error(f"Failed to get bronze data: {e}")
            raise 