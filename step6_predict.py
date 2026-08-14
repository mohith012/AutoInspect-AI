"""
step6_predict.py
----------------
STEP 6: Test the fine-tuned model on unseen images.

Usage:
    python step6_predict.py path\to\car.jpg

Output:
    === Damage Detection Result ===
    Damage detected : scratch
    Confidence      : 91.3%
    Location        : front center
    ==============================
"""
import sys
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO

MODEL_PATH = Path(r'C:\Users\sango\OneDrive\Desktop\Car project\cardd_model\exp\weights\best.pt')

# Horizontal thirds × vertical halves → region label
def bbox_to_region(box_xywh, img_h, img_w):
    """Convert normalised xywh to a human-readable region string."""
    xc, yc, w, h = box_xywh
    # Convert to absolute
    xc_abs = xc * img_w
    yc_abs = yc * img_h

    if xc_abs < img_w / 3:
        horiz = 'left'
    elif xc_abs > img_w * 2 / 3:
        horiz = 'right'
    else:
        horiz = 'center'

    vert = 'upper' if yc_abs < img_h / 2 else 'lower'
    return f'{vert} {horiz}'


def predict(image_path: str):
    if not MODEL_PATH.is_file():
        print(f'❌ Model not found at {MODEL_PATH}')
        print('   Run step5_train.py first to fine-tune the model.')
        return

    model = YOLO(str(MODEL_PATH))
    img_path = Path(image_path)
    if not img_path.is_file():
        print(f'❌ Image not found: {img_path}')
        return

    img = cv2.imread(str(img_path))
    h, w = img.shape[:2]

    results = model.predict(str(img_path), verbose=False, conf=0.25)

    if not results or not results[0].boxes or len(results[0].boxes) == 0:
        print('\n🔍 No damage detected in the image.\n')
        return

    boxes = results[0].boxes
    confidences = boxes.conf.cpu().numpy()
    best_idx = int(np.argmax(confidences))
    best_box = boxes[best_idx]

    cls_id     = int(best_box.cls.cpu().item())
    class_name = model.names[cls_id]
    confidence = float(confidences[best_idx]) * 100.0
    xywh_norm  = best_box.xywhn.cpu().numpy()[0]  # normalised [xc, yc, w, h]
    region     = bbox_to_region(xywh_norm, h, w)

    print()
    print('=== Damage Detection Result ===')
    print(f'Damage detected : {class_name}')
    print(f'Confidence      : {confidence:.1f}%')
    print(f'Location        : {region} region')
    print('================================')
    print()

    # Also print all detections if more than one
    if len(confidences) > 1:
        print('--- All detections ---')
        for i, box in enumerate(boxes):
            c   = int(box.cls.cpu().item())
            cf  = float(box.conf.cpu().item()) * 100.0
            xywh = box.xywhn.cpu().numpy()[0]
            reg = bbox_to_region(xywh, h, w)
            print(f'  [{i+1}] {model.names[c]:<20s} {cf:.1f}%  @ {reg}')
        print()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python step6_predict.py <path_to_car_image>')
        sys.exit(1)
    predict(sys.argv[1])
