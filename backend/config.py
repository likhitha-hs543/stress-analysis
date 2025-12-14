"""
Configuration settings for Worker Stress Analysis System
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Server Configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# CORS Settings
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

# Audio Processing Settings
AUDIO_SAMPLE_RATE = 16000  # 16 kHz
AUDIO_CHUNK_DURATION = 3.0  # seconds
AUDIO_OVERLAP = 0.5  # 50% overlap
AUDIO_CHANNELS = 1  # mono

# Audio Feature Extraction
MFCC_N_COEFF = 13
MFCC_N_FFT = 2048
MFCC_HOP_LENGTH = 512
PITCH_FMIN = 75  # Hz (minimum pitch)
PITCH_FMAX = 600  # Hz (maximum pitch)

# Video Processing Settings
VIDEO_FPS = 15  # Target frames per second
VIDEO_FRAME_WIDTH = 640
VIDEO_FRAME_HEIGHT = 480
FACE_DETECTION_CONFIDENCE = 0.5

# Model Paths
MODELS_DIR = BASE_DIR / 'models'
AUDIO_MODEL_PATH = MODELS_DIR / 'audio_emotion_model.pth'
VIDEO_MODEL_PATH = MODELS_DIR / 'video_emotion_model.pth'

# Emotion Labels (7 basic emotions)
EMOTION_LABELS = [
    'neutral',
    'happy',
    'sad',
    'angry',
    'fear',
    'disgust',
    'surprise'
]

# Stress Mapping (emotion -> stress weight)
EMOTION_STRESS_WEIGHTS = {
    'neutral': 0.1,
    'happy': 0.0,
    'sad': 0.5,
    'angry': 0.9,
    'fear': 0.85,
    'disgust': 0.6,
    'surprise': 0.3
}

# Fusion Settings
AUDIO_WEIGHT = 0.5  # Weight for audio modality
VIDEO_WEIGHT = 0.5  # Weight for video modality

# Stress Level Thresholds
STRESS_LOW_THRESHOLD = 0.33
STRESS_HIGH_THRESHOLD = 0.66

# Alert Settings
ALERT_HIGH_STRESS_THRESHOLD = 0.7
ALERT_HIGH_STRESS_DURATION = 180  # seconds (3 minutes)
ALERT_SPIKE_THRESHOLD = 0.3  # stress increase
ALERT_SPIKE_WINDOW = 30  # seconds

# Session Settings
SESSION_MAX_HISTORY = 1000  # Maximum data points to keep in memory
SESSION_CLEANUP_INTERVAL = 3600  # seconds (1 hour)

# Privacy Settings
STORE_RAW_AUDIO = False  # Never store raw audio
STORE_RAW_VIDEO = False  # Never store raw video
STORE_FEATURES = True  # Store aggregated features only
STORE_PREDICTIONS = True  # Store predictions only

# WebSocket Events
WS_EVENT_AUDIO_CHUNK = 'audio_chunk'
WS_EVENT_VIDEO_FRAME = 'video_frame'
WS_EVENT_EMOTION_RESULT = 'emotion_result'
WS_EVENT_STRESS_UPDATE = 'stress_update'
WS_EVENT_ALERT = 'alert'
WS_EVENT_SESSION_INFO = 'session_info'
