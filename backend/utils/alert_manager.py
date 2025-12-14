"""
Alert Manager
Monitors stress levels and triggers alerts
"""
import time
from collections import deque
import config


class AlertManager:
    """Manages stress alerts and notifications"""
    
    def __init__(self):
        self.high_stress_threshold = config.ALERT_HIGH_STRESS_THRESHOLD
        self.high_stress_duration = config.ALERT_HIGH_STRESS_DURATION
        self.spike_threshold = config.ALERT_SPIKE_THRESHOLD
        self.spike_window = config.ALERT_SPIKE_WINDOW
        
        # Track stress history for each session
        self.session_history = {}
        self.active_alerts = {}
        
    def check_alerts(self, session_id, stress_score, timestamp=None):
        """
        Check if any alert conditions are met
        
        Args:
            session_id: Unique session identifier
            stress_score: Current stress score
            timestamp: Current timestamp (default: current time)
            
        Returns:
            List of alert dictionaries
        """
        if timestamp is None:
            timestamp = time.time()
        
        # Initialize session history if needed
        if session_id not in self.session_history:
            self.session_history[session_id] = deque(maxlen=1000)
            self.active_alerts[session_id] = {}
        
        # Add current score to history
        self.session_history[session_id].append({
            'score': stress_score,
            'timestamp': timestamp
        })
        
        alerts = []
        
        # Check for sustained high stress
        sustained_alert = self._check_sustained_high_stress(session_id, timestamp)
        if sustained_alert:
            alerts.append(sustained_alert)
        
        # Check for sudden stress spike
        spike_alert = self._check_stress_spike(session_id)
        if spike_alert:
            alerts.append(spike_alert)
        
        return alerts
    
    def _check_sustained_high_stress(self, session_id, current_time):
        """
        Check if stress has been high for sustained period
        
        Args:
            session_id: Session identifier
            current_time: Current timestamp
            
        Returns:
            Alert dictionary if condition met, None otherwise
        """
        history = self.session_history[session_id]
        
        # Get entries from last N seconds
        cutoff_time = current_time - self.high_stress_duration
        recent_high = [
            entry for entry in history
            if entry['timestamp'] >= cutoff_time and entry['score'] >= self.high_stress_threshold
        ]
        
        # Check if all entries in duration window are high stress
        total_recent = [entry for entry in history if entry['timestamp'] >= cutoff_time]
        
        if len(total_recent) > 0:
            high_ratio = len(recent_high) / len(total_recent)
            
            # Alert if >80% of recent entries are high stress
            if high_ratio >= 0.8:
                alert_key = 'sustained_high_stress'
                
                # Only trigger once (don't spam)
                if alert_key not in self.active_alerts[session_id]:
                    self.active_alerts[session_id][alert_key] = current_time
                    
                    return {
                        'type': 'sustained_high_stress',
                        'severity': 'high',
                        'title': 'Prolonged High Stress Detected',
                        'message': f'Worker has shown high stress levels for over {self.high_stress_duration // 60} minutes',
                        'timestamp': current_time,
                        'recommendations': [
                            'Suggest taking a 5-10 minute break',
                            'Practice deep breathing exercises',
                            'Consider reassigning tasks if workload is overwhelming',
                            'Notify supervisor for support'
                        ],
                        'priority': 'urgent'
                    }
        
        return None
    
    def _check_stress_spike(self, session_id):
        """
        Check for sudden stress spike
        
        Args:
            session_id: Session identifier
            
        Returns:
            Alert dictionary if condition met, None otherwise
        """
        history = list(self.session_history[session_id])
        
        if len(history) < 2:
            return None
        
        # Compare current to recent average
        current = history[-1]['score']
        
        # Get scores from spike window
        window_size = min(5, len(history) - 1)
        previous_scores = [history[i]['score'] for i in range(-window_size-1, -1)]
        previous_avg = sum(previous_scores) / len(previous_scores)
        
        spike = current - previous_avg
        
        if spike >= self.spike_threshold:
            alert_key = f'spike_{int(history[-1]["timestamp"])}'
            
            # Only trigger once per spike
            if alert_key not in self.active_alerts[session_id]:
                self.active_alerts[session_id][alert_key] = history[-1]['timestamp']
                
                return {
                    'type': 'sudden_stress_spike',
                    'severity': 'medium',
                    'title': 'Sudden Stress Increase Detected',
                    'message': f'Stress level increased by {spike:.2f} in a short period',
                    'timestamp': history[-1]['timestamp'],
                    'recommendations': [
                        'Check if a specific event triggered the stress',
                        'Offer immediate support or intervention',
                        'Monitor closely for the next few minutes'
                    ],
                    'priority': 'high'
                }
        
        return None
    
    def clear_session(self, session_id):
        """Clear history and alerts for a session"""
        if session_id in self.session_history:
            del self.session_history[session_id]
        if session_id in self.active_alerts:
            del self.active_alerts[session_id]
    
    def get_alert_history(self, session_id, limit=10):
        """Get recent alerts for a session"""
        if session_id not in self.active_alerts:
            return []
        
        # Return recent alerts (simplified - in production, maintain separate history)
        return list(self.active_alerts[session_id].keys())[:limit]
