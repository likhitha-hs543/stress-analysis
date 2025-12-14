/**
 * Stress Timeline Component
 * Real-time chart showing stress levels over time
 */
import React, { useEffect, useRef } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import './StressTimeline.css';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const StressTimeline = ({ timelineData }) => {
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#e2e8f0',
                    font: { size: 12 }
                }
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                titleColor: '#e2e8f0',
                bodyColor: '#94a3b8',
                borderColor: 'rgba(59, 130, 246, 0.3)',
                borderWidth: 1
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(148, 163, 184, 0.1)'
                },
                ticks: {
                    color: '#94a3b8',
                    maxRotation: 45,
                    minRotation: 45
                }
            },
            y: {
                min: 0,
                max: 1,
                grid: {
                    color: 'rgba(148, 163, 184, 0.1)'
                },
                ticks: {
                    color: '#94a3b8',
                    callback: (value) => `${(value * 100).toFixed(0)}%`
                }
            }
        },
        interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
        }
    };

    // Prepare chart data
    const prepareChartData = () => {
        if (!timelineData || timelineData.length === 0) {
            return {
                labels: [],
                datasets: []
            };
        }

        const labels = timelineData.map(d => {
            const date = new Date(d.timestamp * 1000);
            return date.toLocaleTimeString();
        });

        return {
            labels,
            datasets: [
                {
                    label: 'Combined Stress',
                    data: timelineData.map(d => d.stress_score),
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }
            ]
        };
    };

    return (
        <div className="stress-timeline">
            <div className="timeline-header">
                <h2>📈 Stress Timeline</h2>
                <p className="timeline-subtitle">
                    Real-time stress levels (Last {timelineData?.length || 0} readings)
                </p>
            </div>
            <div className="chart-container">
                <Line options={chartOptions} data={prepareChartData()} />
            </div>
        </div>
    );
};

export default StressTimeline;
