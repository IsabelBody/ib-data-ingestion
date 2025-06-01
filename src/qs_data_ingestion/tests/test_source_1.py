import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import json

from pipelines.source_1.extract import DataExtractor
from pipelines.source_1.transform import DataTransformer
from pipelines.source_1.load import DataLoader, LoadResult

@pytest.fixture
def mock_credentials():
    return {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret"
    }

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def sample_data():
    return [
        {
            "id": "1",
            "timestamp": "2024-01-01T00:00:00Z",
            "data": {"key": "value"}
        },
        {
            "id": "2",
            "timestamp": "2024-01-01T01:00:00Z",
            "data": {"key": "value2"}
        }
    ]

@pytest.mark.asyncio
async def test_extract_data(mock_credentials):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_response = Mock()
        mock_response.json.return_value = {"items": sample_data()}
        mock_response.__aenter__.return_value = mock_response
        
        mock_session.return_value.get.return_value = mock_response
        
        extractor = DataExtractor(mock_credentials)
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 2)
        
        data = await extractor.fetch_data(start_date, end_date)
        assert len(data) == 2
        assert data[0]["id"] == "1"
        assert data[1]["id"] == "2"

def test_transform_data(sample_data):
    transformer = DataTransformer()
    transformed_data = transformer.transform(sample_data)
    
    assert len(transformed_data) == 2
    assert transformed_data[0]["source"] == "source_1"
    assert transformed_data[0]["raw_id"] == "1"
    assert transformed_data[0]["validation_status"] == "valid"

@pytest.mark.asyncio
async def test_load_data(mock_db, sample_data):
    transformer = DataTransformer()
    transformed_data = transformer.transform(sample_data)
    
    loader = DataLoader(mock_db)
    result = await loader.load(transformed_data)
    
    assert result.success
    assert result.records_processed == 2
    assert len(result.errors) == 0

@pytest.mark.asyncio
async def test_load_data_with_error(mock_db, sample_data):
    mock_db.execute.side_effect = Exception("Database error")
    
    transformer = DataTransformer()
    transformed_data = transformer.transform(sample_data)
    
    loader = DataLoader(mock_db)
    result = await loader.load(transformed_data)
    
    assert not result.success
    assert result.records_processed == 0
    assert len(result.errors) > 0 