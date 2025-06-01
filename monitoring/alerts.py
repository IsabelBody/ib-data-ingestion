from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from utils.logger import logger

class AlertManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.alert_thresholds = {
            'error_rate': 0.05,  # 5% error rate threshold
            'latency': 300,      # 5 minutes latency threshold
            'data_quality': 0.8,  # 80% quality score threshold
            'resource_utilization': {
                'cpu': 0.8,      # 80% CPU utilization threshold
                'memory': 0.85,  # 85% memory utilization threshold
                'disk': 0.85     # 85% disk utilization threshold
            }
        }
        self.alert_history: List[Dict[str, Any]] = []
    
    def check_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check metrics against thresholds and generate alerts."""
        alerts = []
        
        # Check error rate
        if metrics.get('error_rate', 0) > self.alert_thresholds['error_rate']:
            alerts.append({
                'level': 'ERROR',
                'message': f'High error rate detected: {metrics["error_rate"]:.2%}',
                'metric': 'error_rate',
                'value': metrics['error_rate'],
                'threshold': self.alert_thresholds['error_rate']
            })
        
        # Check latency
        if metrics.get('latency', 0) > self.alert_thresholds['latency']:
            alerts.append({
                'level': 'WARNING',
                'message': f'High latency detected: {metrics["latency"]} seconds',
                'metric': 'latency',
                'value': metrics['latency'],
                'threshold': self.alert_thresholds['latency']
            })
        
        # Check data quality
        if metrics.get('quality_score', 1.0) < self.alert_thresholds['data_quality']:
            alerts.append({
                'level': 'WARNING',
                'message': f'Low data quality score: {metrics["quality_score"]:.2f}',
                'metric': 'quality_score',
                'value': metrics['quality_score'],
                'threshold': self.alert_thresholds['data_quality']
            })
        
        # Check resource utilization
        for resource, threshold in self.alert_thresholds['resource_utilization'].items():
            if metrics.get(f'{resource}_utilization', 0) > threshold:
                alerts.append({
                    'level': 'WARNING',
                    'message': f'High {resource} utilization: {metrics[f"{resource}_utilization"]:.2%}',
                    'metric': f'{resource}_utilization',
                    'value': metrics[f'{resource}_utilization'],
                    'threshold': threshold
                })
        
        # Process alerts
        for alert in alerts:
            self._process_alert(alert)
        
        return alerts
    
    def _process_alert(self, alert: Dict[str, Any]):
        """Process an alert by logging and sending notifications."""
        # Add timestamp
        alert['timestamp'] = datetime.utcnow().isoformat()
        
        # Log alert
        if alert['level'] == 'ERROR':
            logger.error(
                alert['message'],
                metric=alert['metric'],
                value=alert['value'],
                threshold=alert['threshold']
            )
        else:
            logger.warning(
                alert['message'],
                metric=alert['metric'],
                value=alert['value'],
                threshold=alert['threshold']
            )
        
        # Store in history
        self.alert_history.append(alert)
        
        # Send notification if configured
        if self.config.get('enable_notifications', False):
            self._send_notification(alert)
    
    def _send_notification(self, alert: Dict[str, Any]):
        """Send alert notification via email."""
        if not self.config.get('smtp_config'):
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['smtp_config']['from_email']
            msg['To'] = self.config['smtp_config']['to_email']
            msg['Subject'] = f"[{alert['level']}] Data Pipeline Alert"
            
            body = f"""
            Alert Details:
            Level: {alert['level']}
            Message: {alert['message']}
            Metric: {alert['metric']}
            Value: {alert['value']}
            Threshold: {alert['threshold']}
            Timestamp: {alert['timestamp']}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(
                self.config['smtp_config']['smtp_server'],
                self.config['smtp_config']['smtp_port']
            ) as server:
                server.starttls()
                server.login(
                    self.config['smtp_config']['username'],
                    self.config['smtp_config']['password']
                )
                server.send_message(msg)
                
        except Exception as e:
            logger.error(
                "Failed to send alert notification",
                error=str(e)
            )
    
    def get_alert_history(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get alert history with optional filtering."""
        filtered_alerts = self.alert_history
        
        if start_time:
            filtered_alerts = [
                alert for alert in filtered_alerts
                if datetime.fromisoformat(alert['timestamp']) >= start_time
            ]
        
        if end_time:
            filtered_alerts = [
                alert for alert in filtered_alerts
                if datetime.fromisoformat(alert['timestamp']) <= end_time
            ]
        
        if level:
            filtered_alerts = [
                alert for alert in filtered_alerts
                if alert['level'] == level
            ]
        
        return filtered_alerts 