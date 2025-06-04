import pytest
from datetime import datetime, timedelta
from pipelines.templates.extract import DataExtractor
from pipelines.templates.transform import DataTransformer
from pipelines.templates.load import DataLoader
from utils.validation import DataValidator
import json
import os
from unittest.mock import patch, Mock

@pytest.fixture
def config():
    return {
        'source_name': 'test_source',
        'api_url': 'https://api.example.com/data',
        'api_key': 'test_key',
        'rate_limit': 100,
        'retry_attempts': 3,
        'retry_delay': 1
    }

@pytest.fixture
def test_schema():
    return {
        "type": "object",
        "required": ["id", "timestamp", "value"],
        "properties": {
            "id": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"},
            "value": {"type": "number"},
            "_metadata": {
                "type": "object",
                "required": ["fetched_at", "source", "api_version"],
                "properties": {
                    "fetched_at": {"type": "string", "format": "date-time"},
                    "source": {"type": "string"},
                    "api_version": {"type": "string"}
                }
            }
        }
    }

@pytest.fixture
def validator(test_schema):
    return DataValidator(test_schema)

@pytest.fixture
def sample_data():
    return [
        {
            'id': '1',
            'timestamp': '2024-01-01T00:00:00Z',
            'value': 100,
            '_metadata': {
                'fetched_at': '2024-01-01T00:00:00Z',
                'source': 'test_source',
                'api_version': '1.0'
            }
        }
    ]

@pytest.mark.asyncio
async def test_extract(config):
    async with DataExtractor(config) as extractor:
        start_date = datetime.utcnow() - timedelta(days=1)
        end_date = datetime.utcnow()
        
        # Mock the _fetch_page method
        async def mock_fetch_page(date):
            return [{
                'id': '1',
                'timestamp': date.isoformat(),
                'value': 100,
                '_metadata': {
                    'fetched_at': datetime.utcnow().isoformat(),
                    'source': config['source_name'],
                    'api_version': '1.0'
                }
            }]
        
        extractor._fetch_page = mock_fetch_page
        
        data = await extractor.fetch_data(start_date, end_date)
        assert len(data) > 0
        assert 'id' in data[0]
        assert '_metadata' in data[0]

def test_transform(validator, sample_data):
    transformer = DataTransformer()
    transformed_data = transformer.transform(sample_data)
    
    assert len(transformed_data) == len(sample_data)
    assert transformed_data[0] == sample_data[0]  # No transformation in template

@pytest.mark.asyncio
async def test_load(sample_data):
    loader = DataLoader('test_source')
    results = await loader.load(sample_data)
    
    assert results.records_processed == len(sample_data)
    assert len(results.errors) == 0 