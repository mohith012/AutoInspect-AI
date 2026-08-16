import os
import torch
import torch.nn as nn
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from dataset import get_dataloaders
from model import get_severity_model
import json

def evaluate_model(model_path, data_dir, save_dir='../results'):
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(os.path.join(save_dir, 'metrics'), exist_ok=True)
    os.makedirs(os.path.join(save_dir, 'visualizations'), exist_ok=True)
    os.makedirs(os.path.join(save_dir, 'failure_cases'), exist_ok=True)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load dataset
    _, val_loader, idx_to_class = get_dataloaders(data_dir, batch_size=32)
    
    # Load model
    model = get_severity_model(num_classes=3)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())
            
    # Metrics
    classes = [idx_to_class[i] for i in range(len(idx_to_class))]
    
    # Generate classification report
    report = classification_report(all_labels, all_preds, target_names=classes, output_dict=True)
    acc = accuracy_score(all_labels, all_preds)
    
    # Save metrics to JSON
    metrics_file = os.path.join(save_dir, 'metrics', 'evaluation_metrics.json')
    with open(metrics_file, 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(all_labels, all_preds, target_names=classes))
    
    # Generate Confusion Matrix
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Severity Confusion Matrix')
    
    cm_path = os.path.join(save_dir, 'visualizations', 'confusion_matrix.png')
    plt.savefig(cm_path)
    print(f"Saved confusion matrix to {cm_path}")
    
    return report

if __name__ == "__main__":
    data_dir = '../data/raw/kaggle_severity_dataset/data3a'
    model_path = '../models/severity_model_best.pt'
    evaluate_model(model_path, data_dir)
