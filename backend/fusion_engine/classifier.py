"""
Stress Classifier
Final stress level classification and interpretation
"""
import config


class StressClassifier:
    """Classifies and interprets stress levels"""
    
    def __init__(self):
        self.low_threshold = config.STRESS_LOW_THRESHOLD
        self.high_threshold = config.STRESS_HIGH_THRESHOLD
        
    def classify(self, stress_score):
        """
        Classify stress score into categorical level
        
        Args:
            stress_score: Continuous stress score [0, 1]
            
        Returns:
            Dictionary with classification and interpretation
        """
        if stress_score < self.low_threshold:
            level = 'Low'
            color = 'green'
            description = 'Worker appears calm and relaxed'
            recommendation = 'Maintain current work conditions'
        elif stress_score < self.high_threshold:
            level = 'Medium'
            color = 'yellow'
            description = 'Worker shows moderate stress indicators'
            recommendation = 'Monitor closely for any changes'
        else:
            level = 'High'
            color = 'red'
            description = 'Worker shows elevated stress levels'
            recommendation = 'Suggest taking a break and assess workload'
        
        return {
            'level': level,
            'score': float(stress_score),
            'color': color,
            'description': description,
            'recommendation': recommendation
        }
    
    def get_stress_trend(self, stress_history, window=10):
        """
        Analyze stress trend over recent history
        
        Args:
            stress_history: List of recent stress scores
            window: Number of recent scores to analyze
            
        Returns:
            Dictionary with trend analysis
        """
        if not stress_history or len(stress_history) < 2:
            return {
                'trend': 'insufficient_data',
                'direction': 'neutral',
                'change': 0.0
            }
        
        # Get recent window
        recent = stress_history[-min(window, len(stress_history)):]
        
        # Calculate trend
        first_half = recent[:len(recent)//2]
        second_half = recent[len(recent)//2:]
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        change = avg_second - avg_first
        
        if abs(change) < 0.05:
            trend = 'stable'
            direction = 'neutral'
        elif change > 0:
            trend = 'increasing'
            direction = 'up'
        else:
            trend = 'decreasing'
            direction = 'down'
        
        return {
            'trend': trend,
            'direction': direction,
            'change': float(change),
            'recent_average': float(avg_second)
        }
