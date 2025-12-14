/**
 * Media Stream Service
 * Handles camera and microphone capture
 */

class MediaStreamService {
    constructor() {
        this.audioContext = null;
        this.videoStream = null;
        this.audioStream = null;
        this.mediaRecorder = null;
        this.isCapturing = false;
    }

    async requestPermissions() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                },
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 16000
                }
            });

            // Split into video and audio streams
            const videoTracks = stream.getVideoTracks();
            const audioTracks = stream.getAudioTracks();

            this.videoStream = new MediaStream(videoTracks);
            this.audioStream = new MediaStream(audioTracks);

            return { video: true, audio: true };
        } catch (error) {
            console.error('Error requesting media permissions:', error);
            throw error;
        }
    }

    getVideoStream() {
        return this.videoStream;
    }

    getAudioStream() {
        return this.audioStream;
    }

    captureVideoFrame(videoElement) {
        if (!videoElement) return null;

        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoElement, 0, 0);

        // Convert to base64 JPEG
        const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
        const base64 = dataUrl.split(',')[1];

        return base64;
    }

    startAudioCapture(onAudioData, chunkDuration = 3000) {
        if (!this.audioStream) {
            console.error('Audio stream not initialized');
            return;
        }

        this.audioContext = new (window.AudioContext || window.webkitAudioContext)({
            sampleRate: 16000
        });

        const source = this.audioContext.createMediaStreamSource(this.audioStream);
        const processor = this.audioContext.createScriptProcessor(4096, 1, 1);

        let audioBuffer = [];
        let lastSendTime = Date.now();

        processor.onaudioprocess = (e) => {
            const inputData = e.inputBuffer.getChannelData(0);
            audioBuffer.push(...inputData);

            // Send chunk every chunkDuration milliseconds
            const now = Date.now();
            if (now - lastSendTime >= chunkDuration) {
                const chunk = new Float32Array(audioBuffer);
                const base64 = this.arrayBufferToBase64(chunk.buffer);
                onAudioData(base64);

                // Reset buffer
                audioBuffer = [];
                lastSendTime = now;
            }
        };

        source.connect(processor);
        processor.connect(this.audioContext.destination);

        this.processor = processor;
        this.source = source;
        this.isCapturing = true;
    }

    stopAudioCapture() {
        if (this.processor) {
            this.processor.disconnect();
            this.source.disconnect();
        }
        if (this.audioContext) {
            this.audioContext.close();
        }
        this.isCapturing = false;
    }

    arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        const len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return btoa(binary);
    }

    stopAllStreams() {
        if (this.videoStream) {
            this.videoStream.getTracks().forEach(track => track.stop());
        }
        if (this.audioStream) {
            this.audioStream.getTracks().forEach(track => track.stop());
        }
        this.stopAudioCapture();
    }
}

// Export singleton instance
const mediaService = new MediaStreamService();
export default mediaService;
