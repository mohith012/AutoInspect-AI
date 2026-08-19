"""
train_cardd.py
--------------
Train a YOLOv8‑n baseline on the CarDD dataset (multiclass damage detection).

Usage:
    python train_cardd.py
"""

import os
from pathlib import Path
from ultralytics import YOLO
import torch

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
PROJECT_ROOT = Path(r"C:\Users\sango\OneDrive\Desktop\Car project")
DATA_CFG      = PROJECT_ROOT / "stages/damage_detection/configs/cardd_data.yaml"            # YOLO data file
OUTPUT_DIR    = PROJECT_ROOT / "cardd_model"               # where weights will be saved
EPOCHS        = 50
IMG_SIZE      = 640
BATCH_SIZE    = 16
# ----------------------------------------------------------------------

def main() -> None:
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load a fresh YOLOv8 nano model (pre‑trained on COCO)
    model = YOLO("yolov8n.pt")

    # Train – the trainer will automatically create runs/ folders under OUTPUT_DIR
    model.train(
        data=str(DATA_CFG),
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH_SIZE,
        project=str(OUTPUT_DIR),
        name="exp",
        device="cpu" if not torch.cuda.is_available() else "0",  # auto‑detect GPU
        save=True,
        save_period=10,
        optimizer="SGD",
        patience=20,                 # early‑stop if no improvement
    )

    # After training, the best checkpoint is saved as `best.pt`
    best_weight = OUTPUT_DIR / "exp" / "weights" / "best.pt"
    if best_weight.is_file():
        print(f"\n✅ Training finished. Best model saved to: {best_weight}\n")
    else:
        print("\n⚠️ Training finished but best.pt not found. Check training logs.\n")


if __name__ == "__main__":
    main()
