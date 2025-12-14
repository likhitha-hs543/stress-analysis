"""
Audio Feature Extractor
Extracts acoustic features from preprocessed audio
"""
import numpy as np
import librosa
import config


class AudioFeatureExtractor:
    """Extracts multiple acoustic features from audio signals"""
    
    def __init__(self, sample_rate=config.AUDIO_SAMPLE_RATE):
        self.sample_rate = sample_rate
        self.n_mfcc = config.MFCC_N_COEFF
        self.n_fft = config.MFCC_N_FFT
        self.hop_length = config.MFCC_HOP_LENGTH
        self.fmin = config.PITCH_FMIN
        self.fmax = config.PITCH_FMAX
        
    def extract_features(self, audio_frame):
        """
        Extract all acoustic features from audio frame
        
        Args:
            audio_frame: Preprocessed audio signal (numpy array)
            
        Returns:
            Dictionary containing all extracted features
        """
        features = {}
        
        # Extract MFCC features
        features['mfcc'] = self._extract_mfcc(audio_frame)
        features['mfcc_delta'] = self._extract_mfcc_delta(features['mfcc'])
        features['mfcc_delta2'] = self._extract_mfcc_delta(features['mfcc_delta'])
        
        # Extract pitch (F0) features
        features['pitch_mean'], features['pitch_std'] = self._extract_pitch(audio_frame)
        
        # Extract energy features
        features['energy_mean'], features['energy_std'] = self._extract_energy(audio_frame)
        
        # Extract jitter and shimmer (voice quality)
        features['jitter'] = self._extract_jitter(audio_frame)
        features['shimmer'] = self._extract_shimmer(audio_frame)
        
        # Extract speech rate
        features['speech_rate'] = self._extract_speech_rate(audio_frame)
        
        # Extract zero crossing rate
        features['zcr_mean'] = self._extract_zero_crossing_rate(audio_frame)
        
        # Extract spectral features
        features['spectral_centroid'] = self._extract_spectral_centroid(audio_frame)
        features['spectral_rolloff'] = self._extract_spectral_rolloff(audio_frame)
        
        return features
    
    def _extract_mfcc(self, audio):
        """Extract MFCC coefficients"""
        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=self.sample_rate,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        return mfcc
    
    def _extract_mfcc_delta(self, mfcc):
        """Calculate delta (derivatives) of MFCC"""
        delta = librosa.feature.delta(mfcc)
        return delta
    
    def _extract_pitch(self, audio):
        """
        Extract pitch (fundamental frequency) using PYIN
        
        Returns:
            Mean and standard deviation of pitch
        """
        try:
            f0, voiced_flag, voiced_probs = librosa.pyin(
                audio,
                fmin=self.fmin,
                fmax=self.fmax,
                sr=self.sample_rate
            )
            
            # Filter out unvoiced frames
            f0_voiced = f0[voiced_flag]
            
            if len(f0_voiced) > 0:
                pitch_mean = np.nanmean(f0_voiced)
                pitch_std = np.nanstd(f0_voiced)
            else:
                pitch_mean = 0.0
                pitch_std = 0.0
                
            return pitch_mean, pitch_std
        except Exception as e:
            print(f"Pitch extraction error: {e}")
            return 0.0, 0.0
    
    def _extract_energy(self, audio):
        """
        Extract RMS energy
        
        Returns:
            Mean and standard deviation of energy
        """
        rms = librosa.feature.rms(y=audio, hop_length=self.hop_length)[0]
        energy_mean = np.mean(rms)
        energy_std = np.std(rms)
        return energy_mean, energy_std
    
    def _extract_jitter(self, audio):
        """
        Calculate jitter (pitch period variability)
        Simplified implementation for real-time processing
        
        Returns:
            Jitter value
        """
        try:
            # Estimate period lengths using autocorrelation
            autocorr = librosa.autocorrelate(audio)
            
            # Find peaks (period estimates)
            peaks = librosa.util.peak_pick(
                autocorr,
                pre_max=3,
                post_max=3,
                pre_avg=3,
                post_avg=5,
                delta=0.5,
                wait=10
            )
            
            if len(peaks) > 1:
                # Calculate period differences
                periods = np.diff(peaks)
                jitter = np.std(periods) / (np.mean(periods) + 1e-6)
            else:
                jitter = 0.0
                
            return float(jitter)
        except Exception as e:
            print(f"Jitter extraction error: {e}")
            return 0.0
    
    def _extract_shimmer(self, audio):
        """
        Calculate shimmer (amplitude variability)
        
        Returns:
            Shimmer value
        """
        try:
            # Calculate frame-wise amplitude
            rms = librosa.feature.rms(y=audio, hop_length=self.hop_length)[0]
            
            if len(rms) > 1:
                # Calculate amplitude differences
                amp_diffs = np.abs(np.diff(rms))
                shimmer = np.mean(amp_diffs) / (np.mean(rms) + 1e-6)
            else:
                shimmer = 0.0
                
            return float(shimmer)
        except Exception as e:
            print(f"Shimmer extraction error: {e}")
            return 0.0
    
    def _extract_speech_rate(self, audio):
        """
        Estimate speech rate (syllables per second)
        Using onset detection as proxy
        
        Returns:
            Estimated speech rate
        """
        try:
            # Detect onsets (syllable approximation)
            onset_env = librosa.onset.onset_strength(y=audio, sr=self.sample_rate)
            onsets = librosa.onset.onset_detect(
                onset_envelope=onset_env,
                sr=self.sample_rate,
                units='time'
            )
            
            # Calculate rate
            duration = len(audio) / self.sample_rate
            speech_rate = len(onsets) / duration if duration > 0 else 0.0
            
            return float(speech_rate)
        except Exception as e:
            print(f"Speech rate extraction error: {e}")
            return 0.0
    
    def _extract_zero_crossing_rate(self, audio):
        """Extract zero crossing rate (voice/unvoiced indicator)"""
        zcr = librosa.feature.zero_crossing_rate(audio, hop_length=self.hop_length)[0]
        return float(np.mean(zcr))
    
    def _extract_spectral_centroid(self, audio):
        """Extract spectral centroid (brightness)"""
        centroid = librosa.feature.spectral_centroid(
            y=audio,
            sr=self.sample_rate,
            hop_length=self.hop_length
        )[0]
        return float(np.mean(centroid))
    
    def _extract_spectral_rolloff(self, audio):
        """Extract spectral rolloff"""
        rolloff = librosa.feature.spectral_rolloff(
            y=audio,
            sr=self.sample_rate,
            hop_length=self.hop_length
        )[0]
        return float(np.mean(rolloff))
    
    def get_feature_vector_for_model(self, features):
        """
        Convert feature dictionary to input vector for emotion model
        
        Args:
            features: Dictionary of extracted features
            
        Returns:
            Numpy array ready for model input
        """
        # For MFCC-based models, we typically use MFCC + deltas
        mfcc = features['mfcc']  # Shape: (n_mfcc, time_frames)
        mfcc_delta = features['mfcc_delta']
        mfcc_delta2 = features['mfcc_delta2']
        
        # Stack all MFCC features
        mfcc_combined = np.vstack([mfcc, mfcc_delta, mfcc_delta2])
        
        # Return transposed for (time_frames, features) format
        return mfcc_combined.T
