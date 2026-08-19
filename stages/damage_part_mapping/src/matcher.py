from src.bbox_utils import get_center, is_point_in_box, calculate_iou

def match_damages_to_parts(damages, parts, min_iou_threshold=0.3):
    """
    Matches a list of damage detections to vehicle part detections.
    
    A strict matching is applied:
    - The damage center must be inside the part bounding box OR 
    - The IoU must be above a significant threshold (e.g., >= 0.3).
    - If no part meets the criteria, the mapped part is 'uncertain'.
    - If multiple parts meet the criteria with very close scores, it is also 'uncertain'.
    """
    results = []
    
    for d in damages:
        dcx, dcy = get_center(d['bbox'])
        
        candidates = []
        for p in parts:
            in_box = is_point_in_box(dcx, dcy, p['bbox'])
            iou = calculate_iou(d['bbox'], p['bbox'])
            
            # Score formula
            center_score = 1.0 if in_box else 0.0
            score = 0.6 * center_score + 0.4 * iou
            
            # To be a valid candidate, it must either contain the center OR have decent overlap
            if in_box or iou >= min_iou_threshold:
                candidates.append({
                    "part": p,
                    "score": score,
                    "iou": iou
                })
        
        # Sort candidates by score descending
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        if not candidates:
            damage_name = d['damage']
            if d['confidence'] < 0.5:
                damage_name = f"maybe {damage_name}"
                
            # If damage doesn't map to a specific part, default to "body" for pricing estimation later
            results.append({
                "damage": damage_name,
                "damage_confidence": d['confidence'],
                "damage_bbox": d['bbox'],
                "damaged_part": "body",
                "part_confidence": None,
                "part_bbox": None,
                "mapping_score": 0.0
            })
            continue
            
        # User instruction: "remove this uncertainity handling ... we need to know the exact parts"
        # Always pick the top-scoring candidate, even if ambiguous.
        best = candidates[0]
        final_part = best['part']['part']
        final_part_conf = best['part']['confidence']
        final_part_bbox = best['part']['bbox']
        final_score = best['score']
        
        damage_name = d['damage']
        if d['confidence'] < 0.5:
            damage_name = f"maybe {damage_name}"
                
        results.append({
            "damage": damage_name,
            "damage_confidence": d['confidence'],
            "damage_bbox": d['bbox'],
            "damaged_part": final_part,
            "part_confidence": final_part_conf,
            "part_bbox": final_part_bbox,
            "mapping_score": round(final_score, 3)
        })
        
    return results
