# Stage 2: Vehicle Part Detection

## 1. Project Purpose
This module is **Stage 2** of the **AutoInspect AI** system. The goal of this stage is to detect and localize specific vehicle parts (e.g., bumpers, doors, hoods, tires) in images. 
Eventually, this model (Model 2) will be integrated with the damage detection model (Model 1) using spatial overlap (IoU) to determine exactly *which* vehicle part is damaged.

## 2. Dataset Source
**Ultralytics Carparts-Seg**
- Originally hosted on Roboflow Universe (by NCAI / Gianmarco Russo).
- Curated and formatted by Ultralytics.
- **URL:** [Ultralytics Carparts-Seg Dataset](https://docs.ultralytics.com/datasets/segment/carparts-seg/)

## 3. Dataset License
**AGPL-3.0 License**
- Free for research and open-source use.
- *Note:* Commercial deployment requires either open-sourcing the entire application or acquiring a commercial license from Ultralytics.

## 4. Dataset Classes
The dataset contains 23 raw classes (22 vehicle parts + 1 catch-all):
0: `back_bumper`, 1: `back_door`, 2: `back_glass`, 3: `back_left_door`, 4: `back_left_light`, 5: `back_light`, 6: `back_right_door`, 7: `back_right_light`, 8: `front_bumper`, 9: `front_door`, 10: `front_glass`, 11: `front_left_door`, 12: `front_left_light`, 13: `front_light`, 14: `front_right_door`, 15: `front_right_light`, 16: `hood`, 17: `left_mirror`, 18: `object` (excluded), 19: `right_mirror`, 20: `tailgate`, 21: `trunk`, 22: `wheel`

## 5. Class Mapping
To align with AutoInspect AI's project-level terminology, the dataset classes are mapped as follows (defined in `configs/class_mapping.yaml`):

- **Bumpers:** `front_bumper` → `front_bumper`, `back_bumper` → `rear_bumper`
- **Doors:** All positional doors (`front_door`, `back_left_door`, etc.) → `door`
- **Glass:** `front_glass` → `windshield`, `back_glass` → `rear_windshield`
- **Lights:** Front lights → `headlight`, Back lights → `taillight`
- **Mirrors:** `left_mirror`, `right_mirror` → `side_mirror`
- **Others:** `hood` → `hood`, `tailgate` → `tailgate`, `trunk` → `trunk`, `wheel` → `tire`
- **Excluded:** `object`

## 6. Dataset Statistics
- **Total Images:** 3,833
- **Split:** Train: 3,156 | Val: 401 | Test: 276
- **Annotation Format:** Instance segmentation polygons (converted to bounding boxes during inference).
- **Total Annotations (Train):** 16,733

## 7. Model Architecture
- **Model:** YOLOv8n (Nano)
- **Reason:** Smallest, fastest, and most memory-efficient model in the YOLOv8 family. Easily runs on an RTX 2050 (4GB VRAM) and provides rapid inference times suitable for web deployment.

## 8. Training Configuration
- **Weights:** Pretrained `yolov8n.pt` (fine-tuning)
- **Epochs:** 50
- **Image Size:** 640x640
- **Batch Size:** 16
- **Optimizer:** SGD (lr0=0.01)
- **Hardware:** NVIDIA GeForce RTX 2050 (4GB)

## 9. Evaluation Metrics
The model was evaluated on the validation set at Epoch 33 (best model):
- **mAP50:** 0.681
- **mAP50-95:** 0.537
- **Precision:** ~0.563
- **Recall:** ~0.729
- **Strongest Classes:** `front_bumper` (0.972), `front_glass` (0.981), `hood` (0.972)
- **Weakest Classes:** `wheel` (0.441), `back_right_door` (0.475)

## 10. Test Results
The model was visually tested on unseen real-world images from the CarDD test set. It successfully identified multiple parts simultaneously, correctly classifying tires, bumpers, windshields, hoods, headlights, and doors with high confidence.

## 11. Known Limitations
1. **Missing Classes:** The `fender` and `grille` classes are entirely absent from the dataset and cannot be detected. Damage to these areas will either be unassigned or fall back to an adjacent part (like bumper or door).
2. **Close-ups:** The model may struggle to identify parts in extreme close-up shots (e.g., macro shots of a scratch) where surrounding structural context is lost.
3. **Class 'object':** This dataset class is poorly defined and noisy, so it is strictly ignored during inference.

## 12. Example Predictions
```json
[
  {
    "part": "windshield",
    "raw_class": "front_glass",
    "confidence": 0.921,
    "bbox": [205.0, 102.8, 603.5, 212.8]
  },
  {
    "part": "hood",
    "raw_class": "hood",
    "confidence": 0.842,
    "bbox": [177.7, 203.0, 626.0, 319.5]
  }
]
```

## 13. How to Run Inference
To run predictions and get structured outputs, use the `s2_predict.py` script:

```bash
# From the project root directory
python stages/vehicle_part_detection/scripts/s2_predict.py path/to/image.jpg
```

Or within Python:
```python
from stages.vehicle_part_detection.scripts.s2_predict import detect_vehicle_parts
parts = detect_vehicle_parts("path/to/image.jpg", conf_threshold=0.25)
```

## 14. How to Reproduce Training
1. Run `s2_explore.py` (optional) to view dataset structure.
2. Ensure the dataset is downloaded to `data/` and `data.yaml` is configured correctly.
3. Execute the training script:
```bash
python stages/vehicle_part_detection/scripts/s2_train.py
```
This will output the trained weights to `models/vehicle_parts_v1/weights/best.pt`.
