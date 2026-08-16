import os
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch

def get_transforms(is_train=True):
    if is_train:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

def get_dataloaders(data_dir, batch_size=32):
    train_dir = os.path.join(data_dir, 'training')
    val_dir = os.path.join(data_dir, 'validation')
    
    train_dataset = datasets.ImageFolder(train_dir, transform=get_transforms(is_train=True))
    val_dataset = datasets.ImageFolder(val_dir, transform=get_transforms(is_train=False))
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    
    # Class mapping mapping to our target classes: minor, moderate, severe
    # Assuming Kaggle dataset folders are '01-minor', '02-moderate', '03-severe'
    idx_to_class = {v: k.split('-')[-1].lower() for k, v in train_dataset.class_to_idx.items()}
    
    return train_loader, val_loader, idx_to_class
