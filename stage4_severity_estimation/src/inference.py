import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms
from model import get_severity_model
import os

class SeverityPredictor:
    def __init__(self, model_path, threshold=0.40):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load the model
        self.model = get_severity_model(num_classes=3)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model = self.model.to(self.device)
        self.model.eval()
        
        self.threshold = threshold
        
        # Kaggle dataset order is usually minor, moderate, severe based on alphabetical or index
        # 01-minor, 02-moderate, 03-severe -> [minor, moderate, severe]
        self.classes = ['minor', 'moderate', 'severe']
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    def predict_severity(self, damage_crop):
        """
        Predicts the severity of a damage crop image.
        
        Args:
            damage_crop (PIL.Image or str): A PIL Image or path to an image.
            
        Returns:
            dict: {
                "severity": str,
                "confidence": float,
                "probabilities": dict
            }
        """
        if isinstance(damage_crop, str):
            damage_crop = Image.open(damage_crop).convert('RGB')
            
        input_tensor = self.transform(damage_crop).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probs = F.softmax(outputs, dim=1)[0]
            
        confidence, predicted_idx = torch.max(probs, 0)
        confidence = confidence.item()
        
        probabilities = {self.classes[i]: probs[i].item() for i in range(len(self.classes))}
        
        if confidence < self.threshold:
            severity = "uncertain"
        else:
            severity = self.classes[predicted_idx.item()]
            
        return {
            "severity": severity,
            "confidence": round(confidence, 2),
            "probabilities": {k: round(v, 2) for k, v in probabilities.items()}
        }
