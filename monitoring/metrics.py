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

@dataclass
class IngestionMetrics:
    """Class for tracking ingestion metrics."""
    source: str
    start_time: datetime
    end_time: Optional[datetime] = None
    records_processed: int = 0
    bytes_processed: int = 0
    status: str = "in_progress"
    error_type: Optional[str] = None

    def complete(self, status: str = "success") -> None:
        """Mark ingestion as complete and record metrics."""
        self.end_time = datetime.now()
        self.status = status
        
        # Record metrics
        INGESTION_COUNTER.labels(source=self.source, status=status).inc()
        if self.end_time and self.start_time:
            duration = (self.end_time - self.start_time).total_seconds()
            INGESTION_DURATION.labels(source=self.source).observe(duration)
        DATA_VOLUME.labels(source=self.source).set(self.bytes_processed)
        
        if status == "error" and self.error_type:
            ERROR_COUNTER.labels(source=self.source, error_type=self.error_type).inc()

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