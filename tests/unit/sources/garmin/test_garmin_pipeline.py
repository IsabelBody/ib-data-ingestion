import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from src.pipelines.sources.garmin.extract import GarminExtractor
from src.pipelines.sources.garmin.transform import GarminTransformer
from src.pipelines.sources.garmin.load import GarminLoader

@pytest.fixture
def mock_garmin_client():
    with patch('garminconnect.Garmin') as mock:
        client = Mock()
        # Mock the activities data
        client.get_activities.return_value = [{
            'activityId': '123',
            'activityName': 'Morning Run',
            'startTime': '2024-03-20T06:00:00.0',
            'duration': 3600,
            'distance': 5000,
            'averageHeartRate': 150,
            'maxHeartRate': 180,
            'calories': 500,
            'averageSpeed': 5.0,
            'maxSpeed': 6.0,
            'averagePace': 7.2,
            'maxPace': 6.5,
            'elevationGain': 100,
            'elevationLoss': 100,
            'deviceName': 'Forerunner 255',
            'activityType': 'running'
        }]
        # Mock the sleep data
        client.get_sleep_data.return_value = {
            'dailySleepDTO': {
                'calendarDate': '2024-03-20',
                'sleepTimeSeconds': 28800,
                'deepSleepSeconds': 7200,
                'lightSleepSeconds': 14400,
                'remSleepSeconds': 7200,
                'awakeSleepSeconds': 0,
                'sleepStartTimestampGMT': '2024-03-20T22:00:00.0',
                'sleepEndTimestampGMT': '2024-03-21T06:00:00.0',
                'sleepStartTimestampLocal': '2024-03-20T22:00:00.0',
                'sleepEndTimestampLocal': '2024-03-21T06:00:00.0',
                'averageSleepStress': 10,
                'sleepScores': {
                    'overall': 85,
                    'deep': 90,
                    'rem': 80,
                    'light': 85
                }
            }
        }
        mock.return_value = client
        yield client

@pytest.fixture
def extractor(mock_garmin_client):
    return GarminExtractor()

@pytest.fixture
def transformer():
    return GarminTransformer()

@pytest.fixture
def loader():
    return GarminLoader()

def test_extract_activities(extractor, mock_garmin_client):
    # Test extracting activities
    activities = extractor.extract_activities()
    assert len(activities) == 1
    assert activities[0]['activityId'] == '123'
    assert activities[0]['activityName'] == 'Morning Run'
    mock_garmin_client.get_activities.assert_called_once()

def test_extract_sleep(extractor, mock_garmin_client):
    # Test extracting sleep data
    sleep_data = extractor.extract_sleep()
    assert sleep_data['dailySleepDTO']['calendarDate'] == '2024-03-20'
    assert sleep_data['dailySleepDTO']['sleepTimeSeconds'] == 28800
    mock_garmin_client.get_sleep_data.assert_called_once()

def test_transform_activity(transformer):
    # Test transforming activity data
    raw_activity = {
        'activityId': '123',
        'activityName': 'Morning Run',
        'startTime': '2024-03-20T06:00:00.0',
        'duration': 3600,
        'distance': 5000,
        'averageHeartRate': 150,
        'maxHeartRate': 180,
        'calories': 500,
        'averageSpeed': 5.0,
        'maxSpeed': 6.0,
        'averagePace': 7.2,
        'maxPace': 6.5,
        'elevationGain': 100,
        'elevationLoss': 100,
        'deviceName': 'Forerunner 255',
        'activityType': 'running'
    }
    
    transformed = transformer.transform_activity(raw_activity)
    assert transformed['source'] == 'garmin'
    assert transformed['data_type'] == 'activity'
    assert transformed['source_timestamp'] == '2024-03-20T06:00:00.0'
    assert transformed['validation_status'] == 'valid'
    assert 'raw_data' in transformed
    assert 'metadata' in transformed

def test_transform_sleep(transformer):
    # Test transforming sleep data
    raw_sleep = {
        'dailySleepDTO': {
            'calendarDate': '2024-03-20',
            'sleepTimeSeconds': 28800,
            'deepSleepSeconds': 7200,
            'lightSleepSeconds': 14400,
            'remSleepSeconds': 7200,
            'awakeSleepSeconds': 0,
            'sleepStartTimestampGMT': '2024-03-20T22:00:00.0',
            'sleepEndTimestampGMT': '2024-03-21T06:00:00.0',
            'sleepStartTimestampLocal': '2024-03-20T22:00:00.0',
            'sleepEndTimestampLocal': '2024-03-21T06:00:00.0',
            'averageSleepStress': 10,
            'sleepScores': {
                'overall': 85,
                'deep': 90,
                'rem': 80,
                'light': 85
            }
        }
    }
    
    transformed = transformer.transform_sleep(raw_sleep)
    assert transformed['source'] == 'garmin'
    assert transformed['data_type'] == 'sleep'
    assert transformed['source_timestamp'] == '2024-03-20T22:00:00.0'
    assert transformed['validation_status'] == 'valid'
    assert 'raw_data' in transformed
    assert 'metadata' in transformed

def test_load_data(loader):
    # Test loading data to database
    test_data = {
        'source': 'garmin',
        'data_type': 'activity',
        'source_timestamp': '2024-03-20T06:00:00.0',
        'validation_status': 'valid',
        'raw_data': {'activityId': '123'},
        'metadata': {'device': 'Forerunner 255'}
    }
    
    with patch('src.utils.db.get_db_connection') as mock_db:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        loader.load(test_data)
        
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once() 