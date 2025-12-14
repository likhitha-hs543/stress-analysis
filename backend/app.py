"""
Flask Application with WebSocket Support
Main entry point for Worker Stress Analysis System backend
"""
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import config
from websocket_handler import WebSocketHandler

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'worker-stress-analysis-secret-key'

# Enable CORS
CORS(app, resources={r"/*": {"origins": config.CORS_ORIGINS}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins=config.CORS_ORIGINS, async_mode='eventlet')

# Initialize WebSocket handler
ws_handler = WebSocketHandler()

# Store session mappings (SID -> session_id)
session_mappings = {}


# ===== HTTP Routes =====

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'Worker Stress Analysis System',
        'version': '1.0.0'
    })


@app.route('/api/info')
def get_system_info():
    """Get system and model information"""
    return jsonify({
        'system': {
            'name': 'Worker Stress Analysis System',
            'version': '1.0.0',
            'description': 'Real-time multimodal stress detection using audio and video'
        },
        'models': {
            'audio': {
                'type': 'CNN-LSTM',
                'input': 'MFCC features',
                'emotions': config.EMOTION_LABELS,
                'sample_rate': config.AUDIO_SAMPLE_RATE
            },
            'video': {
                'type': 'CNN',
                'input': '48x48 grayscale face image',
                'emotions': config.EMOTION_LABELS,
                'face_landmarks': 468
            }
        },
        'fusion': {
            'method': 'Confidence-weighted averaging',
            'modalities': ['audio', 'video']
        },
        'stress_levels': {
            'low': f'< {config.STRESS_LOW_THRESHOLD}',
            'medium': f'{config.STRESS_LOW_THRESHOLD} - {config.STRESS_HIGH_THRESHOLD}',
            'high': f'≥ {config.STRESS_HIGH_THRESHOLD}'
        },
        'alerts': {
            'sustained_high_stress_threshold': config.ALERT_HIGH_STRESS_THRESHOLD,
            'sustained_duration': f'{config.ALERT_HIGH_STRESS_DURATION} seconds',
            'spike_threshold': config.ALERT_SPIKE_THRESHOLD
        }
    })


@app.route('/api/model/architecture')
def get_model_architecture():
    """Get detailed model architecture information"""
    return jsonify({
        'audio_model': {
            'architecture': 'CNN-LSTM',
            'layers': [
                'Conv1D (64 filters, kernel=5)',
                'BatchNorm + ReLU + MaxPool',
                'Conv1D (128 filters, kernel=5)',
                'BatchNorm + ReLU + MaxPool',
                'Bidirectional LSTM (hidden=128, layers=2)',
                'Fully Connected (64)',
                'Output (7 emotions)'
            ],
            'features': [
                '13 MFCC coefficients',
                '13 MFCC delta (1st derivative)',
                '13 MFCC delta-delta (2nd derivative)',
                'Pitch (F0)',
                'Energy (RMS)',
                'Jitter',
                'Shimmer',
                'Speech rate',
                'Zero crossing rate',
                'Spectral centroid',
                'Spectral rolloff'
            ]
        },
        'video_model': {
            'architecture': 'CNN',
            'layers': [
                'Conv2D (64 filters) + BatchNorm + ReLU + MaxPool',
                'Conv2D (128 filters) + BatchNorm + ReLU + MaxPool',
                'Conv2D (256 filters) + BatchNorm + ReLU + MaxPool',
                'Conv2D (512 filters) + BatchNorm + ReLU + MaxPool',
                'Fully Connected (512)',
                'Fully Connected (256)',
                'Output (7 emotions)'
            ],
            'features': [
                'Eye aspect ratio',
                'Eyebrow height',
                'Mouth aspect ratio',
                'Head pose (pitch, yaw, roll)',
                'Facial symmetry',
                'Eye strain indicator',
                'Facial tension indicator'
            ]
        }
    })


# ===== WebSocket Events =====

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    sid = request.sid
    session_id = ws_handler.handle_connect(sid)
    session_mappings[sid] = session_id
    print(f"Client connected: {sid}")


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    sid = request.sid
    session_id = session_mappings.get(sid)
    ws_handler.handle_disconnect(sid, session_id)
    if sid in session_mappings:
        del session_mappings[sid]
    print(f"Client disconnected: {sid}")


@socketio.on('audio_chunk')
def handle_audio_chunk(data):
    """Process audio chunk"""
    sid = request.sid
    data['session_id'] = session_mappings.get(sid)
    ws_handler.handle_audio_chunk(data)


@socketio.on('video_frame')
def handle_video_frame(data):
    """Process video frame"""
    sid = request.sid
    data['session_id'] = session_mappings.get(sid)
    ws_handler.handle_video_frame(data)


@socketio.on('fusion_request')
def handle_fusion_request(data):
    """Perform multimodal fusion"""
    sid = request.sid
    data['session_id'] = session_mappings.get(sid)
    ws_handler.handle_fusion_request(data)


@socketio.on('get_session_info')
def handle_get_session_info(data):
    """Get session information"""
    sid = request.sid
    data['session_id'] = session_mappings.get(sid)
    ws_handler.handle_get_session_info(data)


@socketio.on('get_timeline')
def handle_get_timeline(data):
    """Get timeline data"""
    sid = request.sid
    data['session_id'] = session_mappings.get(sid)
    ws_handler.handle_get_timeline(data)


# ===== Main =====

if __name__ == '__main__':
    print('='*60)
    print('Worker Stress Analysis System - Backend Server')
    print('='*60)
    print(f'Host: {config.HOST}')
    print(f'Port: {config.PORT}')
    print(f'Debug: {config.DEBUG}')
    print('='*60)
    
    socketio.run(
        app,
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
