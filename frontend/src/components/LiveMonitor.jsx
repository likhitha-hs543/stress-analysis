/**
 * Live Monitor Component
 * Displays real-time camera feed, audio waveform, emotions, and stress meter
 */
import React, { useRef, useEffect, useState } from 'react';
import './LiveMonitor.css';

const LiveMonitor = ({
    videoStream,
    currentEmotion,
    currentStress,
    audioLevel
}) => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    // Set up video stream
    useEffect(() => {
        if (videoRef.current && videoStream) {
            videoRef.current.srcObject = videoStream;
        }
    }, [videoStream]);

    // Draw audio waveform
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // Clear canvas
        ctx.fillStyle = 'rgba(15, 23, 42, 0.3)';
        ctx.fillRect(0, 0, width, height);

        // Draw waveform
        const amplitude = (audioLevel || 0) * height / 2;
        ctx.strokeStyle = '#3b82f6';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, height / 2);

        for (let x = 0; x < width; x += 10) {
            const y = height / 2 + Math.sin(x / 20 + Date.now() / 100) * amplitude;
            ctx.lineTo(x, y);
        }

        ctx.stroke();
    }, [audioLevel]);

    const getStressColor = (score) => {
        if (score < 0.33) return '#10b981'; // green
        if (score < 0.66) return '#f59e0b'; // yellow
        return '#ef4444'; // red
    };

    const getStressLevel = (score) => {
        if (score < 0.33) return 'Low';
        if (score < 0.66) return 'Medium';
        return 'High';
    };

    const stressScore = currentStress?.stress_score || 0.5;
    const stressColor = getStressColor(stressScore);

    return (
        <div className="live-monitor">
            <div className="monitor-grid">
                {/* Camera Preview */}
                <div className="monitor-card camera-preview">
                    <h3>📷 Live Camera Feed</h3>
                    <div className="video-container">
                        <video
                            ref={videoRef}
                            autoPlay
                            playsInline
                            muted
                            className="video-feed"
                        />
                    </div>
                </div>

                {/* Audio Waveform */}
                <div className="monitor-card audio-waveform">
                    <h3>🎤 Audio Waveform</h3>
                    <canvas
                        ref={canvasRef}
                        width={400}
                        height={100}
                        className="waveform-canvas"
                    />
                </div>

                {/* Current Emotions */}
                <div className="monitor-card emotions">
                    <h3>😊 Current Emotions</h3>
                    <div className="emotion-display">
                        <div className="emotion-item">
                            <span className="emotion-label">Voice:</span>
                            <span className="emotion-value">
                                {currentEmotion?.audio || 'Detecting...'}
                            </span>
                        </div>
                        <div className="emotion-item">
                            <span className="emotion-label">Face:</span>
                            <span className="emotion-value">
                                {currentEmotion?.video || 'Detecting...'}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Stress Meter */}
                <div className="monitor-card stress-meter">
                    <h3>📊 Stress Level</h3>
                    <div className="meter-container">
                        <svg className="circular-meter" viewBox="0 0 200 200">
                            <circle
                                className="meter-background"
                                cx="100"
                                cy="100"
                                r="80"
                                fill="none"
                                stroke="#1e293b"
                                strokeWidth="20"
                            />
                            <circle
                                className="meter-foreground"
                                cx="100"
                                cy="100"
                                r="80"
                                fill="none"
                                stroke={stressColor}
                                strokeWidth="20"
                                strokeDasharray={`${stressScore * 502.4} 502.4`}
                                transform="rotate(-90 100 100)"
                            />
                            <text
                                x="100"
                                y="100"
                                textAnchor="middle"
                                dominantBaseline="middle"
                                className="meter-text"
                                fill={stressColor}
                            >
                                {Math.round(stressScore * 100)}%
                            </text>
                            <text
                                x="100"
                                y="130"
                                textAnchor="middle"
                                className="meter-label"
                                fill="#94a3b8"
                            >
                                {getStressLevel(stressScore)}
                            </text>
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LiveMonitor;
