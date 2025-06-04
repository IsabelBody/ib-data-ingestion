"""
Health check module for monitoring system components.
"""
import logging
from typing import Dict, Any, List
import psycopg2
from datetime import datetime
import requests
from prometheus_client import Gauge

# Configure logging
logger = logging.getLogger(__name__)

# Health check metrics
HEALTH_STATUS = Gauge(
    'system_health_status',
    'Health status of system components',
    ['component']
)

class HealthChecker:
    """Class for performing health checks on system components."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.is_healthy = True
        self.components = {
            'database': self.check_database,
            'api': self.check_api,
            'storage': self.check_storage
        }
    
    def check_database(self, connection) -> Dict[str, Any]:
        """Check database health."""
        try:
            connection.execute('SELECT 1')
            HEALTH_STATUS.labels(component='database').set(1)
            self.is_healthy = True
            return {
                'status': 'healthy',
                'message': 'Database connection successful',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            HEALTH_STATUS.labels(component='database').set(0)
            self.is_healthy = False
            return {
                'status': 'unhealthy',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_api(self) -> Dict[str, Any]:
        """Check API health."""
        try:
            # Add your API health check logic here
            response = requests.get('http://localhost:8000/health')
            if response.status_code == 200:
                HEALTH_STATUS.labels(component='api').set(1)
                self.is_healthy = True
                return {
                    'status': 'healthy',
                    'message': 'API is responding',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                raise Exception(f"API returned status code {response.status_code}")
        except Exception as e:
            logger.error(f"API health check failed: {e}")
            HEALTH_STATUS.labels(component='api').set(0)
            self.is_healthy = False
            return {
                'status': 'unhealthy',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_storage(self) -> Dict[str, Any]:
        """Check storage health."""
        try:
            # Add your storage health check logic here
            # This is a placeholder implementation
            HEALTH_STATUS.labels(component='storage').set(1)
            self.is_healthy = True
            return {
                'status': 'healthy',
                'message': 'Storage is accessible',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Storage health check failed: {e}")
            HEALTH_STATUS.labels(component='storage').set(0)
            self.is_healthy = False
            return {
                'status': 'unhealthy',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks and return results."""
        results = {}
        for component, check_func in self.components.items():
            results[component] = check_func()
        return results
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get a summary of system health."""
        results = self.run_all_checks()
        all_healthy = all(r['status'] == 'healthy' for r in results.values())
        
        return {
            'overall_status': 'healthy' if all_healthy else 'unhealthy',
            'components': results,
            'timestamp': datetime.now().isoformat()
        } 