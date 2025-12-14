"""
Video Feature Extractor
Extracts geometric facial features from landmarks
"""
import numpy as np
import config


class VideoFeatureExtractor:
    """Extracts facial features from landmarks for emotion analysis"""
    
    def __init__(self):
        # Eye landmark indices
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]
        
        # Eyebrow landmark indices
        self.LEFT_EYEBROW = [70, 63, 105, 66, 107]
        self.RIGHT_EYEBROW = [300, 293, 334, 296, 336]
        
        # Mouth landmark indices
        self.MOUTH_OUTER = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
        self.MOUTH_INNER = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]
        
        # Nose tip for reference
        self.NOSE_TIP = 1
        
        # Face points for head pose
        self.FACE_OVAL = [10, 338, 297, 332, 284, 251]
        
    def extract_features(self, landmarks):
        """
        Extract all geometric features from facial landmarks
        
        Args:
            landmarks: List of facial landmark coordinates
            
        Returns:
            Dictionary of extracted features
        """
        features = {}
        
        # Extract eye features
        features['left_eye_openness'] = self._calculate_eye_aspect_ratio(landmarks, self.LEFT_EYE)
        features['right_eye_openness'] = self._calculate_eye_aspect_ratio(landmarks, self.RIGHT_EYE)
        features['avg_eye_openness'] = (features['left_eye_openness'] + features['right_eye_openness']) / 2
        
        # Extract eyebrow features
        features['left_eyebrow_height'] = self._calculate_eyebrow_height(landmarks, self.LEFT_EYEBROW, self.LEFT_EYE)
        features['right_eyebrow_height'] = self._calculate_eyebrow_height(landmarks, self.RIGHT_EYEBROW, self.RIGHT_EYE)
        features['avg_eyebrow_height'] = (features['left_eyebrow_height'] + features['right_eyebrow_height']) / 2
        
        # Extract mouth features
        features['mouth_openness'] = self._calculate_mouth_aspect_ratio(landmarks)
        features['mouth_width'] = self._calculate_mouth_width(landmarks)
        
        # Extract head pose features
        pitch, yaw, roll = self._estimate_head_pose(landmarks)
        features['head_pitch'] = pitch
        features['head_yaw'] = yaw
        features['head_roll'] = roll
        
        # Extract facial symmetry
        features['facial_symmetry'] = self._calculate_facial_symmetry(landmarks)
        
        # Additional stress indicators
        features['eye_strain'] = self._calculate_eye_strain(features)
        features['facial_tension'] = self._calculate_facial_tension(features)
        
        return features
    
    def _calculate_eye_aspect_ratio(self, landmarks, eye_indices):
        """
        Calculate Eye Aspect Ratio (EAR)
        Higher value = more open eye
        
        Args:
            landmarks: Facial landmarks
            eye_indices: Indices for eye landmarks
            
        Returns:
            Eye aspect ratio
        """
        try:
            eye_points = [landmarks[i] for i in eye_indices]
            
            # Vertical eye landmarks (top and bottom)
            vertical_1 = self._euclidean_distance(eye_points[1], eye_points[5])
            vertical_2 = self._euclidean_distance(eye_points[2], eye_points[4])
            
            # Horizontal eye landmark
            horizontal = self._euclidean_distance(eye_points[0], eye_points[3])
            
            # EAR formula
            ear = (vertical_1 + vertical_2) / (2.0 * horizontal + 1e-6)
            
            return float(ear)
        except Exception as e:
            print(f"Eye aspect ratio calculation error: {e}")
            return 0.2  # Default value
    
    def _calculate_eyebrow_height(self, landmarks, eyebrow_indices, eye_indices):
        """
        Calculate distance between eyebrow and eye (indicator of surprise/fear)
        
        Args:
            landmarks: Facial landmarks
            eyebrow_indices: Eyebrow landmark indices
            eye_indices: Eye landmark indices
            
        Returns:
            Normalized eyebrow height
        """
        try:
            # Get centroid of eyebrow
            eyebrow_points = [landmarks[i] for i in eyebrow_indices]
            eyebrow_y = np.mean([p['y'] for p in eyebrow_points])
            
            # Get top of eye
            eye_points = [landmarks[i] for i in eye_indices]
            eye_y = np.mean([p['y'] for p in eye_points])
            
            # Distance (normalized)
            height = abs(eyebrow_y - eye_y)
            
            return float(height)
        except Exception as e:
            print(f"Eyebrow height calculation error: {e}")
            return 0.05  # Default value
    
    def _calculate_mouth_aspect_ratio(self, landmarks):
        """
        Calculate Mouth Aspect Ratio (MAR)
        Higher value = more open mouth
        
        Args:
            landmarks: Facial landmarks
            
        Returns:
            Mouth aspect ratio
        """
        try:
            # Vertical mouth opening (top to bottom)
            top_lip = landmarks[13]  # Upper lip center
            bottom_lip = landmarks[14]  # Lower lip center
            vertical = self._euclidean_distance(top_lip, bottom_lip)
            
            # Horizontal mouth width
            left_corner = landmarks[61]
            right_corner = landmarks[291]
            horizontal = self._euclidean_distance(left_corner, right_corner)
            
            # MAR formula
            mar = vertical / (horizontal + 1e-6)
            
            return float(mar)
        except Exception as e:
            print(f"Mouth aspect ratio calculation error: {e}")
            return 0.1  # Default value
    
    def _calculate_mouth_width(self, landmarks):
        """
        Calculate mouth width (indicator of smile/frown)
        
        Args:
            landmarks: Facial landmarks
            
        Returns:
            Normalized mouth width
        """
        try:
            left_corner = landmarks[61]
            right_corner = landmarks[291]
            width = self._euclidean_distance(left_corner, right_corner)
            
            return float(width)
        except Exception as e:
            print(f"Mouth width calculation error: {e}")
            return 0.2  # Default value
    
    def _estimate_head_pose(self, landmarks):
        """
        Estimate head pose (pitch, yaw, roll) from landmarks
        Simplified 2D approach
        
        Args:
            landmarks: Facial landmarks
            
        Returns:
            Tuple of (pitch, yaw, roll) in degrees
        """
        try:
            # Use key points for pose estimation
            nose_tip = landmarks[1]
            left_eye_outer = landmarks[33]
            right_eye_outer = landmarks[263]
            mouth_center = landmarks[13]
            
            # Calculate yaw (left-right rotation)
            left_dist = abs(nose_tip['x'] - left_eye_outer['x'])
            right_dist = abs(nose_tip['x'] - right_eye_outer['x'])
            yaw = (right_dist - left_dist) * 100  # Approximate in degrees
            
            # Calculate pitch (up-down rotation)
            eye_y = (left_eye_outer['y'] + right_eye_outer['y']) / 2
            mouth_y = mouth_center['y']
            pitch = (mouth_y - eye_y) * 100  # Approximate in degrees
            
            # Calculate roll (tilt)
            roll = np.arctan2(
                right_eye_outer['y'] - left_eye_outer['y'],
                right_eye_outer['x'] - left_eye_outer['x']
            ) * 180 / np.pi
            
            return float(pitch), float(yaw), float(roll)
        except Exception as e:
            print(f"Head pose estimation error: {e}")
            return 0.0, 0.0, 0.0
    
    def _calculate_facial_symmetry(self, landmarks):
        """
        Calculate facial symmetry (deviation from symmetry can indicate stress)
        
        Args:
            landmarks: Facial landmarks
            
        Returns:
            Symmetry score (1.0 = perfect symmetry, 0.0 = asymmetric)
        """
        try:
            # Compare left and right eye openness
            left_ear = self._calculate_eye_aspect_ratio(landmarks, self.LEFT_EYE)
            right_ear = self._calculate_eye_aspect_ratio(landmarks, self.RIGHT_EYE)
            eye_symmetry = 1.0 - abs(left_ear - right_ear)
            
            # Compare left and right eyebrow height
            left_brow = self._calculate_eyebrow_height(landmarks, self.LEFT_EYEBROW, self.LEFT_EYE)
            right_brow = self._calculate_eyebrow_height(landmarks, self.RIGHT_EYEBROW, self.RIGHT_EYE)
            brow_symmetry = 1.0 - abs(left_brow - right_brow) * 10
            
            # Average symmetry
            symmetry = (eye_symmetry + brow_symmetry) / 2
            symmetry = np.clip(symmetry, 0.0, 1.0)
            
            return float(symmetry)
        except Exception as e:
            print(f"Facial symmetry calculation error: {e}")
            return 0.8  # Default value
    
    def _calculate_eye_strain(self, features):
        """
        Estimate eye strain from eye openness and blink rate
        
        Args:
            features: Extracted features dictionary
            
        Returns:
            Eye strain indicator [0, 1]
        """
        # Low eye openness indicates strain or fatigue
        avg_openness = features.get('avg_eye_openness', 0.2)
        
        # Normal range is around 0.2-0.3
        if avg_openness < 0.15:
            strain = 0.8  # High strain (tired)
        elif avg_openness < 0.2:
            strain = 0.5  # Medium strain
        else:
            strain = 0.2  # Low strain
        
        return float(strain)
    
    def _calculate_facial_tension(self, features):
        """
        Estimate overall facial tension from multiple features
        
        Args:
            features: Extracted features dictionary
            
        Returns:
            Facial tension indicator [0, 1]
        """
        # High eyebrow position indicates surprise/fear
        brow_tension = features.get('avg_eyebrow_height', 0.05) * 10
        
        # Mouth tension (very open or very closed)
        mouth_openness = features.get('mouth_openness', 0.1)
        mouth_tension = abs(mouth_openness - 0.1) * 5
        
        # Asymmetry indicates tension
        symmetry = features.get('facial_symmetry', 0.8)
        asymmetry_tension = (1.0 - symmetry)
        
        # Combined tension
        tension = (brow_tension + mouth_tension + asymmetry_tension) / 3
        tension = np.clip(tension, 0.0, 1.0)
        
        return float(tension)
    
    def _euclidean_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        dx = point1['x'] - point2['x']
        dy = point1['y'] - point2['y']
        return np.sqrt(dx**2 + dy**2)
    
    def get_feature_vector_for_model(self, features):
        """
        Convert feature dictionary to vector for additional models (optional)
        
        Args:
            features: Dictionary of extracted features
            
        Returns:
            Numpy array of features
        """
        feature_list = [
            features.get('avg_eye_openness', 0.0),
            features.get('avg_eyebrow_height', 0.0),
            features.get('mouth_openness', 0.0),
            features.get('mouth_width', 0.0),
            features.get('head_pitch', 0.0),
            features.get('head_yaw', 0.0),
            features.get('head_roll', 0.0),
            features.get('facial_symmetry', 0.0),
            features.get('eye_strain', 0.0),
            features.get('facial_tension', 0.0)
        ]
        
        return np.array(feature_list, dtype=np.float32)
