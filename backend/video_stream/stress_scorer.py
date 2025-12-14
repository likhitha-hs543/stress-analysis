"""
Video Stress Scorer
Converts facial emotion predictions to stress scores
"""
import numpy as np
import config


class VideoStressScorer:
    """Calculates stress score from facial emotion predictions and features"""
    
    def __init__(self):
        self.emotion_stress_weights = config.EMOTION_STRESS_WEIGHTS
        
    def calculate_stress_score(self, emotion, emotion_probabilities, confidence, facial_features=None):
        """
        Calculate stress score from facial emotion prediction and features
        
        Args:
            emotion: Predicted emotion label (str)
            emotion_probabilities: Dictionary of {emotion: probability}
            confidence: Model confidence score
            facial_features: Optional dictionary of geometric features
            
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
        
        # Method 3: Use facial features if available
        feature_stress = 0.5
        if facial_features:
            feature_stress = self._calculate_feature_based_stress(facial_features)
        
        # Combine all methods
        # 30% primary emotion, 40% weighted emotions, 30% facial features
        combined_stress = (
            0.3 * primary_stress +
            0.4 * weighted_stress +
            0.3 * feature_stress
        )
        
        # Adjust by confidence (low confidence -> move towards neutral 0.5)
        confidence_adjusted_stress = combined_stress * confidence + 0.5 * (1 - confidence)
        
        # Clip to [0, 1] range
        stress_score = np.clip(confidence_adjusted_stress, 0.0, 1.0)
        
        # Determine stress level
        stress_level = self._classify_stress_level(stress_score)
        
        # Create details dictionary
        details = {
            'primary_emotion': emotion,
            'emotion_stress': primary_stress,
            'weighted_stress': weighted_stress,
            'feature_stress': feature_stress,
            'confidence': confidence,
            'final_stress_score': float(stress_score),
            'stress_level': stress_level,
            'emotion_probabilities': emotion_probabilities
        }
        
        if facial_features:
            details['facial_features'] = facial_features
        
        return float(stress_score), stress_level, details
    
    def _calculate_feature_based_stress(self, features):
        """
        Calculate stress from geometric facial features
        
        Args:
            features: Dictionary of facial features
            
        Returns:
            Stress score based on features
        """
        stress_indicators = []
        
        # Eye strain indicator
        eye_strain = features.get('eye_strain', 0.0)
        stress_indicators.append(eye_strain)
        
        # Facial tension
        tension = features.get('facial_tension', 0.0)
        stress_indicators.append(tension)
        
        # Low eye openness (fatigue/stress)
        eye_openness = features.get('avg_eye_openness', 0.2)
        if eye_openness < 0.15:
            stress_indicators.append(0.7)
        elif eye_openness < 0.2:
            stress_indicators.append(0.4)
        else:
            stress_indicators.append(0.1)
        
        # High eyebrow position (surprise/fear/stress)
        eyebrow = features.get('avg_eyebrow_height', 0.05)
        eyebrow_stress = min(eyebrow * 10, 1.0)
        stress_indicators.append(eyebrow_stress)
        
        # Facial asymmetry (stress indicator)
        symmetry = features.get('facial_symmetry', 0.8)
        asymmetry_stress = 1.0 - symmetry
        stress_indicators.append(asymmetry_stress)
        
        # Extreme head poses (discomfort)
        pitch = abs(features.get('head_pitch', 0.0))
        yaw = abs(features.get('head_yaw', 0.0))
        if pitch > 20 or yaw > 20:
            stress_indicators.append(0.6)
        else:
            stress_indicators.append(0.2)
        
        # Average all indicators
        if stress_indicators:
            feature_stress = np.mean(stress_indicators)
        else:
            feature_stress = 0.5
        
        return float(np.clip(feature_stress, 0.0, 1.0))
    
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
