"""
Video Emotion Model
CNN model for facial emotion recognition
"""
import numpy as np
import torch
import torch.nn as nn
import config


class VideoEmotionCNN(nn.Module):
    """
    CNN architecture for facial emotion recognition
    Input: 48x48 grayscale face image
    Output: Emotion probabilities (7 classes)
    """
    
    def __init__(self, num_classes=7):
        """
        Args:
            num_classes: Number of emotion classes
        """
        super(VideoEmotionCNN, self).__init__()
        
        self.num_classes = num_classes
        
        # Convolutional blocks
        # Block 1
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2, 2)  # 48x48 -> 24x24
        self.dropout1 = nn.Dropout2d(0.25)
        
        # Block 2
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(2, 2)  # 24x24 -> 12x12
        self.dropout2 = nn.Dropout2d(0.25)
        
        # Block 3
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(256)
        self.relu3 = nn.ReLU()
        self.pool3 = nn.MaxPool2d(2, 2)  # 12x12 -> 6x6
        self.dropout3 = nn.Dropout2d(0.25)
        
        # Block 4
        self.conv4 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(512)
        self.relu4 = nn.ReLU()
        self.pool4 = nn.MaxPool2d(2, 2)  # 6x6 -> 3x3
        self.dropout4 = nn.Dropout2d(0.25)
        
        # Fully connected layers
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(512 * 3 * 3, 512)
        self.relu5 = nn.ReLU()
        self.dropout5 = nn.Dropout(0.5)
        
        self.fc2 = nn.Linear(512, 256)
        self.relu6 = nn.ReLU()
        self.dropout6 = nn.Dropout(0.5)
        
        self.fc3 = nn.Linear(256, num_classes)
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self, x):
        """
        Forward pass
        
        Args:
            x: Input tensor of shape (batch, 1, 48, 48)
            
        Returns:
            Emotion probabilities (batch, num_classes)
        """
        # Convolutional blocks
        x = self.dropout1(self.pool1(self.relu1(self.bn1(self.conv1(x)))))
        x = self.dropout2(self.pool2(self.relu2(self.bn2(self.conv2(x)))))
        x = self.dropout3(self.pool3(self.relu3(self.bn3(self.conv3(x)))))
        x = self.dropout4(self.pool4(self.relu4(self.bn4(self.conv4(x)))))
        
        # Fully connected layers
        x = self.flatten(x)
        x = self.dropout5(self.relu5(self.fc1(x)))
        x = self.dropout6(self.relu6(self.fc2(x)))
        x = self.fc3(x)
        x = self.softmax(x)
        
        return x


class VideoEmotionModel:
    """Wrapper class for video emotion model inference"""
    
    def __init__(self, model_path=None, device='cpu'):
        """
        Initialize video emotion model
        
        Args:
            model_path: Path to saved model weights
            device: 'cpu' or 'cuda'
        """
        self.device = torch.device(device)
        self.model = VideoEmotionCNN(
            num_classes=len(config.EMOTION_LABELS)
        ).to(self.device)
        
        # Load pre-trained weights if available
        if model_path and model_path.exists():
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                print(f"Loaded video emotion model from {model_path}")
            except Exception as e:
                print(f"Could not load model weights: {e}")
                print("Using randomly initialized weights (for demo purposes)")
        else:
            print("No pre-trained model found. Using randomly initialized weights.")
            print("Note: In production, you should train or download a pre-trained model.")
        
        self.model.eval()  # Set to evaluation mode
        
    def predict(self, face_image):
        """
        Predict emotion from face image
        
        Args:
            face_image: Grayscale face image (48x48 numpy array, normalized [0,1])
            
        Returns:
            Tuple of (predicted_emotion, probabilities, confidence)
        """
        with torch.no_grad():
            # Convert to tensor and add batch and channel dimensions
            # Shape: (1, 1, 48, 48)
            x = torch.FloatTensor(face_image).unsqueeze(0).unsqueeze(0).to(self.device)
            
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
    
    def predict_batch(self, face_images):
        """
        Predict emotions for a batch of face images
        
        Args:
            face_images: List of grayscale face images
            
        Returns:
            List of predictions
        """
        predictions = []
        for img in face_images:
            pred = self.predict(img)
            predictions.append(pred)
        return predictions
