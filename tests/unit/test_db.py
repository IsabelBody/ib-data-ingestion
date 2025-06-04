import pytest
from datetime import datetime
from utils.db import DatabaseManager
from unittest.mock import patch, Mock

@pytest.fixture
def db_manager(test_config):
    return DatabaseManager(test_config['database'])

@pytest.mark.asyncio
async def test_connection(db_manager):
    with patch('asyncpg.create_pool') as mock_create_pool:
        mock_pool = Mock()
        mock_create_pool.return_value = mock_pool
        
        await db_manager.connect()
        assert db_manager.pool is not None
        mock_create_pool.assert_called_once()

@pytest.mark.asyncio
async def test_insert_bronze_data(db_manager, sample_bronze_data):
    with patch('asyncpg.create_pool') as mock_create_pool:
        mock_pool = Mock()
        mock_create_pool.return_value = mock_pool
        
        mock_pool.acquire.return_value.__aenter__.return_value.execute.return_value = "INSERT 1"
        
        await db_manager.connect()
        result = await db_manager.insert_bronze_data(sample_bronze_data)
        
        assert result == "INSERT 1"
        mock_pool.acquire.return_value.__aenter__.return_value.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_bronze_data(db_manager):
    with patch('asyncpg.create_pool') as mock_create_pool:
        mock_pool = Mock()
        mock_create_pool.return_value = mock_pool
        
        mock_data = [{'id': '1', 'raw_data': {'key': 'value'}}]
        mock_pool.acquire.return_value.__aenter__.return_value.fetch.return_value = mock_data
        
        await db_manager.connect()
        result = await db_manager.get_bronze_data('test_source', limit=1)
        
        assert result == mock_data
        mock_pool.acquire.return_value.__aenter__.return_value.fetch.assert_called_once()

@pytest.mark.asyncio
async def test_connection_error(db_manager):
    with patch('asyncpg.create_pool', side_effect=Exception("Connection error")):
        with pytest.raises(Exception) as exc_info:
            await db_manager.connect()
        assert "Connection error" in str(exc_info.value)

@pytest.mark.asyncio
async def test_insert_error(db_manager, sample_bronze_data):
    with patch('asyncpg.create_pool') as mock_create_pool:
        mock_pool = Mock()
        mock_create_pool.return_value = mock_pool
        
        mock_pool.acquire.return_value.__aenter__.return_value.execute.side_effect = Exception("Insert error")
        
        await db_manager.connect()
        with pytest.raises(Exception) as exc_info:
            await db_manager.insert_bronze_data(sample_bronze_data)
        assert "Insert error" in str(exc_info.value) 