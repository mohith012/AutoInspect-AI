import time
from pathlib import Path
from src.damage_detector import detect_damages
from src.part_detector import detect_parts
from src.matcher import match_damages_to_parts

def analyze_vehicle_damage(image_path: str, damage_conf=0.25, part_conf=0.25, min_iou=0.3):
    """
    Complete Stage 3 pipeline for mapping vehicle damages to vehicle parts.
    
    1. Runs Model 1 (Damages)
    2. Runs Model 2 (Parts)
    3. Maps damages to parts geometrically
    4. Measures inference time
    """
    t0 = time.time()
    
    # 1. Run Damage Detection
    t1 = time.time()
    damages = detect_damages(image_path, conf_threshold=damage_conf)
    t2 = time.time()
    
    # 2. Run Part Detection
    parts = detect_parts(image_path, conf_threshold=part_conf)
    t3 = time.time()
    
    # 3. Match
    mapped_damages = match_damages_to_parts(damages, parts, min_iou_threshold=min_iou)
    t4 = time.time()
    
    # Performance metrics
    perf = {
        "model1_time_ms": round((t2 - t1) * 1000, 1),
        "model2_time_ms": round((t3 - t2) * 1000, 1),
        "mapping_time_ms": round((t4 - t3) * 1000, 1),
        "total_time_ms": round((t4 - t0) * 1000, 1)
    }
    
    return {
        "damages": mapped_damages,
        "raw_damages_count": len(damages),
        "performance": perf
    }

if __name__ == "__main__":
    import sys
    import json
    if len(sys.argv) < 2:
        print("Usage: python src/pipeline.py <img_path>")
        sys.exit(1)
        
    result = analyze_vehicle_damage(sys.argv[1])
    print(json.dumps(result, indent=2))
