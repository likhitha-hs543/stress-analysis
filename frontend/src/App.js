/**
 * Main App Component
 * Worker Stress Analysis System
 */
import React, { useState, useEffect, useRef } from 'react';
import LiveMonitor from './components/LiveMonitor';
import StressTimeline from './components/StressTimeline';
import Analytics from './components/Analytics';
import AlertPanel from './components/AlertPanel';
import SystemInfo from './components/SystemInfo';
import wsService from './services/websocket';
import mediaService from './services/mediaStream';
import './App.css';

function App() {
    const [connected, setConnected] = useState(false);
    const [permissionsGranted, setPermissionsGranted] = useState(false);
    const [showConsent, setShowConsent] = useState(true);
    const [activeTab, setActiveTab] = useState('monitor');
    const [videoStream, setVideoStream] = useState(null);
    const [currentEmotion, setCurrentEmotion] = useState({ audio: null, video: null });
    const [currentStress, setCurrentStress] = useState(null);
    const [audioLevel, setAudioLevel] = useState(0);
    const [sessionInfo, setSessionInfo] = useState(null);
    const [timelineData, setTimelineData] = useState([]);
    const [alerts, setAlerts] = useState([]);

    const videoRef = useRef(null);
    const audioResultRef = useRef(null);
    const videoResultRef = useRef(null);
    const videoIntervalRef = useRef(null);

    // Initialize WebSocket connection
    useEffect(() => {
        const initWebSocket = async () => {
            try {
                await wsService.connect();
                setConnected(true);
                console.log('WebSocket connected');

                // Set up event listeners
                wsService.on('audio_result', handleAudioResult);
                wsService.on('video_result', handleVideoResult);
                wsService.on('stress_update', handleStressUpdate);
                wsService.on('session_update', handleSessionUpdate);
                wsService.on('alert', handleAlert);
                wsService.on('timeline_data', handleTimelineData);
            } catch (error) {
                console.error('Failed to connect to WebSocket:', error);
            }
        };

        initWebSocket();

        return () => {
            stopCapture();
            wsService.disconnect();
        };
    }, []);

    const handleAudioResult = (data) => {
        audioResultRef.current = data;
        setCurrentEmotion(prev => ({ ...prev, audio: data.emotion }));
        setAudioLevel(Math.random() * 0.5 + 0.3); // Simulated audio level

        // Request fusion if we have both results
        if (videoResultRef.current) {
            wsService.requestFusion(audioResultRef.current, videoResultRef.current);
        }
    };

    const handleVideoResult = (data) => {
        if (data.face_detected) {
            videoResultRef.current = data;
            setCurrentEmotion(prev => ({ ...prev, video: data.emotion }));

            // Request fusion if we have both results
            if (audioResultRef.current) {
                wsService.requestFusion(audioResultRef.current, videoResultRef.current);
            }
        }
    };

    const handleStressUpdate = (data) => {
        setCurrentStress(data);
    };

    const handleSessionUpdate = (data) => {
        setSessionInfo(data);
    };

    const handleAlert = (alert) => {
        setAlerts(prev => [...prev, alert]);
    };

    const handleTimelineData = (data) => {
        setTimelineData(data.timeline || []);
    };

    const handleConsentAccept = async () => {
        try {
            // Request media permissions
            await mediaService.requestPermissions();

            const videoStream = mediaService.getVideoStream();
            setVideoStream(videoStream);
            setPermissionsGranted(true);
            setShowConsent(false);

            // Start capture
            startCapture();
        } catch (error) {
            console.error('Permission denied:', error);
            alert('Camera and microphone permissions are required to use this system.');
        }
    };

    const startCapture = () => {
        // Start audio capture (every 3 seconds)
        mediaService.startAudioCapture((audioData) => {
            wsService.sendAudioChunk(audioData);
        }, 3000);

        // Start video capture (every 200ms = 5 fps)
        videoIntervalRef.current = setInterval(() => {
            if (videoRef.current) {
                const frameData = mediaService.captureVideoFrame(videoRef.current);
                if (frameData) {
                    wsService.sendVideoFrame(frameData);
                }
            }
        }, 200);

        // Request timeline updates every 5 seconds
        setInterval(() => {
            wsService.getTimeline(100);
            wsService.getSessionInfo();
        }, 5000);
    };

    const stopCapture = () => {
        mediaService.stopAllStreams();
        if (videoIntervalRef.current) {
            clearInterval(videoIntervalRef.current);
        }
    };

    const renderTabContent = () => {
        switch (activeTab) {
            case 'monitor':
                return (
                    <LiveMonitor
                        videoStream={videoStream}
                        currentEmotion={currentEmotion}
                        currentStress={currentStress}
                        audioLevel={audioLevel}
                    />
                );
            case 'timeline':
                return <StressTimeline timelineData={timelineData} />;
            case 'analytics':
                return <Analytics sessionInfo={sessionInfo} />;
            case 'alerts':
                return <AlertPanel alerts={alerts} sessionInfo={sessionInfo} />;
            case 'system':
                return <SystemInfo />;
            default:
                return null;
        }
    };

    return (
        <div className="app">
            {/* Consent Modal */}
            {showConsent && (
                <div className="consent-modal">
                    <div className="consent-content">
                        <h1>🔒 Privacy & Consent</h1>
                        <div className="consent-message">
                            <p>This Worker Stress Analysis System will access your camera and microphone to analyze your emotional state and stress levels in real-time.</p>

                            <div className="consent-highlights">
                                <div className="highlight">
                                    <span className="highlight-icon">✅</span>
                                    <span>No raw data is stored</span>
                                </div>
                                <div className="highlight">
                                    <span className="highlight-icon">✅</span>
                                    <span>Session-based analysis only</span>
                                </div>
                                <div className="highlight">
                                    <span className="highlight-icon">✅</span>
                                    <span>No identity recognition</span>
                                </div>
                                <div className="highlight">
                                    <span className="highlight-icon">✅</span>
                                    <span>You can stop at any time</span>
                                </div>
                            </div>

                            <p className="consent-disclaimer">By clicking "Accept & Continue", you grant permission to access your camera and microphone for stress analysis purposes.</p>
                        </div>

                        <div className="consent-actions">
                            <button className="btn-primary" onClick={handleConsentAccept}>
                                Accept & Continue
                            </button>
                            <button className="btn-secondary" onClick={() => alert('Camera and microphone access is required to use this system.')}>
                                Decline
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Main Dashboard */}
            {permissionsGranted && (
                <>
                    {/* Header */}
                    <header className="app-header">
                        <div className="header-content">
                            <div className="header-left">
                                <h1>🧠 Worker Stress Analysis System</h1>
                                <p className="header-subtitle">Real-time AI-powered stress detection</p>
                            </div>
                            <div className="header-right">
                                <div className="connection-status">
                                    <span className={`status-dot ${connected ? 'connected' : 'disconnected'}`}></span>
                                    <span>{connected ? 'Connected' : 'Disconnected'}</span>
                                </div>
                                {sessionInfo && (
                                    <div className="worker-info">
                                        <span className="worker-id">{sessionInfo.worker_id}</span>
                                    </div>
                                )}
                            </div>
                        </div>
                    </header>

                    {/* Navigation Tabs */}
                    <nav className="nav-tabs">
                        <button
                            className={`nav-tab ${activeTab === 'monitor' ? 'active' : ''}`}
                            onClick={() => setActiveTab('monitor')}
                        >
                            📊 Live Monitor
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'timeline' ? 'active' : ''}`}
                            onClick={() => setActiveTab('timeline')}
                        >
                            📈 Timeline
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'analytics' ? 'active' : ''}`}
                            onClick={() => setActiveTab('analytics')}
                        >
                            📊 Analytics
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'alerts' ? 'active' : ''}`}
                            onClick={() => setActiveTab('alerts')}
                        >
                            🚨 Alerts
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'system' ? 'active' : ''}`}
                            onClick={() => setActiveTab('system')}
                        >
                            ℹ️ System Info
                        </button>
                    </nav>

                    {/* Main Content */}
                    <main className="app-content">
                        {/* Hidden video element for processing */}
                        <video
                            ref={videoRef}
                            style={{ display: 'none' }}
                            autoPlay
                            playsInline
                            muted
                        />

                        {renderTabContent()}
                    </main>
                </>
            )}
        </div>
    );
}

export default App;
