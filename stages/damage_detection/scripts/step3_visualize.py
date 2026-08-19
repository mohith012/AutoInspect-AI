"""
step3_visualize.py
------------------
STEP 3: Visualize annotations - original image → annotation overlay → damage region highlighted

Saves 5 sample visualizations to: Car project/visualizations/

Run: python step3_visualize.py
"""
import json
import os
import cv2
import numpy as np
import random

BASE       = r'C:\Users\sango\OneDrive\Desktop\Car project\CarDD_release\CarDD_release\CarDD_COCO'
IMG_DIR    = os.path.join(BASE, 'train2017')
TRAIN_JSON = os.path.join(BASE, 'annotations', 'instances_train2017.json')
OUT_DIR    = r'C:\Users\sango\OneDrive\Desktop\Car project\visualizations'
os.makedirs(OUT_DIR, exist_ok=True)

# Color palette per class (BGR)
PALETTE = {
    1: (0, 100, 255),    # dent          – orange
    2: (0, 255, 100),    # scratch       – green
    3: (0, 60, 255),     # crack         – red
    4: (255, 200, 0),    # glass shatter – cyan
    5: (200, 0, 255),    # lamp broken   – magenta
    6: (0, 220, 220),    # tire flat     – yellow
}

with open(TRAIN_JSON) as f:
    data = json.load(f)

cat_map  = {c['id']: c['name'] for c in data['categories']}
img_map  = {img['id']: img for img in data['images']}

# Build image_id → list of annotations
from collections import defaultdict
ann_map = defaultdict(list)
for a in data['annotations']:
    ann_map[a['image_id']].append(a)

# Pick 5 images that have annotations
random.seed(42)
candidates = [iid for iid, anns in ann_map.items() if len(anns) >= 1]
sample_ids = random.sample(candidates, min(5, len(candidates)))

for i, img_id in enumerate(sample_ids):
    img_info = img_map[img_id]
    img_path = os.path.join(IMG_DIR, img_info['file_name'])
    if not os.path.isfile(img_path):
        print(f'Image not found: {img_path}')
        continue

    img_orig = cv2.imread(img_path)
    overlay  = img_orig.copy()

    annotations = ann_map[img_id]
    for ann in annotations:
        cat_id = ann['category_id']
        color  = PALETTE.get(cat_id, (255, 255, 255))
        label  = cat_map[cat_id]

        # Draw filled segmentation polygon (semi-transparent)
        segs = ann.get('segmentation', [])
        for seg in segs:
            pts = np.array(seg, dtype=np.float32).reshape(-1, 2).astype(np.int32)
            cv2.fillPoly(overlay, [pts], color)

        # Draw bounding box
        x, y, w, h = [int(v) for v in ann['bbox']]
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, 3)

        # Label text
        cv2.putText(overlay, label, (x, max(y - 8, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)

    # Blend for transparency
    vis = cv2.addWeighted(img_orig, 0.45, overlay, 0.55, 0)

    # Side-by-side: original | annotated
    h_img, w_img = img_orig.shape[:2]
    combined = np.zeros((h_img, w_img * 2 + 10, 3), dtype=np.uint8)
    combined[:, :w_img]              = img_orig
    combined[:, w_img + 10:]         = vis

    cv2.putText(combined, 'Original', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(combined, 'Annotation overlay', (w_img + 20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    out_path = os.path.join(OUT_DIR, f'sample_{i+1}_{img_info["file_name"]}')
    cv2.imwrite(out_path, combined)
    print(f'Saved: {out_path}')

print(f'\nDone. Open the {OUT_DIR} folder to see the visualizations.')
