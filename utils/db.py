import os
import asyncpg
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

class DatabaseManager:
    _pool: Optional[asyncpg.Pool] = None
    
    @classmethod
    async def initialize(cls) -> None:
        """Initialize the database connection pool."""
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                host=os.getenv('PG_HOST', 'localhost'),
                port=int(os.getenv('PG_PORT', '5432')),
                database=os.getenv('PG_DB', 'ib_data'),
                user=os.getenv('PG_USER', 'postgres'),
                password=os.getenv('PG_PASS', 'password'),
                min_size=5,
                max_size=20
            )
    
    @classmethod
    async def close(cls) -> None:
        """Close the database connection pool."""
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
    
    @classmethod
    @asynccontextmanager
    async def get_connection(cls):
        """Get a database connection from the pool."""
        if cls._pool is None:
            await cls.initialize()
        async with cls._pool.acquire() as connection:
            yield connection
    
    @classmethod
    async def execute_query(cls, query: str, *args) -> Any:
        """Execute a query and return the results."""
        async with cls.get_connection() as conn:
            return await conn.fetch(query, *args)
    
    @classmethod
    async def execute_transaction(cls, queries: list[tuple[str, tuple]]) -> None:
        """Execute multiple queries in a transaction."""
        async with cls.get_connection() as conn:
            async with conn.transaction():
                for query, params in queries:
                    await conn.execute(query, *params)
    
    @classmethod
    async def insert_bronze_data(cls, source: str, data: Dict[str, Any]) -> int:
        """Insert data into the bronze layer."""
        query = """
        INSERT INTO bronze_template (
            source, raw_data, source_timestamp, raw_id,
            validation_status, metadata, pipeline_run_id
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id
        """
        async with cls.get_connection() as conn:
            return await conn.fetchval(
                query,
                source,
                data['raw_data'],
                data.get('source_timestamp'),
                data.get('raw_id'),
                data.get('validation_status', 'valid'),
                data.get('metadata', {}),
                data.get('pipeline_run_id')
            )

    @asynccontextmanager
    async def transaction(self):
        """Context manager for database transactions."""
        if not self._pool:
            await self.initialize()
        
        async with self._pool.acquire() as conn:
            async with conn.transaction() as transaction:
                yield transaction

    async def execute(self, query: str, *args, **kwargs) -> str:
        """Execute a query and return the result."""
        if not self._pool:
            await self.initialize()
        
        async with self._pool.acquire() as conn:
            return await conn.execute(query, *args, **kwargs)

    async def fetch(self, query: str, *args, **kwargs) -> list:
        """Execute a query and return all results."""
        if not self._pool:
            await self.initialize()
        
        async with self._pool.acquire() as conn:
            return await conn.fetch(query, *args, **kwargs)

    async def fetchrow(self, query: str, *args, **kwargs) -> Optional[Dict[str, Any]]:
        """Execute a query and return one row."""
        if not self._pool:
            await self.initialize()
        
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(query, *args, **kwargs)

    async def create_partition(self, source_name: str, partition_date: str) -> None:
        """Create a new partition for a source table."""
        query = """
        SELECT create_partition_if_not_exists($1, $2::date);
        """
        await self.execute(query, source_name, partition_date) 