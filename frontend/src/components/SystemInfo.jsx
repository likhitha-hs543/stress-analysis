/**
 * System Info Component
 * Displays model information and ethics disclaimer
 */
import React from 'react';
import './SystemInfo.css';

const SystemInfo = () => {
    return (
        <div className="system-info">
            <h2>ℹ️ System Information</h2>

            {/* Model Architecture */}
            <div className="info-section">
                <h3>🧠 Model Architecture</h3>
                <div className="model-grid">
                    <div className="model-card">
                        <h4>Audio Analysis</h4>
                        <p className="model-type">CNN-LSTM Network</p>
                        <ul className="feature-list">
                            <li>13 MFCC coefficients + deltas</li>
                            <li>Pitch (F0) extraction</li>
                            <li>Energy & voice quality (jitter, shimmer)</li>
                            <li>Speech rate analysis</li>
                            <li>Spectral features</li>
                        </ul>
                    </div>

                    <div className="model-card">
                        <h4>Video Analysis</h4>
                        <p className="model-type">Convolutional Neural Network</p>
                        <ul className="feature-list">
                            <li>MediaPipe Face Mesh (468 landmarks)</li>
                            <li>Eye aspect ratio</li>
                            <li>Eyebrow & mouth features</li>
                            <li>Head pose estimation</li>
                            <li>Facial tension indicators</li>
                        </ul>
                    </div>

                    <div className="model-card">
                        <h4>Multimodal Fusion</h4>
                        <p className="model-type">Confidence-Weighted Averaging</p>
                        <ul className="feature-list">
                            <li>Dynamic weight adjustment</li>
                            <li>Cross-modal validation</li>
                            <li>Real-time inference</li>
                            <li>7 emotion classes</li>
                        </ul>
                    </div>
                </div>
            </div>

            {/* Privacy & Ethics */}
            <div className="info-section ethics-section">
                <h3>🔒 Privacy & Ethics</h3>
                <div className="ethics-content">
                    <div className="ethics-card important">
                        <span className="ethics-icon">🛡️</span>
                        <div>
                            <h4>No Data Storage</h4>
                            <p>Raw audio and video are NEVER stored. Only aggregated feature values and predictions are kept temporarily in memory.</p>
                        </div>
                    </div>

                    <div className="ethics-card">
                        <span className="ethics-icon">🎯</span>
                        <div>
                            <h4>Session-Based Analysis</h4>
                            <p>All analysis is session-based. Data is automatically cleared when you disconnect.</p>
                        </div>
                    </div>

                    <div className="ethics-card">
                        <span className="ethics-icon">👤</span>
                        <div>
                            <h4>No Identity Recognition</h4>
                            <p>The system does not perform facial recognition or identity tracking. Only emotion and stress indicators are analyzed.</p>
                        </div>
                    </div>

                    <div className="ethics-card">
                        <span className="ethics-icon">✋</span>
                        <div>
                            <h4>Explicit Consent</h4>
                            <p>Camera and microphone access requires your explicit permission. You can stop at any time.</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Technical Details */}
            <div className="info-section">
                <h3>⚙️ Technical Specifications</h3>
                <div className="tech-grid">
                    <div className="tech-item">
                        <span className="tech-label">Audio Sample Rate:</span>
                        <span className="tech-value">16 kHz</span>
                    </div>
                    <div className="tech-item">
                        <span className="tech-label">Video FPS:</span>
                        <span className="tech-value">15 fps</span>
                    </div>
                    <div className="tech-item">
                        <span className="tech-label">Processing Mode:</span>
                        <span className="tech-value">Real-time Streaming</span>
                    </div>
                    <div className="tech-item">
                        <span className="tech-label">Emotion Classes:</span>
                        <span className="tech-value">7 (Neutral, Happy, Sad, Angry, Fear, Disgust, Surprise)</span>
                    </div>
                    <div className="tech-item">
                        <span className="tech-label">Stress Levels:</span>
                        <span className="tech-value">Low (&lt;33%), Medium (33-66%), High (&gt;66%)</span>
                    </div>
                </div>
            </div>

            {/* Disclaimer */}
            <div className="disclaimer">
                <p><strong>⚠️ Disclaimer:</strong> This system is designed as a supportive tool for workplace wellness monitoring. It should not replace professional medical or psychological assessment. Results are probabilistic estimates based on machine learning models and should be interpreted with appropriate caution.</p>
            </div>
        </div>
    );
};

export default SystemInfo;
