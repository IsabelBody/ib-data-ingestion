import pytest
from datetime import datetime
from unittest.mock import patch, Mock, AsyncMock

from src.utils.db import DatabaseManager

@pytest.fixture
def db_manager(test_config):
    return DatabaseManager(test_config['database'])

@pytest.mark.asyncio
async def test_connection(db_manager):
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        
        await db_manager.connect()
        assert db_manager.connection is not None
        mock_connect.assert_called_once()

@pytest.mark.asyncio
async def test_insert_bronze_data(db_manager, sample_bronze_data):
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        # Simulate successful insert for each record
        mock_cursor.execute.side_effect = [None] * len(sample_bronze_data)
        
        await db_manager.connect()
        result = await db_manager.insert_bronze_data(sample_bronze_data, source='test_source')
        
        assert result['total_records'] == len(sample_bronze_data)
        assert result['successful_records'] == len(sample_bronze_data)
        assert result['failed_records'] == 0
        assert len(result['errors']) == 0
        assert mock_cursor.execute.call_count == len(sample_bronze_data)

@pytest.mark.asyncio
async def test_get_bronze_data(db_manager):
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_data = [{'id': '1', 'raw_data': {'key': 'value'}}]
        mock_cursor.fetchall.return_value = mock_data
        
        await db_manager.connect()
        result = await db_manager.get_bronze_data('test_source', limit=1)
        
        assert result == mock_data
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()

@pytest.mark.asyncio
async def test_connection_error(db_manager):
    with patch('psycopg2.connect', side_effect=Exception("Connection error")):
        with pytest.raises(Exception) as exc_info:
            await db_manager.connect()
        assert "Connection error" in str(exc_info.value)

@pytest.mark.asyncio
async def test_insert_error(db_manager, sample_bronze_data):
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        # Simulate error for every insert
        mock_cursor.execute.side_effect = Exception("Insert error")
        
        await db_manager.connect()
        result = await db_manager.insert_bronze_data(sample_bronze_data, source='test_source')
        
        assert result['total_records'] == len(sample_bronze_data)
        assert result['successful_records'] == 0
        assert result['failed_records'] == len(sample_bronze_data)
        assert len(result['errors']) == len(sample_bronze_data)
        for error in result['errors']:
            assert "Insert error" in error 