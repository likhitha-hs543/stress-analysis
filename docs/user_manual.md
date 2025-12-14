# User Manual

## Getting Started

### System Requirements

**Backend:**
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- CPU with support for ML inference (GPU optional)

**Frontend:**
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Microphone and webcam
- Stable internet connection

### Installation

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### Running the Application

#### Start Backend Server

```bash
cd backend
python app.py
```

You should see:
```
Worker Stress Analysis System - Backend Server
============================================================
Host: 0.0.0.0
Port: 5000
Debug: True
============================================================
```

#### Start Frontend

In a new terminal:

```bash
cd frontend
npm start
```

The application will automatically open at `http://localhost:3000`

## Using the Application

### First-Time Setup

1. **Privacy Consent Screen**
   - Read the privacy policy carefully
   - Click "Accept & Continue" to grant camera and microphone permissions
   - Your browser will ask for permission - click "Allow"

2. **Initial Calibration**
   - Position yourself centered in the camera view
   - Ensure good lighting on your face
   - Minimize background noise for best audio quality

### Dashboard Overview

The application consists of 5 main tabs:

#### 📊 Live Monitor

**What you'll see:**
- **Video Feed**: Live camera preview with your face
- **Audio Waveform**: Real-time audio activity visualization
- **Current Emotions**: Detected emotions from voice and face
- **Stress Meter**: Circular gauge showing current stress level

**Color Coding:**
- 🟢 Green (0-33%): Low stress - you're calm and relaxed
- 🟡 Yellow (33-66%): Medium stress - monitor the situation
- 🔴 Red (66-100%): High stress - consider taking a break

**Tips:**
- Keep your face visible and centered
- Speak naturally (don't shout or whisper)
- Good lighting improves facial detection

#### 📈 Timeline

**What you'll see:**
- Real-time line chart showing stress levels over the session
- Last 100 data points displayed

**How to interpret:**
- Rising trend: Stress is increasing
- Flat line: Stress is stable
- Declining trend: Stress is decreasing

**Use cases:**
- Identify peak stress periods during your workday
- See how breaks affect your stress levels
- Track stress recovery over time

#### 📊 Analytics

**What you'll see:**
- **Session Duration**: How long you've been monitored
- **Average Stress**: Your typical stress level this session
- **Peak Stress**: Highest stress point reached
- **High Stress Time**: Percentage of time in high stress
- **Dominant Emotion**: Most frequent emotion detected
- **Emotion Distribution**: Bar chart of all detected emotions

**Tips:**
- Review analytics after meetings or tasks
- Compare different work activities
- Identify patterns in your stress triggers

#### 🚨 Alerts

**What you'll see:**
- **Status Badge**: Normal or At Risk
- **Active Alerts**: Current warnings
- **Recommendations**: Suggested actions
- **General Tips**: Wellness advice

**Alert Types:**

1. **Sustained High Stress**
   - Triggered: Stress ≥70% for 3+ minutes
   - Severity: High
   - Recommendation: Take a 5-10 minute break

2. **Sudden Stress Spike**
   - Triggered: Stress increases ≥30% rapidly
   - Severity: Medium
   - Recommendation: Check for specific triggers

**Responding to Alerts:**
- Take suggested actions seriously
- Step away from stressful tasks
- Practice deep breathing
- Seek support if needed

#### ℹ️ System Info

**What you'll see:**
- **Model Architecture**: How the AI works
- **Privacy Policy**: What data is collected
- **Technical Specs**: System capabilities
- **Disclaimer**: Important limitations

## Best Practices

### For Accurate Detection

1. **Environment**:
   - Work in well-lit area (front or side lighting)
   - Minimize background noise
   - Stable internet connection

2. **Positioning**:
   - Face the camera directly
   - Keep face in frame
   - Maintain normal distance (arm's length)

3. **Natural Behavior**:
   - Speak and act naturally
   - Don't try to "game" the system
   - Authentic emotions are better detected

### For Privacy

1. **Consent**:
   - Only use when you consent to monitoring
   - You can close the tab anytime to stop

2. **Data**:
   - No recordings are saved
   - Close browser tab to clear all session data
   - No data persists after session ends

3. **Sharing**:
   - Don't share your screen if privacy is a concern
   - Session IDs are temporary and don't identify you

## Troubleshooting

### Camera/Microphone Not Working

**Problem**: "No camera detected" or permissions denied

**Solutions**:
1. Check browser permissions (click lock icon in address bar)
2. Ensure no other app is using camera/mic
3. Try refreshing the page
4. Restart browser
5. Check system privacy settings

### No Face Detected

**Problem**: "No face detected in frame"

**Solutions**:
1. Improve lighting (face should be visible)
2. Center your face in camera view
3. Move closer or farther from camera
4. Remove obstructions (masks, hands)
5. Make sure camera lens is clean

### Connection Issues

**Problem**: "Disconnected" status shown

**Solutions**:
1. Check if backend server is running
2. Verify backend is on `http://localhost:5000`
3. Clear browser cache and reload
4. Check firewall settings
5. Restart both frontend and backend

### Inaccurate Results

**Problem**: Emotions or stress levels seem wrong

**Possible Causes**:
1. Poor audio quality (background noise)
2. Poor video quality (low light, face not visible)
3. Models need more context (wait 10-15 seconds)
4. Extreme expressions may be misclassified

**Solutions**:
1. Improve environment (lighting, noise)
2. Allow system to run for longer period
3. Remember: Results are probabilistic, not perfect

## Keyboard Shortcuts

- **Tab Navigation**: Use mouse to click tabs (no keyboard shortcuts yet)
- **Browser Controls**: Use standard browser shortcuts (F5 to refresh, etc.)

## Getting Help

### Check Logs

**Backend Logs**: Check terminal running `python app.py`
**Frontend Logs**: Open browser DevTools (F12) → Console tab

### Common Error Messages

1. **"Failed to connect to WebSocket"**
   - Backend is not running
   - Run `python app.py` in backend directory

2. **"Permission denied"**
   - Click "Allow" when browser asks for camera/mic
   - Check browser settings

3. **"Session not found"**
   - Refresh the page
   - Reconnect to backend

## Privacy & Data

### What is Collected?
- ✅ Facial landmark coordinates (numbers, not images)
- ✅ Audio features (MFCC values, not recordings)
- ✅ Emotion predictions
- ✅ Stress scores
- ✅ Session statistics

### What is NOT Collected?
- ❌ Raw video frames
- ❌ Raw audio recordings
- ❌ Your identity
- ❌ Personal information
- ❌ Browsing history

### Data Retention
- All data stored in browser memory only
- Data cleared when:
  - You close the tab/browser
  - You disconnect
  - Session ends
- Nothing persists on disk

## Updates & Maintenance

### Updating the Application

```bash
# Update backend dependencies
cd backend
pip install -r requirements.txt --upgrade

# Update frontend dependencies
cd frontend
npm update
```

### Clearing Cache

If you experience issues:

```bash
# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Backend
cd backend
pip install -r requirements.txt --force-reinstall
```

## Support

For technical issues or questions:
1. Check this manual first
2. Review error logs
3. Ensure all dependencies are installed
4. Verify system requirements are met

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-14
