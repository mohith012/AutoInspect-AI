"""
step2_explore.py
----------------
STEP 2: Understand the dataset - images, annotations, classes, masks/bboxes, labels

Run: python step2_explore.py
"""
import json
import os

BASE = r'C:\Users\sango\OneDrive\Desktop\Car project\CarDD_release\CarDD_release\CarDD_COCO'
TRAIN_JSON = os.path.join(BASE, 'annotations', 'instances_train2017.json')
VAL_JSON   = os.path.join(BASE, 'annotations', 'instances_val2017.json')
TEST_JSON  = os.path.join(BASE, 'annotations', 'instances_test2017.json')

for split, path in [('TRAIN', TRAIN_JSON), ('VAL', VAL_JSON), ('TEST', TEST_JSON)]:
    with open(path) as f:
        data = json.load(f)
    imgs = data['images']
    anns = data['annotations']

    # Count per class
    cat_map = {c['id']: c['name'] for c in data['categories']}
    counts = {n: 0 for n in cat_map.values()}
    for a in anns:
        counts[cat_map[a['category_id']]] += 1

    print(f'===== {split} =====')
    print(f'  Images      : {len(imgs)}')
    print(f'  Annotations : {len(anns)}')
    print(f'  Classes     :')
    for name, cnt in counts.items():
        print(f'    {name:<20s} {cnt:>5d} instances')
    print()

print('=== ANNOTATION FORMAT ===')
with open(TRAIN_JSON) as f:
    data = json.load(f)
a = data['annotations'][0]
print('Keys:', list(a.keys()))
print('bbox  (x,y,w,h):', a['bbox'])
print('Has segmentation polygon:', len(a['segmentation']) > 0)
print()
print('Done. Dataset exploration complete.')
