"""
step5_train.py
--------------
STEP 5: Fine-tune pretrained YOLOv8n on CarDD dataset (6 damage classes).
        Uses the pre-downloaded yolov8n.pt weights (COCO pretrained).
        No hyperparameter optimisation at this stage – just a working baseline.

Run: python step5_train.py
"""
import torch
from pathlib import Path
from ultralytics import YOLO

# ---------- config ----------
DATA_CFG   = r'C:\Users\sango\OneDrive\Desktop\Car project\cardd_data.yaml'
OUTPUT_DIR = r'C:\Users\sango\OneDrive\Desktop\Car project\cardd_model'
WEIGHTS    = r'C:\Users\sango\OneDrive\Desktop\Car project\cardd_model\exp\weights\last.pt'  # resume from epoch 30
EPOCHS     = 50
IMG_SIZE   = 640
BATCH      = 16  # RTX 2050 4GB – reduce to 8 if OOM
DEVICE     = '0' if torch.cuda.is_available() else 'cpu'
# ----------------------------

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

print(f'Using device: {DEVICE}')
print(f'Resuming training from: {WEIGHTS}')
model = YOLO(WEIGHTS)

results = model.train(
    data=DATA_CFG,
    epochs=EPOCHS,
    imgsz=IMG_SIZE,
    batch=BATCH,
    device=DEVICE,
    project=OUTPUT_DIR,
    name='exp',
    exist_ok=True,          # continue in same folder
    resume=True,            # resume from last.pt checkpoint
    save=True,
    save_period=10,
    optimizer='SGD',
    lr0=0.01,
    patience=20,            # early-stop if no improvement for 20 epochs
    workers=0,              # required on Windows to avoid multiprocessing spawn error
    verbose=True,
)

best_pt = Path(OUTPUT_DIR) / 'exp' / 'weights' / 'best.pt'
if best_pt.is_file():
    print(f'\n✅ Training done! Best model: {best_pt}')
else:
    print('\n⚠️  Training finished but best.pt not found – check logs above.')
