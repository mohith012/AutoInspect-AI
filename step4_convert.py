"""
step4_convert.py
----------------
STEP 4: Convert COCO format → YOLO txt format for YOLOv8 fine-tuning.

COCO bbox  : [x_top_left, y_top_left, width, height]  (absolute pixels)
YOLO bbox  : [x_center, y_center, width, height]       (normalised 0-1)

Produces:
  Car project/
  └─ cardd_yolo/
     ├─ train/
     │   ├─ images/   (symlinks or copies)
     │   └─ labels/   (.txt files)
     ├─ val/
     │   ├─ images/
     │   └─ labels/
     └─ test/
         ├─ images/
         └─ labels/

Run: python step4_convert.py
"""
import json
import os
import shutil
from pathlib import Path

BASE      = r'C:\Users\sango\OneDrive\Desktop\Car project\CarDD_release\CarDD_release\CarDD_COCO'
OUT_ROOT  = r'C:\Users\sango\OneDrive\Desktop\Car project\cardd_yolo'

SPLITS = {
    'train': ('train2017', 'instances_train2017.json'),
    'val':   ('val2017',   'instances_val2017.json'),
    'test':  ('test2017',  'instances_test2017.json'),
}

def coco_to_yolo(bbox, img_w, img_h):
    x, y, w, h = bbox
    xc = (x + w / 2) / img_w
    yc = (y + h / 2) / img_h
    wn = w / img_w
    hn = h / img_h
    return xc, yc, wn, hn

for split, (img_folder, json_name) in SPLITS.items():
    json_path = os.path.join(BASE, 'annotations', json_name)
    img_dir   = os.path.join(BASE, img_folder)

    out_img_dir = os.path.join(OUT_ROOT, split, 'images')
    out_lbl_dir = os.path.join(OUT_ROOT, split, 'labels')
    os.makedirs(out_img_dir, exist_ok=True)
    os.makedirs(out_lbl_dir, exist_ok=True)

    with open(json_path) as f:
        data = json.load(f)

    # COCO category_id starts at 1; YOLO class index starts at 0
    # Build sorted mapping: cat_id (1-based) → yolo_idx (0-based)
    cats_sorted = sorted(data['categories'], key=lambda c: c['id'])
    cat_id_to_yolo = {c['id']: i for i, c in enumerate(cats_sorted)}

    img_map = {img['id']: img for img in data['images']}

    from collections import defaultdict
    ann_map = defaultdict(list)
    for a in data['annotations']:
        ann_map[a['image_id']].append(a)

    copied = 0
    for img_id, img_info in img_map.items():
        src = os.path.join(img_dir, img_info['file_name'])
        dst = os.path.join(out_img_dir, img_info['file_name'])
        if not os.path.isfile(src):
            continue
        if not os.path.isfile(dst):
            shutil.copy2(src, dst)
        copied += 1

        # Write label file
        lbl_file = os.path.join(out_lbl_dir, Path(img_info['file_name']).stem + '.txt')
        lines = []
        for ann in ann_map.get(img_id, []):
            yolo_cls = cat_id_to_yolo[ann['category_id']]
            xc, yc, wn, hn = coco_to_yolo(ann['bbox'], img_info['width'], img_info['height'])
            # Clamp to [0,1]
            xc = max(0.0, min(1.0, xc))
            yc = max(0.0, min(1.0, yc))
            wn = max(0.0, min(1.0, wn))
            hn = max(0.0, min(1.0, hn))
            lines.append(f'{yolo_cls} {xc:.6f} {yc:.6f} {wn:.6f} {hn:.6f}')
        with open(lbl_file, 'w') as lf:
            lf.write('\n'.join(lines))

    print(f'[{split}] {copied} images copied, labels written.')

# Write data YAML
yaml_content = f"""train: {OUT_ROOT}/train/images
val:   {OUT_ROOT}/val/images
test:  {OUT_ROOT}/test/images

nc: 6
names: ["dent", "scratch", "crack", "glass_shatter", "lamp_broken", "tire_flat"]
"""
yaml_path = r'C:\Users\sango\OneDrive\Desktop\Car project\cardd_data.yaml'
with open(yaml_path, 'w') as f:
    f.write(yaml_content)
print(f'\nData YAML updated: {yaml_path}')
print('Conversion complete! Run step5_train.py next.')
