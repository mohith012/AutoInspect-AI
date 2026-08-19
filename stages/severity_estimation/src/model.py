import torch.nn as nn
import torchvision.models as models

def get_severity_model(num_classes=3, freeze_backbone=True):
    """
    Returns a pretrained MobileNetV2 model modified for severity classification.
    """
    # Load pretrained MobileNetV2
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
    
    if freeze_backbone:
        for param in model.parameters():
            param.requires_grad = False
            
    # Replace the classification head
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(in_features, 128),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(128, num_classes)
    )
    
    return model
