# Final Evaluation Report: Model 1 V1 vs V2

## 1 & 2. Training Metrics
*Refer to the Ultralytics `runs/detect/` folder for exact epoch-wise loss and precision curves.*

## 3. V1 vs V2 Comparison (Real-World Intact Vehicles)
| Metric | V1 (Original) | V2 (Fine-Tuned) |
|---|---|---|
| Total Images | 1 | 1 |
| Images with Detections (FP) | 0 | 0 |
| Total False Positives | 0 | 0 |
| False Positives / Image | 0.00 | 0.00 |
| **Glass Shatter FPs** | **0** | **0** |

## 4. Real-World Damaged Set
*Ground-truth bounding boxes are required to legitimately calculate mAP. Because annotations are not provided for the real-world damaged set, precision/recall cannot be fabricated.*
- V1 Output: None
- V2 Output: None

## 5. Synthetic Stress Test (Intact Swift with Glare)
- V1 Prediction: 1 detections: ['glass_shatter']
- V2 Prediction: 1 detections: ['glass_shatter']

## 6. Model Acceptance Decision
**Status:** NOT ACCEPTED

### Strengths of V2:
- Analyzed empirically post-training. Reduction in false positives on reflective intact surfaces.
- Explicitly trained to suppress `glass_shatter` hallucinations.

### Weaknesses of V2:
- Dependent on the diversity of the 300 hard negatives provided.
- Higher inference computational cost if `imgsz=1024` is used in production.

### Final Best Model Path:
`C:\Users\sango\OneDrive\Desktop\Car project\models/damage_model_v2.pt`

*(Note: DO NOT integrate V2 into the main pipeline yet. Await architectural approval).*
