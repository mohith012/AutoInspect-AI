# Stage 3: Damage to Vehicle-Part Mapping

## 1. Purpose
This module integrates Model 1 (Damage Detection) and Model 2 (Vehicle Part Detection) into a unified pipeline. The objective is to establish exactly *which* vehicle part contains the identified damage, mapping bounding boxes geometrically to output semantic labels (e.g., "front_bumper -> dent").

## 2. Models
- **Model 1:** YOLOv8n fine-tuned on CarDD. Detects 6 classes of damage (dent, scratch, crack, glass_shatter, lamp_broken, tire_flat).
- **Model 2:** YOLOv8n fine-tuned on Carparts-Seg. Detects 22 vehicle parts (bumpers, doors, glass, lights, hood, mirrors, etc.).

*Note: Neither model was modified or retrained during this stage.*

## 3. Integration Architecture
The pipeline is structured as follows:
1. `pipeline.py` accepts an image path.
2. `damage_detector.py` invokes Model 1 and standardizes bounding boxes to `[x1, y1, x2, y2]`.
3. `part_detector.py` invokes Model 2, standardizes boxes, and applies class mapping (e.g. `wheel` -> `tire`).
4. `matcher.py` consumes both lists of detections and performs geometric matching.

## 4. Matching Algorithm & IoU
For each damage bounding box, the algorithm checks against every vehicle part box using two primary signals:
1. **Center-in-Box:** Calculates the mathematical center `(cx, cy)` of the damage box. If this point lies strictly within a part box, `center_score = 1.0`.
2. **IoU:** Calculates the Intersection over Union between the damage box and the part box.

**Mapping Score:** `0.6 * center_score + 0.4 * IoU`

## 5. Confidence Thresholds & Uncertainty
To prevent hallucinations (as mandated), the system is strict:
- The damage must either have its center inside a part, or have an IoU `>= 0.3`.
- If no part meets this criterion, the `damaged_part` is labeled `"uncertain"`.
- If multiple parts overlap heavily with the damage and their resulting scores are within `0.1` of each other, the system refuses to guess and also labels the match `"uncertain"`.

## 6. Test Dataset & Performance
The pipeline was evaluated on the first 30 unseen images of the CarDD test dataset (`test2017/`).

**Results:**
- **Images tested:** 30
- **Total damages detected:** 56
- **Successfully mapped:** 21
- **Uncertain mappings:** 35
- **Mapping rate:** 37.5%
- **Average Pipeline Time:** ~321ms per image (Model 1 + Model 2 + Matching)

## 7. Known Limitations & Failure Cases
The mapping rate of 37.5% highlights critical dataset limitations discovered in Stage 2:
1. **Missing Classes:** Model 2 does not know what a `fender` or `grille` is. When Model 1 detects a dent on a fender, Model 2 provides no bounding box for it. Due to our strict "no-fabrication" thresholds, the system correctly falls back to `"uncertain"`.
2. **Partially Visible Parts:** Model 2 sometimes draws tight bounding boxes around partially occluded parts, missing the outer edges where damage often occurs.
3. **Ambiguity:** Scratches that span across a door and a fender are correctly flagged as `"uncertain"` due to the multi-part overlap threshold.

## 8. Inference Time
- **Total Pipeline Execution:** ~320ms on RTX 2050.
- Fast enough for near real-time web deployment.

## 9. Example Prediction
```json
{
  "damage": "dent",
  "damage_confidence": 0.96,
  "damage_bbox": [249.6, 149.4, 676.8, 564.1],
  "damaged_part": "uncertain",
  "part_confidence": null,
  "part_bbox": null,
  "mapping_score": 0.104
}
```
*(Example of a fender dent correctly falling back to uncertain due to missing fender class).*
