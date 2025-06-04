import pytest
from unittest.mock import Mock, patch
from monitoring.metrics import MetricsCollector
from monitoring.health import HealthChecker
from monitoring.alerts import AlertManager
from datetime import datetime

@pytest.fixture
def mock_prometheus_client():
    mock_client = {
        'Counter': Mock(return_value=Mock()),
        'Gauge': Mock(return_value=Mock()),
        'Histogram': Mock(return_value=Mock())
    }
    return mock_client

@pytest.fixture
def metrics_collector(mock_prometheus_client):
    return MetricsCollector(mock_prometheus_client)

@pytest.fixture
def health_check(test_config):
    return HealthChecker(test_config)

@pytest.fixture
def alert_manager():
    return AlertManager()

def test_metrics_collector_initialization(metrics_collector):
    assert metrics_collector.prometheus_client is not None
    assert metrics_collector.ingestion_counter is not None
    assert metrics_collector.processing_time_histogram is not None
    assert metrics_collector.data_quality_gauge is not None

def test_record_ingestion(metrics_collector):
    metrics_collector.record_ingestion('test_source', 10)
    metrics_collector.ingestion_counter.labels.assert_called_once_with(
        source='test_source',
        status='success'
    )

def test_record_processing_time(metrics_collector):
    start_time = datetime.utcnow()
    end_time = datetime.utcnow()
    metrics_collector.record_processing_time('test_source', start_time, end_time)
    metrics_collector.processing_time_histogram.labels.assert_called_once_with(
        source='test_source'
    )

def test_record_data_quality(metrics_collector):
    metrics_collector.record_data_quality('test_source', 0.95)
    metrics_collector.data_quality_gauge.labels.assert_called_once_with(
        source='test_source'
    )

def test_health_check_initialization(health_check):
    assert health_check.config is not None
    assert health_check.is_healthy is True

def test_health_check_database(health_check, mock_db_connection):
    health_check.check_database(mock_db_connection)
    assert health_check.is_healthy is True
    mock_db_connection.execute.assert_called_once()

def test_health_check_database_failure(health_check, mock_db_connection):
    mock_db_connection.execute.side_effect = Exception("Database error")
    health_check.check_database(mock_db_connection)
    assert health_check.is_healthy is False

def test_alert_manager_initialization(alert_manager):
    assert alert_manager.alerts == []

def test_create_alert(alert_manager):
    alert = alert_manager.create_alert(
        source='test_source',
        level='error',
        message='Test error message'
    )
    assert alert['source'] == 'test_source'
    assert alert['level'] == 'error'
    assert alert['message'] == 'Test error message'
    assert 'timestamp' in alert
    assert len(alert_manager.alerts) == 1

def test_get_alerts(alert_manager):
    alert_manager.create_alert(
        source='test_source',
        level='error',
        message='Test error message'
    )
    alerts = alert_manager.get_alerts()
    assert len(alerts) == 1
    assert alerts[0]['source'] == 'test_source'

def test_clear_alerts(alert_manager):
    alert_manager.create_alert(
        source='test_source',
        level='error',
        message='Test error message'
    )
    alert_manager.clear_alerts()
    assert len(alert_manager.alerts) == 0 