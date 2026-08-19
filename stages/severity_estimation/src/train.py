import os
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

def train_model(model, train_loader, val_loader, num_epochs=10, save_dir='../models'):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=0.001)
    
    os.makedirs(save_dir, exist_ok=True)
    best_val_loss = float('inf')
    best_model_path = os.path.join(save_dir, 'severity_model_best.pt')
    
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        train_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs} [Train]")
        for inputs, labels in train_bar:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            train_bar.set_postfix(loss=loss.item(), acc=100.*correct/total)
            
        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            val_bar = tqdm(val_loader, desc=f"Epoch {epoch+1}/{num_epochs} [Val]")
            for inputs, labels in val_bar:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
                
                val_bar.set_postfix(loss=loss.item(), acc=100.*val_correct/val_total)
        
        avg_val_loss = val_loss / len(val_loader)
        avg_val_acc = 100. * val_correct / val_total
        
        print(f"Epoch {epoch+1} - Val Loss: {avg_val_loss:.4f}, Val Acc: {avg_val_acc:.2f}%")
        
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            print(f"Saving best model to {best_model_path}")
            torch.save(model.state_dict(), best_model_path)
            
    print("Training complete.")
    return best_model_path

if __name__ == "__main__":
    from dataset import get_dataloaders
    from model import get_severity_model
    
    data_dir = '../data/raw/kaggle_severity_dataset/data3a'
    train_loader, val_loader, idx_to_class = get_dataloaders(data_dir, batch_size=32)
    
    print("Class mapping:", idx_to_class)
    
    model = get_severity_model(num_classes=3)
    train_model(model, train_loader, val_loader, num_epochs=10)
