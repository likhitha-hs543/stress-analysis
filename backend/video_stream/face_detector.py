"""
Face Detector
Real-time face detection and facial landmark extraction using MediaPipe
"""
import cv2
import mediapipe as mp
import numpy as np
import config


class FaceDetector:
    """Detects faces and extracts facial landmarks using MediaPipe Face Mesh"""
    
    def __init__(self):
        """Initialize MediaPipe Face Mesh"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=config.FACE_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.FACE_DETECTION_CONFIDENCE
        )
        
        # Landmark indices for key facial features
        # Eyes
        self.LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
        
        # Eyebrows
        self.LEFT_EYEBROW_INDICES = [70, 63, 105, 66, 107]
        self.RIGHT_EYEBROW_INDICES = [300, 293, 334, 296, 336]
        
        # Mouth
        self.MOUTH_OUTER_INDICES = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
        self.MOUTH_INNER_INDICES = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]
        
        # Face oval for head pose estimation
        self.FACE_OVAL_INDICES = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323,
                                   361, 288, 397, 365, 379, 378, 400, 377, 152, 148,
                                   176, 149, 150, 136, 172, 58, 132, 93, 234, 127,
                                   162, 21, 54, 103, 67, 109]
        
    def detect_face_and_landmarks(self, frame):
        """
        Detect face and extract facial landmarks
        
        Args:
            frame: Input image (BGR format from OpenCV)
            
        Returns:
            Tuple of (success, landmarks, annotated_frame)
            - success: Boolean indicating if face was detected
            - landmarks: List of 468 (x, y, z) landmark coordinates (normalized)
            - annotated_frame: Frame with face mesh drawn (for visualization)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            # Get the first face landmarks
            face_landmarks = results.multi_face_landmarks[0]
            
            # Extract landmark coordinates
            landmarks = []
            h, w, _ = frame.shape
            
            for landmark in face_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x,  # Normalized [0, 1]
                    'y': landmark.y,  # Normalized [0, 1]
                    'z': landmark.z,  # Relative depth
                    'x_px': int(landmark.x * w),  # Pixel coordinates
                    'y_px': int(landmark.y * h)
                })
            
            # Create annotated frame for visualization
            annotated_frame = frame.copy()
            mp.solutions.drawing_utils.draw_landmarks(
                image=annotated_frame,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style()
            )
            
            return True, landmarks, annotated_frame
        else:
            return False, None, frame
    
    def extract_face_roi(self, frame, landmarks):
        """
        Extract face region of interest (ROI) for emotion model
        
        Args:
            frame: Input image
            landmarks: Facial landmarks
            
        Returns:
            Face ROI image (grayscale, 48x48 for FER models)
        """
        if landmarks is None or len(landmarks) == 0:
            return None
        
        # Get bounding box from landmarks
        x_coords = [lm['x_px'] for lm in landmarks]
        y_coords = [lm['y_px'] for lm in landmarks]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Add padding (10%)
        padding_x = int((x_max - x_min) * 0.1)
        padding_y = int((y_max - y_min) * 0.1)
        
        x_min = max(0, x_min - padding_x)
        x_max = min(frame.shape[1], x_max + padding_x)
        y_min = max(0, y_min - padding_y)
        y_max = min(frame.shape[0], y_max + padding_y)
        
        # Extract ROI
        face_roi = frame[y_min:y_max, x_min:x_max]
        
        if face_roi.size == 0:
            return None
        
        # Convert to grayscale
        if len(face_roi.shape) == 3:
            face_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        else:
            face_gray = face_roi
        
        # Resize to 48x48 (standard for FER models)
        face_resized = cv2.resize(face_gray, (48, 48))
        
        # Normalize to [0, 1]
        face_normalized = face_resized.astype(np.float32) / 255.0
        
        return face_normalized
    
    def get_landmark_subset(self, landmarks, indices):
        """
        Get subset of landmarks by indices
        
        Args:
            landmarks: All facial landmarks
            indices: List of landmark indices to extract
            
        Returns:
            List of selected landmarks
        """
        return [landmarks[i] for i in indices if i < len(landmarks)]
    
    def close(self):
        """Release resources"""
        self.face_mesh.close()
