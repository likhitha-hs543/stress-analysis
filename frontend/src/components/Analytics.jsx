/**
 * Analytics Component
 * Session analytics and statistics
 */
import React from 'react';
import './Analytics.css';

const Analytics = ({ sessionInfo }) => {
    const analytics = sessionInfo?.analytics || {};
    const emotions = analytics.emotion_distribution || {};

    const getTopEmotion = () => {
        let topEmotion = 'None';
        let maxPercent = 0;

        Object.entries(emotions).forEach(([emotion, percent]) => {
            if (percent > maxPercent) {
                maxPercent = percent;
                topEmotion = emotion;
            }
        });

        return { emotion: topEmotion, percent: maxPercent };
    };

    const topEmotion = getTopEmotion();

    return (
        <div className="analytics">
            <h2>📊 Session Analytics</h2>

            <div className="analytics-grid">
                {/* Overview Cards */}
                <div className="stat-card">
                    <div className="stat-icon">⏱️</div>
                    <div className="stat-content">
                        <div className="stat-label">Session Duration</div>
                        <div className="stat-value">
                            {sessionInfo?.duration_formatted || '0s'}
                        </div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">📈</div>
                    <div className="stat-content">
                        <div className="stat-label">Average Stress</div>
                        <div className="stat-value">
                            {((analytics.average_stress || 0) * 100).toFixed(1)}%
                        </div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">🔺</div>
                    <div className="stat-content">
                        <div className="stat-label">Peak Stress</div>
                        <div className="stat-value">
                            {((analytics.peak_stress || 0) * 100).toFixed(1)}%
                        </div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">⚠️</div>
                    <div className="stat-content">
                        <div className="stat-label">High Stress Time</div>
                        <div className="stat-value">
                            {(analytics.high_stress_percentage || 0).toFixed(1)}%
                        </div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">😊</div>
                    <div className="stat-content">
                        <div className="stat-label">Dominant Emotion</div>
                        <div className="stat-value emotion-text">
                            {topEmotion.emotion}
                        </div>
                        <div className="stat-subvalue">
                            {topEmotion.percent.toFixed(1)}% of time
                        </div>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">📊</div>
                    <div className="stat-content">
                        <div className="stat-label">Data Points</div>
                        <div className="stat-value">
                            {analytics.data_points || 0}
                        </div>
                    </div>
                </div>
            </div>

            {/* Emotion Distribution */}
            <div className="emotion-distribution">
                <h3>Emotion Distribution</h3>
                <div className="emotion-bars">
                    {Object.entries(emotions).map(([emotion, percent]) => (
                        <div key={emotion} className="emotion-bar-item">
                            <div className="emotion-bar-label">
                                <span className="emotion-name">{emotion}</span>
                                <span className="emotion-percent">{percent.toFixed(1)}%</span>
                            </div>
                            <div className="emotion-bar-track">
                                <div
                                    className="emotion-bar-fill"
                                    style={{ width: `${percent}%` }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Analytics;
