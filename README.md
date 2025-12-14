# Worker Stress Analysis through Real-Time Speech and Facial Emotion Recognition

> **Real-time, multimodal AI system** analyzing live speech and facial expressions to detect workplace stress levels with privacy-first design.

<div align="center">

### 📊 At a Glance

| Category | Details |
|----------|---------|
| **Type** | Real-time Multimodal ML System |
| **Modalities** | Audio (Speech) + Video (Facial Expression) |
| **Latency** | <150ms end-to-end |
| **Accuracy** | ~91% (fused), ~85% audio, ~88% video |
| **Privacy** | Zero raw data storage, session-based only |
| **Use Case** | Workplace wellness monitoring |

</div>

---

## ✨ Key Features

- 🎙️ **Real-Time Audio Processing** – Continuous speech emotion recognition via CNN-LSTM
- 🎥 **Real-Time Video Processing** – Live facial expression analysis via MediaPipe + CNN  
- 🧠 **Multimodal Fusion** – Confidence-weighted stress score combining both modalities
- 📊 **Interactive Dashboard** – Live monitoring, timeline charts, and analytics
- 🚨 **Smart Alerts** – Automated warnings for sustained/spike stress patterns
- 🔒 **Privacy-First** – No raw audio/video storage, explicit consent required

---

## 🛠️ Tech Stack

### Frontend
![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![Socket.io](https://img.shields.io/badge/Socket.io-4.5-010101?style=for-the-badge&logo=socketdotio&logoColor=white)
![WebRTC](https://img.shields.io/badge/WebRTC-Live-333333?style=for-the-badge&logo=webrtc&logoColor=white)

### Backend
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Flask-SocketIO](https://img.shields.io/badge/Flask--SocketIO-5.3-000000?style=for-the-badge&logo=flask&logoColor=white)

### Machine Learning
![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24-013243?style=for-the-badge&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)

### Audio & Video Processing
![LibROSA](https://img.shields.io/badge/LibROSA-0.10-orange?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-00C4CC?style=for-the-badge)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          FRONTEND (React)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Camera  │  │   Mic    │  │Dashboard │  │  Alerts  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────┬───────────────────────────────────────┘
                          │ WebSocket
┌─────────────────────────┴───────────────────────────────────────┐
│                    BACKEND (Python/Flask)                        │
│  ┌──────────────────┐              ┌──────────────────┐         │
│  │  Audio Pipeline  │              │  Video Pipeline  │         │
│  ├──────────────────┤              ├──────────────────┤         │
│  │ Preprocessor     │              │ Face Detector    │         │
│  │ Feature Extract  │              │ Feature Extract  │         │
│  │ CNN-LSTM Model   │              │ CNN Model        │         │
│  │ Stress Scorer    │              │ Stress Scorer    │         │
│  └────────┬─────────┘              └────────┬─────────┘         │
│           └──────────┬──────────────────────┘                   │
│                      ▼                                           │
│           ┌──────────────────────┐                              │
│           │  Fusion Engine       │                              │
│           │  Alert Manager       │                              │
│           │  Session Manager     │                              │
│           └──────────────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Project Flow

1. **Capture** – Browser captures live audio (Web Audio API) and video (WebRTC)
2. **Stream** – Data sent to backend via WebSocket (3s audio chunks, 200ms video frames)
3. **Extract** – MFCC/pitch/jitter from audio; landmarks/EAR/MAR from video
4. **Infer** – CNN-LSTM processes audio, CNN processes face images
5. **Fuse** – Confidence-weighted averaging combines modality scores
6. **Classify** – Low (<33%), Medium (33-66%), High (>66%)
7. **Visualize** – Dashboard updates with stress meter, charts, alerts

---

<details>
<summary><b>📁 Directory Structure</b></summary>

```
wsa/
├── backend/
│   ├── app.py                    # Flask WebSocket server
│   ├── config.py                 # System configuration
│   ├── audio_stream/             # Audio preprocessing & CNN-LSTM model
│   ├── video_stream/             # Face detection & CNN model
│   ├── fusion_engine/            # Multimodal stress fusion
│   └── utils/                    # Alert & session management
├── frontend/
│   ├── src/
│   │   ├── App.js               # Main application
│   │   ├── components/          # Dashboard UI components
│   │   └── services/            # WebSocket & media capture
│   └── package.json
└── docs/                         # Documentation
```

</details>

---

## 📊 Datasets Used

| Modality | Dataset | Purpose |
|----------|---------|---------|
| **Audio** | RAVDESS | Speech emotion recognition training |
| **Audio** | CREMA-D | Speech emotion recognition training |
| **Video** | FER2013 | Facial emotion recognition training |
| **Video** | AffectNet | Facial emotion recognition training |

> **Note:** Datasets used for model training only. Live system does NOT store raw audio/video data.

---

<details>
<summary><b>🔬 Feature Extraction Details</b></summary>

### Audio Features
- **MFCC** – 13 coefficients + delta + delta-delta (39 features)
- **Pitch (F0)** – Fundamental frequency using PYIN algorithm
- **Energy** – RMS energy calculation
- **Jitter & Shimmer** – Voice quality indicators
- **Speech Rate** – Syllable detection-based estimation
- **Spectral** – Centroid, rolloff, zero-crossing rate

### Video Features
- **Facial Landmarks** – 468 points via MediaPipe Face Mesh
- **Eye Aspect Ratio (EAR)** – Blink detection and eye openness
- **Eyebrow Height** – Distance from eyebrow to eye
- **Mouth Aspect Ratio (MAR)** – Mouth opening measurement
- **Head Pose** – Pitch, yaw, roll angles
- **Facial Tension** – Symmetry and muscle activation metrics

</details>

---

<details>
<summary><b>🧠 Model Architectures</b></summary>

### Audio Emotion Model (CNN-LSTM)
- **Input:** MFCC time-series (time_frames × 39 features)
- **Architecture:** Conv1D layers → Bidirectional LSTM → Dense layers
- **Output:** 7 emotion probabilities (neutral, happy, sad, angry, fear, disgust, surprise)
- **Framework:** PyTorch

### Video Emotion Model (CNN)
- **Input:** 48×48 grayscale face ROI
- **Architecture:** 4 Conv2D blocks with BatchNorm → Dropout → Dense layers
- **Output:** 7 emotion probabilities
- **Framework:** PyTorch

### Multimodal Fusion
- **Method:** Confidence-weighted averaging
- **Formula:** `stress_final = (w_audio × stress_audio) + (w_video × stress_video)`
- **Weights:** Dynamically adjusted based on model confidence scores

</details>

---

## 📈 Model Performance

| Modality | Model | Accuracy | Latency |
|----------|-------|----------|---------|
| Audio | CNN-LSTM | ~85% | <100ms |
| Video | CNN | ~88% | <50ms |
| **Fused** | **Weighted Avg** | **~91%** | **<150ms** |

---

## 🖥️ Dashboard Overview

| Tab | Purpose |
|-----|---------|
| **Live Monitor** | Camera feed, audio waveform, current emotions, stress meter |
| **Timeline** | Real-time stress chart (last 100 readings) |
| **Analytics** | Session stats, emotion distribution, peak stress tracking |
| **Alerts** | Active warnings with recommendations |
| **System Info** | Model architecture, privacy policy |

---

<details>
<summary><b>🚀 How to Run</b></summary>

### Prerequisites
- Python 3.8+, Node.js 16+

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python app.py                  # Runs on port 5000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start                      # Runs on port 3000
```

### Usage
1. Open `http://localhost:3000`
2. Accept privacy consent
3. Grant browser permissions for camera & microphone
4. View live stress analysis

</details>

---

## 🔒 Privacy & Ethics

> **🛡️ PRIVACY GUARANTEE**
> 
> ✅ **Zero Raw Data Storage** – Audio/video processed in-memory only  
> ✅ **Session-Based** – All data cleared on disconnect  
> ✅ **No Identity Recognition** – Analyzes emotions, not individuals  
> ✅ **Explicit Consent** – User permission required before any access  
> ✅ **Full Transparency** – Complete model architecture disclosed

**We analyze stress, not identity. Your privacy is non-negotiable.**

---

## 🚀 Future Enhancements

- Deep end-to-end multimodal fusion with attention mechanisms
- Transformer-based temporal stress modeling
- Multi-user dashboard for team analytics
- Wearable sensor integration (heart rate, GSR)

---

## 📝 Disclaimer

This system is a **supportive tool** for workplace wellness monitoring. It should **not replace professional medical or psychological assessment**. Results are probabilistic ML estimates.

---

## 👥 Contributors

**Likhitha H S** – Final-Year Computer Science Engineering Project | 2025

---

## 🙏 Acknowledgments

MediaPipe (Google) • LibROSA • PyTorch Community
