"""
Session Manager
Manages session data and analytics
"""
import time
import uuid
from collections import deque
import config


class SessionManager:
    """Manages worker sessions and stress analytics"""
    
    def __init__(self):
        self.sessions = {}
        self.max_history = config.SESSION_MAX_HISTORY
        
    def create_session(self, worker_id=None):
        """
        Create a new session
        
        Args:
            worker_id: Optional worker identifier
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            'session_id': session_id,
            'worker_id': worker_id or f'worker_{session_id[:8]}',
            'start_time': time.time(),
            'stress_history': deque(maxlen=self.max_history),
            'emotion_counts': {},
            'total_updates': 0,
            'current_stress': 0.5,
            'current_emotion': 'neutral',
            'status': 'active'
        }
        
        return session_id
    
    def update_session(self, session_id, fused_result):
        """
        Update session with new stress analysis result
        
        Args:
            session_id: Session identifier
            fused_result: Fused stress analysis result
            
        Returns:
            Updated session info
        """
        if session_id not in self.sessions:
            # Create session if it doesn't exist
            session_id = self.create_session()
        
        session = self.sessions[session_id]
        
        # Extract data from fused result
        stress_score = fused_result.get('stress_score', 0.5)
        stress_level = fused_result.get('stress_level', 'Medium')
        
        # Determine primary emotion
        audio_emotion = fused_result.get('audio', {}).get('emotion', 'neutral')
        video_emotion = fused_result.get('video', {}).get('emotion', 'neutral')
        primary_emotion = audio_emotion  # Prefer audio emotion
        
        # Add to history
        session['stress_history'].append({
            'timestamp': time.time(),
            'stress_score': stress_score,
            'stress_level': stress_level,
            'emotion': primary_emotion,
            'modalities': fused_result.get('modalities_used', [])
        })
        
        # Update emotion counts
        if primary_emotion in session['emotion_counts']:
            session['emotion_counts'][primary_emotion] += 1
        else:
            session['emotion_counts'][primary_emotion] = 1
        
        # Update current state
        session['current_stress'] = stress_score
        session['current_emotion'] = primary_emotion
        session['total_updates'] += 1
        
        # Determine status
        if stress_score >= config.ALERT_HIGH_STRESS_THRESHOLD:
            session['status'] = 'at_risk'
        else:
            session['status'] = 'normal'
        
        return self.get_session_info(session_id)
    
    def get_session_info(self, session_id):
        """
        Get comprehensive session information
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with session info and analytics
        """
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Calculate session duration
        duration = time.time() - session['start_time']
        
        # Calculate analytics
        analytics = self._calculate_analytics(session)
        
        return {
            'session_id': session['session_id'],
            'worker_id': session['worker_id'],
            'duration': duration,
            'duration_formatted': self._format_duration(duration),
            'status': session['status'],
            'current_stress': session['current_stress'],
            'current_emotion': session['current_emotion'],
            'total_updates': session['total_updates'],
            'analytics': analytics
        }
    
    def _calculate_analytics(self, session):
        """
        Calculate session analytics
        
        Args:
            session: Session dictionary
            
        Returns:
            Analytics dictionary
        """
        history = list(session['stress_history'])
        
        if not history:
            return {
                'average_stress': 0.5,
                'peak_stress': 0.5,
                'min_stress': 0.5,
                'stress_variance': 0.0,
                'emotion_distribution': {},
                'high_stress_percentage': 0.0
            }
        
        # Extract stress scores
        stress_scores = [entry['stress_score'] for entry in history]
        
        # Calculate statistics
        avg_stress = sum(stress_scores) / len(stress_scores)
        peak_stress = max(stress_scores)
        min_stress = min(stress_scores)
        
        # Calculate variance
        variance = sum((x - avg_stress) ** 2 for x in stress_scores) / len(stress_scores)
        
        # Calculate high stress percentage
        high_stress_count = sum(1 for score in stress_scores if score >= config.STRESS_HIGH_THRESHOLD)
        high_stress_pct = (high_stress_count / len(stress_scores)) * 100
        
        # Calculate emotion distribution
        total_emotions = sum(session['emotion_counts'].values())
        emotion_dist = {
            emotion: (count / total_emotions) * 100
            for emotion, count in session['emotion_counts'].items()
        }
        
        return {
            'average_stress': round(avg_stress, 3),
            'peak_stress': round(peak_stress, 3),
            'min_stress': round(min_stress, 3),
            'stress_variance': round(variance, 3),
            'emotion_distribution': emotion_dist,
            'high_stress_percentage': round(high_stress_pct, 1),
            'data_points': len(history)
        }
    
    def get_stress_timeline(self, session_id, limit=100):
        """
        Get stress timeline for visualization
        
        Args:
            session_id: Session identifier
            limit: Maximum number of data points
            
        Returns:
            List of timeline data points
        """
        if session_id not in self.sessions:
            return []
        
        history = list(self.sessions[session_id]['stress_history'])
        
        # Return last N points
        recent = history[-limit:] if len(history) > limit else history
        
        return [
            {
                'timestamp': entry['timestamp'],
                'stress_score': entry['stress_score'],
                'stress_level': entry['stress_level'],
                'emotion': entry['emotion']
            }
            for entry in recent
        ]
    
    def end_session(self, session_id):
        """End a session"""
        if session_id in self.sessions:
            self.sessions[session_id]['status'] = 'ended'
            self.sessions[session_id]['end_time'] = time.time()
    
    def delete_session(self, session_id):
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def _format_duration(self, seconds):
        """Format duration in human-readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
