"""
predict_cardd.py
----------------
Simple inference script for the trained CarDD model.

Usage:
    python predict_cardd.py <image_path>
"""

import sys
from pathlib import Path
import cv2
import numpy as np
from ultralytics import YOLO

PROJECT_ROOT = Path(r"C:\Users\sango\OneDrive\Desktop\Car project")
MODEL_PATH = PROJECT_ROOT / "cardd_model" / "exp" / "weights" / "best.pt"


def load_model():
    if not MODEL_PATH.is_file():
        sys.exit(f"❌ Model not found at {MODEL_PATH}. Run train_cardd.py first.")
    return YOLO(str(MODEL_PATH))


def region_from_bbox(bbox, img_shape):
    h, w = img_shape[:2]
    xc, yc, bw, bh = bbox
    x1 = int((xc - bw / 2) * w)
    x2 = int((xc + bw / 2) * w)
    y1 = int((yc - bh / 2) * h)
    y2 = int((yc + bh / 2) * h)
    horiz_center = w // 2
    if x2 < horiz_center * 0.4:
        horiz = "left"
    elif x1 > horiz_center * 1.6:
        horiz = "right"
    else:
        horiz = "center"
    vert_center = h // 2
    vert = "front" if y2 < vert_center else "rear"
    return f"{vert} {horiz}".strip()


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python predict_cardd.py <image_path>")
    img_path = Path(sys.argv[1])
    if not img_path.is_file():
        sys.exit(f"❌ Image not found: {img_path}")
    model = load_model()
    results = model.predict(str(img_path), verbose=False)
    if not results or not results[0].boxes:
        print("🔍 No damage detected.")
        return
    boxes = results[0].boxes
    confidences = boxes.conf.cpu().numpy()
    best_idx = np.argmax(confidences)
    best_box = boxes[best_idx]
    cls_id = int(best_box.cls.cpu().item())
    class_name = model.names[cls_id]
    confidence = float(confidences[best_idx]) * 100.0
    img = cv2.imread(str(img_path))
    region = region_from_bbox(best_box.xywh.cpu().numpy()[0], img.shape)
    print("\n=== Damage Detection Result ===")
    print(f"Damage detected : {class_name}")
    print(f"Confidence      : {confidence:.1f}%")
    print(f"Location        : {region}")
    print("==============================\n")

if __name__ == "__main__":
    main()
