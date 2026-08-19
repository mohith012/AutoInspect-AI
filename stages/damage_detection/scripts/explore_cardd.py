import json

path = r'C:\Users\sango\OneDrive\Desktop\Car project\CarDD_release\CarDD_release\CarDD_COCO\annotations\instances_train2017.json'
with open(path) as f:
    data = json.load(f)

print('=== CATEGORIES (Classes) ===')
for cat in data['categories']:
    print(cat)

imgs = data['images']
anns = data['annotations']
print()
print('=== DATASET STATS ===')
print('Total images     :', len(imgs))
print('Total annotations:', len(anns))

print()
print('=== SAMPLE IMAGE ===')
print(imgs[0])

print()
print('=== SAMPLE ANNOTATION ===')
print(anns[0])

print()
print('=== ANNOTATION KEYS ===')
print(list(anns[0].keys()))
