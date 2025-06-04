import pytest
import os
from datetime import datetime, timedelta
import json
from unittest.mock import Mock

@pytest.fixture
def test_config():
    return {
        'database': {
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password'
        },
        'monitoring': {
            'prometheus_port': 9090,
            'health_check_port': 8000
        }
    }

@pytest.fixture
def sample_bronze_data():
    return {
        'id': 'test_id_1',
        'source': 'test_source',
        'raw_data': {
            'key1': 'value1',
            'key2': 'value2',
            'timestamp': datetime.utcnow().isoformat()
        },
        'ingested_at': datetime.utcnow(),
        'source_timestamp': datetime.utcnow(),
        'raw_id': 'raw_123',
        'validation_status': 'valid',
        'error_message': None,
        'metadata': {},
        'version': 1,
        'environment': 'test'
    }

@pytest.fixture
def mock_db_connection():
    mock_conn = Mock()
    mock_conn.execute = Mock()
    mock_conn.commit = Mock()
    mock_conn.rollback = Mock()
    return mock_conn

@pytest.fixture
def mock_prometheus_client():
    mock_client = Mock()
    mock_client.Counter = Mock(return_value=Mock())
    mock_client.Gauge = Mock(return_value=Mock())
    mock_client.Histogram = Mock(return_value=Mock())
    return mock_client

@pytest.fixture
def test_schema():
    return {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"},
            "value": {"type": "number"}
        },
        "required": ["id", "timestamp", "value"]
    } 