"""
Multimodal Fusion Engine
Combines audio and video stress scores for final stress estimation
"""
import numpy as np
import config


class MultimodalFusion:
    """Fuses audio and video modalities for robust stress detection"""
    
    def __init__(self):
        self.audio_weight = config.AUDIO_WEIGHT
        self.video_weight = config.VIDEO_WEIGHT
        
    def fuse_stress_scores(self, audio_result=None, video_result=None):
        """
        Fuse audio and video stress scores
        
        Args:
            audio_result: Dictionary with audio stress analysis
                {
                    'stress_score': float,
                    'stress_level': str,
                    'confidence': float,
                    'emotion': str,
                    ...
                }
            video_result: Dictionary with video stress analysis (same structure)
            
        Returns:
            Dictionary with fused results
        """
        # Handle cases where one modality is missing
        if audio_result is None and video_result is None:
            return self._get_default_result()
        
        if audio_result is None:
            return self._single_modality_result(video_result, 'video')
        
        if video_result is None:
            return self._single_modality_result(audio_result, 'audio')
        
        # Both modalities available - perform fusion
        return self._dual_modality_fusion(audio_result, video_result)
    
    def _dual_modality_fusion(self, audio_result, video_result):
        """
        Fuse both audio and video modalities
        
        Args:
            audio_result: Audio stress analysis
            video_result: Video stress analysis
            
        Returns:
            Fused stress analysis
        """
        # Extract stress scores and confidences
        audio_stress = audio_result.get('stress_score', 0.5)
        audio_conf = audio_result.get('confidence', 0.5)
        
        video_stress = video_result.get('stress_score', 0.5)
        video_conf = video_result.get('confidence', 0.5)
        
        # Dynamic weight adjustment based on confidence
        # More confident modality gets higher weight
        total_conf = audio_conf + video_conf
        if total_conf > 0:
            dynamic_audio_weight = audio_conf / total_conf
            dynamic_video_weight = video_conf / total_conf
        else:
            dynamic_audio_weight = 0.5
            dynamic_video_weight = 0.5
        
        # Fuse stress scores using confidence-weighted average
        fused_stress = (
            dynamic_audio_weight * audio_stress +
            dynamic_video_weight * video_stress
        )
        
        # Overall confidence is average of both
        fused_confidence = (audio_conf + video_conf) / 2
        
        # Classify fused stress level
        fused_level = self._classify_stress_level(fused_stress)
        
        # Determine dominant modality
        if abs(audio_stress - video_stress) < 0.1:
            agreement = 'high'
        elif abs(audio_stress - video_stress) < 0.3:
            agreement = 'medium'
        else:
            agreement = 'low'
        
        # Combine emotions
        audio_emotion = audio_result.get('emotion', 'neutral')
        video_emotion = video_result.get('emotion', 'neutral')
        
        # Create fused result
        fused_result = {
            'stress_score': float(fused_stress),
            'stress_level': fused_level,
            'confidence': float(fused_confidence),
            'modalities_used': ['audio', 'video'],
            'audio': {
                'stress_score': float(audio_stress),
                'emotion': audio_emotion,
                'confidence': float(audio_conf),
                'stress_level': audio_result.get('stress_level', 'Medium')
            },
            'video': {
                'stress_score': float(video_stress),
                'emotion': video_emotion,
                'confidence': float(video_conf),
                'stress_level': video_result.get('stress_level', 'Medium')
            },
            'fusion_method': 'confidence_weighted_average',
            'modality_agreement': agreement,
            'weights': {
                'audio': float(dynamic_audio_weight),
                'video': float(dynamic_video_weight)
            }
        }
        
        return fused_result
    
    def _single_modality_result(self, result, modality):
        """
        Process single modality result
        
        Args:
            result: Stress analysis result
            modality: 'audio' or 'video'
            
        Returns:
            Formatted result
        """
        stress_score = result.get('stress_score', 0.5)
        confidence = result.get('confidence', 0.5)
        emotion = result.get('emotion', 'neutral')
        stress_level = result.get('stress_level', 'Medium')
        
        return {
            'stress_score': float(stress_score),
            'stress_level': stress_level,
            'confidence': float(confidence),
            'modalities_used': [modality],
            modality: {
                'stress_score': float(stress_score),
                'emotion': emotion,
                'confidence': float(confidence),
                'stress_level': stress_level
            },
            'fusion_method': 'single_modality',
            'modality_agreement': 'N/A'
        }
    
    def _get_default_result(self):
        """Return default result when no modalities available"""
        return {
            'stress_score': 0.5,
            'stress_level': 'Medium',
            'confidence': 0.0,
            'modalities_used': [],
            'fusion_method': 'none',
            'modality_agreement': 'N/A',
            'error': 'No modality data available'
        }
    
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
