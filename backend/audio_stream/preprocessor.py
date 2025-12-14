"""
Audio Preprocessor
Handles noise reduction, normalization, and audio chunk processing
"""
import numpy as np
import noisereduce as nr
from scipy import signal
import config


class AudioPreprocessor:
    """Preprocesses raw audio data for feature extraction"""
    
    def __init__(self, sample_rate=config.AUDIO_SAMPLE_RATE):
        self.sample_rate = sample_rate
        self.chunk_size = int(sample_rate * config.AUDIO_CHUNK_DURATION)
        
    def process_audio_chunk(self, audio_data):
        """
        Process a chunk of audio data
        
        Args:
            audio_data: numpy array of audio samples (int16 or float32)
            
        Returns:
            Processed audio as numpy array (float32, normalized)
        """
        # Convert to float32 if needed
        if audio_data.dtype == np.int16:
            audio_float = audio_data.astype(np.float32) / 32768.0
        else:
            audio_float = audio_data.astype(np.float32)
        
        # Apply noise reduction
        audio_denoised = self._reduce_noise(audio_float)
        
        # Normalize audio
        audio_normalized = self._normalize_audio(audio_denoised)
        
        # Apply pre-emphasis filter (boost high frequencies)
        audio_emphasized = self._pre_emphasis(audio_normalized)
        
        return audio_emphasized
    
    def _reduce_noise(self, audio):
        """
        Reduce background noise using spectral subtraction
        
        Args:
            audio: Input audio signal
            
        Returns:
            Denoised audio signal
        """
        try:
            # Use noisereduce library for noise reduction
            # Estimate noise from first 0.5 seconds
            noise_sample_len = min(int(0.5 * self.sample_rate), len(audio) // 2)
            reduced_noise = nr.reduce_noise(
                y=audio,
                sr=self.sample_rate,
                stationary=True,
                prop_decrease=0.8
            )
            return reduced_noise
        except Exception as e:
            print(f"Noise reduction error: {e}")
            return audio  # Return original if noise reduction fails
    
    def _normalize_audio(self, audio):
        """
        Normalize audio to consistent RMS energy level
        
        Args:
            audio: Input audio signal
            
        Returns:
            Normalized audio signal
        """
        # Calculate RMS energy
        rms = np.sqrt(np.mean(audio ** 2))
        
        if rms > 1e-6:  # Avoid division by zero
            # Target RMS level
            target_rms = 0.1
            normalized = audio * (target_rms / rms)
            
            # Clip to prevent overflow
            normalized = np.clip(normalized, -1.0, 1.0)
            return normalized
        else:
            return audio
    
    def _pre_emphasis(self, audio, coef=0.97):
        """
        Apply pre-emphasis filter to boost high frequencies
        
        Args:
            audio: Input audio signal
            coef: Pre-emphasis coefficient (default 0.97)
            
        Returns:
            Pre-emphasized audio signal
        """
        emphasized = np.append(audio[0], audio[1:] - coef * audio[:-1])
        return emphasized
    
    def validate_audio_chunk(self, audio_data):
        """
        Validate that audio chunk has sufficient energy (not silence)
        
        Args:
            audio_data: Audio signal
            
        Returns:
            Boolean indicating if chunk is valid (not silence)
        """
        # Calculate energy
        energy = np.sum(audio_data ** 2) / len(audio_data)
        
        # Energy threshold for silence detection
        silence_threshold = 1e-4
        
        return energy > silence_threshold
