"""
Audio Stress Scorer
Converts emotion predictions to stress scores
"""
import numpy as np
import config


class AudioStressScorer:
    """Calculates stress score from audio emotion predictions"""
    
    def __init__(self):
        self.emotion_stress_weights = config.EMOTION_STRESS_WEIGHTS
        
    def calculate_stress_score(self, emotion, emotion_probabilities, confidence):
        """
        Calculate stress score from emotion prediction
        
        Args:
            emotion: Predicted emotion label (str)
            emotion_probabilities: Dictionary of {emotion: probability}
            confidence: Model confidence score
            
        Returns:
            Tuple of (stress_score, stress_level, details)
        """
        # Method 1: Simple mapping from predicted emotion
        primary_stress = self.emotion_stress_weights.get(emotion, 0.5)
        
        # Method 2: Weighted average of all emotion probabilities
        weighted_stress = 0.0
        for emo, prob in emotion_probabilities.items():
            stress_weight = self.emotion_stress_weights.get(emo, 0.5)
            weighted_stress += prob * stress_weight
        
        # Combine both methods (favor weighted average)
        final_stress = 0.3 * primary_stress + 0.7 * weighted_stress
        
        # Adjust by confidence (low confidence -> move towards neutral 0.5)
        confidence_adjusted_stress = final_stress * confidence + 0.5 * (1 - confidence)
        
        # Clip to [0, 1] range
        stress_score = np.clip(confidence_adjusted_stress, 0.0, 1.0)
        
        # Determine stress level
        stress_level = self._classify_stress_level(stress_score)
        
        # Create details dictionary
        details = {
            'primary_emotion': emotion,
            'emotion_stress': primary_stress,
            'weighted_stress': weighted_stress,
            'confidence': confidence,
            'final_stress_score': float(stress_score),
            'stress_level': stress_level,
            'emotion_probabilities': emotion_probabilities
        }
        
        return float(stress_score), stress_level, details
    
    def _classify_stress_level(self, stress_score):
        """
        Classify stress score into categorical level
        
        Args:
            stress_score: Continuous stress score [0, 1]
            
        Returns:
            Stress level: 'Low', 'Medium', or 'High'
        """
        if stress_score < config.STRESS_LOW_THRESHOLD:
            return 'Low'
        elif stress_score < config.STRESS_HIGH_THRESHOLD:
            return 'Medium'
        else:
            return 'High'
    
    def aggregate_stress_scores(self, stress_scores, window_size=5):
        """
        Aggregate multiple stress scores over time window
        
        Args:
            stress_scores: List of recent stress scores
            window_size: Number of recent scores to consider
            
        Returns:
            Aggregated stress score
        """
        if not stress_scores:
            return 0.5
        
        # Take last N scores
        recent_scores = stress_scores[-window_size:]
        
        # Calculate weighted average (more recent = higher weight)
        weights = np.exp(np.linspace(0, 1, len(recent_scores)))
        weights = weights / np.sum(weights)
        
        aggregated = np.average(recent_scores, weights=weights)
        
        return float(aggregated)
