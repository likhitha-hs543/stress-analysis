"""
Audio Emotion Model
CNN-LSTM model for speech emotion recognition
"""
import numpy as np
import torch
import torch.nn as nn
import config


class AudioEmotionCNN_LSTM(nn.Module):
    """
    CNN-LSTM architecture for audio emotion recognition
    Input: MFCC features (time_frames, mfcc_features)
    Output: Emotion probabilities (7 classes)
    """
    
    def __init__(self, input_dim=39, hidden_dim=128, num_classes=7):
        """
        Args:
            input_dim: Number of input features (13 MFCC + 13 delta + 13 delta2 = 39)
            hidden_dim: LSTM hidden dimension
            num_classes: Number of emotion classes
        """
        super(AudioEmotionCNN_LSTM, self).__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes
        
        # CNN layers for local feature extraction
        self.conv1 = nn.Conv1d(input_dim, 64, kernel_size=5, padding=2)
        self.bn1 = nn.BatchNorm1d(64)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool1d(2)
        
        self.conv2 = nn.Conv1d(64, 128, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm1d(128)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool1d(2)
        
        # LSTM layers for temporal modeling
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=hidden_dim,
            num_layers=2,
            batch_first=True,
            bidirectional=True,
            dropout=0.3
        )
        
        # Fully connected layers
        self.fc1 = nn.Linear(hidden_dim * 2, 64)  # *2 for bidirectional
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(64, num_classes)
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self, x):
        """
        Forward pass
        
        Args:
            x: Input tensor of shape (batch, time_frames, features)
            
        Returns:
            Emotion probabilities (batch, num_classes)
        """
        # Transpose for Conv1d: (batch, features, time)
        x = x.transpose(1, 2)
        
        # CNN layers
        x = self.pool1(self.relu1(self.bn1(self.conv1(x))))
        x = self.pool2(self.relu2(self.bn2(self.conv2(x))))
        
        # Transpose back for LSTM: (batch, time, features)
        x = x.transpose(1, 2)
        
        # LSTM layers
        lstm_out, _ = self.lstm(x)
        
        # Take the last time step output
        x = lstm_out[:, -1, :]
        
        # Fully connected layers
        x = self.fc1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.softmax(x)
        
        return x


class AudioEmotionModel:
    """Wrapper class for audio emotion model inference"""
    
    def __init__(self, model_path=None, device='cpu'):
        """
        Initialize audio emotion model
        
        Args:
            model_path: Path to saved model weights
            device: 'cpu' or 'cuda'
        """
        self.device = torch.device(device)
        self.model = AudioEmotionCNN_LSTM(
            input_dim=39,  # 13 MFCC + 13 delta + 13 delta2
            hidden_dim=128,
            num_classes=len(config.EMOTION_LABELS)
        ).to(self.device)
        
        # Load pre-trained weights if available
        if model_path and model_path.exists():
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                print(f"Loaded audio emotion model from {model_path}")
            except Exception as e:
                print(f"Could not load model weights: {e}")
                print("Using randomly initialized weights (for demo purposes)")
        else:
            print("No pre-trained model found. Using randomly initialized weights.")
            print("Note: In production, you should train or download a pre-trained model.")
        
        self.model.eval()  # Set to evaluation mode
        
    def predict(self, feature_vector):
        """
        Predict emotion from audio features
        
        Args:
            feature_vector: Numpy array of shape (time_frames, features)
            
        Returns:
            Tuple of (predicted_emotion, probabilities, confidence)
        """
        with torch.no_grad():
            # Convert to tensor and add batch dimension
            x = torch.FloatTensor(feature_vector).unsqueeze(0).to(self.device)
            
            # Pad or truncate to fixed length (e.g., 100 frames)
            target_length = 100
            if x.shape[1] < target_length:
                # Pad with zeros
                padding = torch.zeros(1, target_length - x.shape[1], x.shape[2], device=self.device)
                x = torch.cat([x, padding], dim=1)
            elif x.shape[1] > target_length:
                # Truncate
                x = x[:, :target_length, :]
            
            # Forward pass
            probabilities = self.model(x)
            
            # Get prediction
            probs_np = probabilities.cpu().numpy()[0]
            predicted_idx = np.argmax(probs_np)
            predicted_emotion = config.EMOTION_LABELS[predicted_idx]
            confidence = float(probs_np[predicted_idx])
            
            # Convert probabilities to dictionary
            prob_dict = {
                emotion: float(prob)
                for emotion, prob in zip(config.EMOTION_LABELS, probs_np)
            }
            
            return predicted_emotion, prob_dict, confidence
    
    def predict_batch(self, feature_vectors):
        """
        Predict emotions for a batch of feature vectors
        
        Args:
            feature_vectors: List of numpy arrays
            
        Returns:
            List of predictions
        """
        predictions = []
        for fv in feature_vectors:
            pred = self.predict(fv)
            predictions.append(pred)
        return predictions
