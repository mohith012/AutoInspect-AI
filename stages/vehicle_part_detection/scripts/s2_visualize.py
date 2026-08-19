"""
s2_visualize.py
---------------
STAGE 2 - STEP 2: Visualize 25 random annotated images from the training set.
Draws segmentation polygons + bounding boxes + class labels.
Saves to: results/visualizations/
"""
import os, random, cv2, numpy as np
from pathlib import Path

BASE   = Path(r'C:\Users\sango\OneDrive\Desktop\Car project\stages/vehicle_part_detection\data')
OUTDIR = Path(r'C:\Users\sango\OneDrive\Desktop\Car project\stages/vehicle_part_detection\results\visualizations')
OUTDIR.mkdir(parents=True, exist_ok=True)

CLASSES = {
    0: 'back_bumper',     1: 'back_door',        2: 'back_glass',
    3: 'back_left_door',  4: 'back_left_light',  5: 'back_light',
    6: 'back_right_door', 7: 'back_right_light', 8: 'front_bumper',
    9: 'front_door',     10: 'front_glass',      11: 'front_left_door',
   12: 'front_left_light',13: 'front_light',    14: 'front_right_door',
   15: 'front_right_light',16: 'hood',           17: 'left_mirror',
   18: 'object',         19: 'right_mirror',     20: 'tailgate',
   21: 'trunk',          22: 'wheel'
}

# Color palette (one per class)
np.random.seed(42)
COLORS = {i: tuple(int(x) for x in np.random.randint(80, 255, 3)) for i in CLASSES}

img_dir = BASE / 'images' / 'train'
lbl_dir = BASE / 'labels' / 'train'
img_files = list(img_dir.glob('*.jpg'))
random.seed(42)
samples = random.sample(img_files, min(25, len(img_files)))

print(f"Visualizing {len(samples)} images...")

for i, img_path in enumerate(samples):
    lbl_path = lbl_dir / (img_path.stem + '.txt')
    if not lbl_path.exists():
        continue

    img = cv2.imread(str(img_path))
    h, w = img.shape[:2]
    overlay = img.copy()

    with open(lbl_path) as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        cls_id = int(parts[0])
        if cls_id not in CLASSES:
            continue
        coords = list(map(float, parts[1:]))
        color = COLORS[cls_id]
        cls_name = CLASSES[cls_id]

        if len(coords) >= 8:
            # Segmentation polygon → draw filled polygon
            pts = np.array([(int(coords[j]*w), int(coords[j+1]*h))
                            for j in range(0, len(coords), 2)], dtype=np.int32)
            cv2.fillPoly(overlay, [pts], color)
            # Bounding box from polygon
            x1, y1 = pts[:, 0].min(), pts[:, 1].min()
            x2, y2 = pts[:, 0].max(), pts[:, 1].max()
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, cls_name, (x1, max(y1-5, 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)
        else:
            # Pure bbox: cx cy w h (normalized)
            cx, cy, bw, bh = coords
            x1 = int((cx - bw/2) * w); y1 = int((cy - bh/2) * h)
            x2 = int((cx + bw/2) * w); y2 = int((cy + bh/2) * h)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, cls_name, (x1, max(y1-5, 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

    # Blend polygon overlay
    result = cv2.addWeighted(overlay, 0.35, img, 0.65, 0)
    out_path = OUTDIR / f'vis_{i+1:02d}_{img_path.stem[:30]}.jpg'
    cv2.imwrite(str(out_path), result)
    print(f"  [{i+1:2d}/25] Saved: {out_path.name}")

print(f"\nAll visualizations saved to: {OUTDIR}")
