/**
 * Alert Panel Component
 * Displays alerts and recommendations
 */
import React from 'react';
import './AlertPanel.css';

const AlertPanel = ({ alerts, sessionInfo }) => {
    const status = sessionInfo?.status || 'normal';

    const getStatusDisplay = () => {
        if (status === 'at_risk') {
            return { text: 'At Risk', color: '#ef4444', icon: '⚠️' };
        }
        return { text: 'Normal', color: '#10b981', icon: '✅' };
    };

    const statusDisplay = getStatusDisplay();

    return (
        <div className="alert-panel">
            <div className="panel-header">
                <h2>🚨 Alerts & Recommendations</h2>
                <div
                    className="status-badge"
                    style={{ backgroundColor: `${statusDisplay.color}20`, borderColor: statusDisplay.color }}
                >
                    <span className="status-icon">{statusDisplay.icon}</span>
                    <span className="status-text" style={{ color: statusDisplay.color }}>
                        {statusDisplay.text}
                    </span>
                </div>
            </div>

            {/* Active Alerts */}
            {alerts && alerts.length > 0 ? (
                <div className="alerts-list">
                    {alerts.map((alert, index) => (
                        <div key={index} className={`alert-card alert-${alert.severity}`}>
                            <div className="alert-header">
                                <span className="alert-icon">
                                    {alert.severity === 'high' ? '🔴' : '🟡'}
                                </span>
                                <h3 className="alert-title">{alert.title}</h3>
                                <span className="alert-priority">{alert.priority}</span>
                            </div>
                            <p className="alert-message">{alert.message}</p>

                            {alert.recommendations && (
                                <div className="recommendations">
                                    <h4>Recommendations:</h4>
                                    <ul>
                                        {alert.recommendations.map((rec, idx) => (
                                            <li key={idx}>{rec}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            ) : (
                <div className="no-alerts">
                    <div className="no-alerts-icon">✨</div>
                    <p>No active alerts. Worker is doing well!</p>
                </div>
            )}

            {/* General Recommendations */}
            <div className="general-recommendations">
                <h3>💡 General Tips</h3>
                <div className="tips-grid">
                    <div className="tip-card">
                        <span className="tip-icon">🧘</span>
                        <p>Take regular breaks every 60-90 minutes</p>
                    </div>
                    <div className="tip-card">
                        <span className="tip-icon">💧</span>
                        <p>Stay hydrated throughout the day</p>
                    </div>
                    <div className="tip-card">
                        <span className="tip-icon">🌬️</span>
                        <p>Practice deep breathing exercises</p>
                    </div>
                    <div className="tip-card">
                        <span className="tip-icon">👥</span>
                        <p>Don't hesitate to ask for support</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AlertPanel;
