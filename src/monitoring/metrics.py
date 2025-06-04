"""
Metrics collection module for monitoring data ingestion processes.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
import logging
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Configure logging
logger = logging.getLogger(__name__)

# Prometheus metrics
INGESTION_COUNTER = Counter(
    'data_ingestion_total',
    'Total number of data ingestion attempts',
    ['source', 'status']
)

INGESTION_DURATION = Histogram(
    'data_ingestion_duration_seconds',
    'Time spent on data ingestion',
    ['source']
)

DATA_VOLUME = Gauge(
    'data_ingestion_volume_bytes',
    'Volume of data ingested',
    ['source']
)

ERROR_COUNTER = Counter(
    'data_ingestion_errors_total',
    'Total number of errors during ingestion',
    ['source', 'error_type']
)

class MetricsCollector:
    """Class for collecting and managing metrics."""
    
    def __init__(self, prometheus_client=None):
        self.prometheus_client = prometheus_client or {
            'Counter': Counter,
            'Gauge': Gauge,
            'Histogram': Histogram
        }
        
        # Initialize metrics
        self.ingestion_counter = self.prometheus_client['Counter'](
            'data_ingestion_total',
            'Total number of data ingestion attempts',
            ['source', 'status']
        )
        
        self.processing_time_histogram = self.prometheus_client['Histogram'](
            'data_ingestion_duration_seconds',
            'Time spent on data ingestion',
            ['source']
        )
        
        self.data_quality_gauge = self.prometheus_client['Gauge'](
            'data_quality_score',
            'Quality score of ingested data',
            ['source']
        )

    def record_ingestion(self, source: str, records: int) -> None:
        """Record ingestion metrics."""
        self.ingestion_counter.labels(source=source, status='success').inc()

    def record_processing_time(self, source: str, start_time: datetime, end_time: datetime) -> None:
        """Record processing time metrics."""
        duration = (end_time - start_time).total_seconds()
        self.processing_time_histogram.labels(source=source).observe(duration)

    def record_data_quality(self, source: str, quality_score: float) -> None:
        """Record data quality metrics."""
        self.data_quality_gauge.labels(source=source).set(quality_score)

def start_metrics_server(port: int = 8000) -> None:
    """Start the Prometheus metrics server."""
    try:
        start_http_server(port)
        logger.info(f"Metrics server started on port {port}")
    except Exception as e:
        logger.error(f"Failed to start metrics server: {e}")

def record_validation_metrics(source: str, valid: bool, error_type: Optional[str] = None) -> None:
    """Record validation metrics."""
    status = "valid" if valid else "invalid"
    INGESTION_COUNTER.labels(source=source, status=status).inc()
    if not valid and error_type:
        ERROR_COUNTER.labels(source=source, error_type=error_type).inc()

def get_metrics_summary() -> Dict[str, Any]:
    """Get a summary of current metrics."""
    return {
        "ingestion_total": INGESTION_COUNTER._value.get(),
        "error_total": ERROR_COUNTER._value.get(),
        "data_volume": DATA_VOLUME._value.get()
    } 