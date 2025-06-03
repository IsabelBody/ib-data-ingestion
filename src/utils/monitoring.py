import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        self.metrics = {}
        self.alert_thresholds = {
            'error_rate': 0.05,  # 5% error rate threshold
            'latency': 2.0,      # 2 seconds latency threshold
            'data_quality': 0.99  # 99% data quality threshold
        }

    def record_ingestion_metrics(self, source: str, metrics: Dict[str, Any]) -> None:
        """Record metrics for a data ingestion operation."""
        if source not in self.metrics:
            self.metrics[source] = {
                'total_records': 0,
                'error_count': 0,
                'last_updated': None,
                'latency': []
            }
        
        self.metrics[source]['total_records'] += metrics.get('records_processed', 0)
        self.metrics[source]['error_count'] += metrics.get('errors', 0)
        self.metrics[source]['last_updated'] = datetime.now()
        
        if 'latency' in metrics:
            self.metrics[source]['latency'].append(metrics['latency'])
            # Keep only last 100 latency measurements
            self.metrics[source]['latency'] = self.metrics[source]['latency'][-100:]
        
        self._check_alerts(source)

    def _check_alerts(self, source: str) -> None:
        """Check if any metrics exceed alert thresholds."""
        metrics = self.metrics[source]
        
        # Calculate error rate
        if metrics['total_records'] > 0:
            error_rate = metrics['error_count'] / metrics['total_records']
            if error_rate > self.alert_thresholds['error_rate']:
                logger.warning(
                    f"High error rate detected for {source}: {error_rate:.2%}"
                )
        
        # Check latency
        if metrics['latency']:
            avg_latency = sum(metrics['latency']) / len(metrics['latency'])
            if avg_latency > self.alert_thresholds['latency']:
                logger.warning(
                    f"High latency detected for {source}: {avg_latency:.2f}s"
                )

    def get_metrics(self, source: str) -> Dict[str, Any]:
        """Get current metrics for a source."""
        return self.metrics.get(source, {})

    def reset_metrics(self, source: str) -> None:
        """Reset metrics for a source."""
        if source in self.metrics:
            self.metrics[source] = {
                'total_records': 0,
                'error_count': 0,
                'last_updated': None,
                'latency': []
            } 