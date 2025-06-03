import pytest
from datetime import datetime, timedelta
from pipelines.template.extract import DataExtractor
from pipelines.template.transform import DataTransformer
from pipelines.template.load import DataLoader
from utils.validation import DataValidator
import json
import os

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
def validator():
    schema_path = os.path.join('pipelines', 'template', 'schema.json')
    with open(schema_path) as f:
        schema = json.load(f)
    return DataValidator(schema)

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
    transformer = DataTransformer(validator)
    transformed_data = transformer.transform(sample_data)
    
    assert len(transformed_data) == len(sample_data)
    assert 'raw_data' in transformed_data[0]
    assert 'source_timestamp' in transformed_data[0]
    assert 'raw_id' in transformed_data[0]
    assert 'validation_status' in transformed_data[0]

@pytest.mark.asyncio
async def test_load(sample_data):
    loader = DataLoader('test_source')
    
    # Mock the database manager
    async def mock_insert(*args, **kwargs):
        return 1
    
    from utils.db import DatabaseManager
    DatabaseManager.insert_bronze_data = mock_insert
    
    results = await loader.load(sample_data)
    
    assert results['total_records'] == len(sample_data)
    assert results['successful_records'] == len(sample_data)
    assert results['failed_records'] == 0
    assert len(results['errors']) == 0 