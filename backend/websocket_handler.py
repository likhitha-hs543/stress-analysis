"""
WebSocket Handler
Manages real-time communication between frontend and backend
"""
import base64
import numpy as np
import cv2
from flask_socketio import emit

# Import processing components
from audio_stream import AudioPreprocessor, AudioFeatureExtractor, AudioEmotionModel, AudioStressScorer
from video_stream import FaceDetector, VideoFeatureExtractor, VideoEmotionModel, VideoStressScorer
from fusion_engine import MultimodalFusion, StressClassifier
from utils import AlertManager, SessionManager
import config


class WebSocketHandler:
    """Handles WebSocket events for real-time processing"""
    
    def __init__(self):
        # Initialize audio components
        self.audio_preprocessor = AudioPreprocessor()
        self.audio_feature_extractor = AudioFeatureExtractor()
        self.audio_emotion_model = AudioEmotionModel(config.AUDIO_MODEL_PATH)
        self.audio_stress_scorer = AudioStressScorer()
        
        # Initialize video components
        self.face_detector = FaceDetector()
        self.video_feature_extractor = VideoFeatureExtractor()
        self.video_emotion_model = VideoEmotionModel(config.VIDEO_MODEL_PATH)
        self.video_stress_scorer = VideoStressScorer()
        
        # Initialize fusion and utilities
        self.fusion_engine = MultimodalFusion()
        self.stress_classifier = StressClassifier()
        self.alert_manager = AlertManager()
        self.session_manager = SessionManager()
        
    def handle_connect(self, sid):
        """Handle client connection"""
        session_id = self.session_manager.create_session()
        print(f"Client connected: {sid}, Session: {session_id}")
        
        emit('session_created', {
            'session_id': session_id,
            'message': 'Connected to Worker Stress Analysis System'
        })
        
        return session_id
    
    def handle_disconnect(self, sid, session_id):
        """Handle client disconnection"""
        print(f"Client disconnected: {sid}")
        if session_id:
            self.session_manager.end_session(session_id)
    
    def handle_audio_chunk(self, data):
        """
        Process audio chunk from client
        
        Args:
            data: Dictionary containing audio data and session_id
        """
        try:
            session_id = data.get('session_id')
            audio_base64 = data.get('audio_data')
            
            if not audio_base64:
                return
            
            # Decode base64 audio to numpy array
            audio_bytes = base64.b64decode(audio_base64)
            audio_array = np.frombuffer(audio_bytes, dtype=np.float32)
            
            # Preprocess audio
            processed_audio = self.audio_preprocessor.process_audio_chunk(audio_array)
            
            # Validate audio (check if not silence)
            if not self.audio_preprocessor.validate_audio_chunk(processed_audio):
                print("Audio chunk is silence, skipping...")
                return None
            
            # Extract features
            features = self.audio_feature_extractor.extract_features(processed_audio)
            
            # Get feature vector for model
            feature_vector = self.audio_feature_extractor.get_feature_vector_for_model(features)
            
            # Predict emotion
            emotion, emotion_probs, confidence = self.audio_emotion_model.predict(feature_vector)
            
            # Calculate stress score
            stress_score, stress_level, details = self.audio_stress_scorer.calculate_stress_score(
                emotion, emotion_probs, confidence
            )
            
            # Emit audio result
            audio_result = {
                'modality': 'audio',
                'emotion': emotion,
                'emotion_probabilities': emotion_probs,
                'stress_score': stress_score,
                'stress_level': stress_level,
                'confidence': confidence
            }
            
            emit('audio_result', audio_result)
            
            return audio_result
            
        except Exception as e:
            print(f"Error processing audio: {e}")
            emit('error', {'message': f'Audio processing error: {str(e)}'})
            return None
    
    def handle_video_frame(self, data):
        """
        Process video frame from client
        
        Args:
            data: Dictionary containing video frame and session_id
        """
        try:
            session_id = data.get('session_id')
            frame_base64 = data.get('frame_data')
            
            if not frame_base64:
                return
            
            # Decode base64 image to numpy array
            frame_bytes = base64.b64decode(frame_base64)
            nparr = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return None
            
            # Detect face and landmarks
            face_detected, landmarks, annotated_frame = self.face_detector.detect_face_and_landmarks(frame)
            
            if not face_detected:
                print("No face detected in frame")
                emit('video_result', {
                    'modality': 'video',
                    'face_detected': False,
                    'message': 'No face detected'
                })
                return None
            
            # Extract facial features
            facial_features = self.video_feature_extractor.extract_features(landmarks)
            
            # Extract face ROI for emotion model
            face_roi = self.face_detector.extract_face_roi(frame, landmarks)
            
            if face_roi is None:
                return None
            
            # Predict emotion
            emotion, emotion_probs, confidence = self.video_emotion_model.predict(face_roi)
            
            # Calculate stress score
            stress_score, stress_level, details = self.video_stress_scorer.calculate_stress_score(
                emotion, emotion_probs, confidence, facial_features
            )
            
            # Emit video result
            video_result = {
                'modality': 'video',
                'face_detected': True,
                'emotion': emotion,
                'emotion_probabilities': emotion_probs,
                'stress_score': stress_score,
                'stress_level': stress_level,
                'confidence': confidence,
                'facial_features': {
                    'eye_openness': facial_features.get('avg_eye_openness', 0),
                    'eyebrow_height': facial_features.get('avg_eyebrow_height', 0),
                    'mouth_openness': facial_features.get('mouth_openness', 0)
                }
            }
            
            emit('video_result', video_result)
            
            return video_result
            
        except Exception as e:
            print(f"Error processing video: {e}")
            emit('error', {'message': f'Video processing error: {str(e)}'})
            return None
    
    def handle_fusion_request(self, data):
        """
        Perform multimodal fusion and send final analysis
        
        Args:
            data: Dictionary containing audio and video results
        """
        try:
            session_id = data.get('session_id')
            audio_result = data.get('audio_result')
            video_result = data.get('video_result')
            
            # Perform fusion
            fused_result = self.fusion_engine.fuse_stress_scores(audio_result, video_result)
            
            # Update session
            session_info = self.session_manager.update_session(session_id, fused_result)
            
            # Check for alerts
            alerts = self.alert_manager.check_alerts(
                session_id,
                fused_result.get('stress_score', 0.5)
            )
            
            # Emit fused result
            emit('stress_update', fused_result)
            
            # Emit session update
            emit('session_update', session_info)
            
            # Emit alerts if any
            if alerts:
                for alert in alerts:
                    emit('alert', alert)
            
        except Exception as e:
            print(f"Error in fusion: {e}")
            emit('error', {'message': f'Fusion error: {str(e)}'})
    
    def handle_get_session_info(self, data):
        """Get session information"""
        session_id = data.get('session_id')
        session_info = self.session_manager.get_session_info(session_id)
        
        if session_info:
            emit('session_info', session_info)
        else:
            emit('error', {'message': 'Session not found'})
    
    def handle_get_timeline(self, data):
        """Get stress timeline data"""
        session_id = data.get('session_id')
        limit = data.get('limit', 100)
        
        timeline = self.session_manager.get_stress_timeline(session_id, limit)
        emit('timeline_data', {'timeline': timeline})
