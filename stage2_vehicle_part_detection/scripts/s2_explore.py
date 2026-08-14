"""
s2_explore.py
-------------
STAGE 2 - STEP 1: Explore and understand the Carparts-Seg dataset.
Reports: folder structure, image count, formats, label formats, classes.
"""
import os, glob, yaml, random
from pathlib import Path
from PIL import Image

BASE = Path(r'C:\Users\sango\OneDrive\Desktop\Car project\stage2_vehicle_part_detection\data')

CLASSES = {
    0: 'back_bumper',    1: 'back_door',       2: 'back_glass',
    3: 'back_left_door', 4: 'back_left_light', 5: 'back_light',
    6: 'back_right_door',7: 'back_right_light',8: 'front_bumper',
    9: 'front_door',    10: 'front_glass',     11: 'front_left_door',
   12: 'front_left_light',13:'front_light',   14: 'front_right_door',
   15: 'front_right_light',16:'hood',         17: 'left_mirror',
   18: 'object',        19: 'right_mirror',   20: 'tailgate',
   21: 'trunk',         22: 'wheel'
}

print("=" * 60)
print("STAGE 2 — Dataset Exploration: Carparts-Seg")
print("=" * 60)

for split in ['train', 'val', 'test']:
    imgs = list((BASE / 'images' / split).glob('*'))
    lbls = list((BASE / 'labels' / split).glob('*.txt'))
    print(f"\n[{split.upper()}]")
    print(f"  Images : {len(imgs)}")
    print(f"  Labels : {len(lbls)}")
    if imgs:
        sample = Image.open(imgs[0])
        print(f"  Sample image size : {sample.size} (WxH)")
        print(f"  Sample image format: {imgs[0].suffix}")

# Annotation format inspection
print("\n[ANNOTATION FORMAT — sample label]")
sample_lbl = list((BASE / 'labels' / 'train').glob('*.txt'))[0]
with open(sample_lbl) as f:
    lines = f.readlines()
print(f"  File: {sample_lbl.name}")
print(f"  Lines (annotations): {len(lines)}")
for i, line in enumerate(lines[:3]):
    parts = line.strip().split()
    cls_id = int(parts[0])
    coords = parts[1:]
    n_coords = len(coords)
    print(f"  Line {i+1}: class={cls_id} ({CLASSES[cls_id]}), coord_count={n_coords} ({'segmentation' if n_coords > 4 else 'bbox'})")

# Class distribution
print("\n[CLASS DISTRIBUTION — training set]")
class_counts = {v: 0 for v in CLASSES.values()}
label_files = list((BASE / 'labels' / 'train').glob('*.txt'))
for lf in label_files:
    with open(lf) as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                cid = int(parts[0])
                class_counts[CLASSES[cid]] += 1

total = sum(class_counts.values())
print(f"  Total annotations: {total}")
print(f"  {'Class':<20} {'Count':>6}  {'%':>5}")
print(f"  {'-'*35}")
for cls, cnt in sorted(class_counts.items(), key=lambda x: -x[1]):
    pct = cnt / total * 100
    print(f"  {cls:<20} {cnt:>6}  {pct:>4.1f}%")

print("\n✅ Exploration complete.")
