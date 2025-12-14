/**
 * WebSocket Service
 * Manages real-time connection to backend
 */
import { io } from 'socket.io-client';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

class WebSocketService {
    constructor() {
        this.socket = null;
        this.sessionId = null;
        this.connected = false;
        this.eventHandlers = {};
    }

    connect() {
        if (this.connected) return Promise.resolve();

        return new Promise((resolve, reject) => {
            this.socket = io(BACKEND_URL, {
                transports: ['websocket', 'polling'],
                reconnection: true,
                reconnectionAttempts: 5,
                reconnectionDelay: 1000
            });

            this.socket.on('connect', () => {
                console.log('Connected to backend WebSocket');
                this.connected = true;
                resolve();
            });

            this.socket.on('session_created', (data) => {
                this.sessionId = data.session_id;
                console.log('Session created:', this.sessionId);
            });

            this.socket.on('disconnect', () => {
                console.log('Disconnected from backend');
                this.connected = false;
            });

            this.socket.on('error', (error) => {
                console.error('Socket error:', error);
                reject(error);
            });

            // Set up event listeners
            this.setupEventListeners();

            setTimeout(() => {
                if (!this.connected) {
                    reject(new Error('Connection timeout'));
                }
            }, 5000);
        });
    }

    setupEventListeners() {
        // Audio results
        this.socket.on('audio_result', (data) => {
            this.emit('audio_result', data);
        });

        // Video results
        this.socket.on('video_result', (data) => {
            this.emit('video_result', data);
        });

        // Fused stress updates
        this.socket.on('stress_update', (data) => {
            this.emit('stress_update', data);
        });

        // Session updates
        this.socket.on('session_update', (data) => {
            this.emit('session_update', data);
        });

        // Alerts
        this.socket.on('alert', (data) => {
            this.emit('alert', data);
        });

        // Timeline data
        this.socket.on('timeline_data', (data) => {
            this.emit('timeline_data', data);
        });

        // Session info
        this.socket.on('session_info', (data) => {
            this.emit('session_info', data);
        });
    }

    on(event, handler) {
        if (!this.eventHandlers[event]) {
            this.eventHandlers[event] = [];
        }
        this.eventHandlers[event].push(handler);
    }

    off(event, handler) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event] = this.eventHandlers[event].filter(h => h !== handler);
        }
    }

    emit(event, data) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].forEach(handler => handler(data));
        }
    }

    sendAudioChunk(audioData) {
        if (!this.connected || !this.socket) return;

        this.socket.emit('audio_chunk', {
            session_id: this.sessionId,
            audio_data: audioData  // Base64 encoded
        });
    }

    sendVideoFrame(frameData) {
        if (!this.connected || !this.socket) return;

        this.socket.emit('video_frame', {
            session_id: this.sessionId,
            frame_data: frameData  // Base64 encoded
        });
    }

    requestFusion(audioResult, videoResult) {
        if (!this.connected || !this.socket) return;

        this.socket.emit('fusion_request', {
            session_id: this.sessionId,
            audio_result: audioResult,
            video_result: videoResult
        });
    }

    getSessionInfo() {
        if (!this.connected || !this.socket) return;

        this.socket.emit('get_session_info', {
            session_id: this.sessionId
        });
    }

    getTimeline(limit = 100) {
        if (!this.connected || !this.socket) return;

        this.socket.emit('get_timeline', {
            session_id: this.sessionId,
            limit: limit
        });
    }

    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.connected = false;
            this.sessionId = null;
        }
    }
}

// Export singleton instance
const wsService = new WebSocketService();
export default wsService;
