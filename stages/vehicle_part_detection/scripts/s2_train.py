"""
s2_train.py
-----------
STAGE 2 - STEP 3: Fine-tune pretrained YOLOv8n on Carparts-Seg (23 vehicle-part classes).

Model  : YOLOv8n (nano) — smallest YOLO, fast on RTX 2050 4GB
Dataset: Carparts-Seg (3,833 images, 23 classes, YOLO segmentation format)
Note   : Using detection head only (not segmentation) for bbox output.
         Segmentation labels are converted to bboxes automatically by Ultralytics.

Run: python scripts/s2_train.py
"""
import torch
from pathlib import Path
from ultralytics import YOLO

# ---------- Config ----------
DATA_CFG   = r'C:\Users\sango\OneDrive\Desktop\Car project\stages/vehicle_part_detection\configs\data.yaml'
OUTPUT_DIR = r'C:\Users\sango\OneDrive\Desktop\Car project\stages/vehicle_part_detection\models'
WEIGHTS    = 'yolov8n.pt'   # pretrained COCO weights — auto-downloaded if not present
EPOCHS     = 50
IMG_SIZE   = 640
BATCH      = 16             # RTX 2050 4GB — reduce to 8 if OOM
DEVICE     = '0' if torch.cuda.is_available() else 'cpu'
# ----------------------------

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

print(f'Device  : {DEVICE}')
print(f'GPU     : {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"}')
print(f'Weights : {WEIGHTS}')

model = YOLO(WEIGHTS)

results = model.train(
    data       = DATA_CFG,
    epochs     = EPOCHS,
    imgsz      = IMG_SIZE,
    batch      = BATCH,
    device     = DEVICE,
    project    = OUTPUT_DIR,
    name       = 'vehicle_parts_v1',
    exist_ok   = True,
    save       = True,
    save_period= 10,
    optimizer  = 'SGD',
    lr0        = 0.01,
    patience   = 20,
    workers    = 0,          # required on Windows
    verbose    = True,
    seed       = 42,
)

best = Path(OUTPUT_DIR) / 'vehicle_parts_v1' / 'weights' / 'best.pt'
if best.exists():
    print(f'\nTraining complete! Best model: {best}')
else:
    print('\nTraining finished - check logs above.')
