import sys
import time
import json
from pathlib import Path
from src.pipeline import analyze_vehicle_damage
from src.visualization import draw_visualizations

def run_evaluation():
    test_dir = Path(r"C:\Users\sango\OneDrive\Desktop\Car project\CarDD_release\CarDD_release\CarDD_COCO\test2017")
    out_dir = Path(r"C:\Users\sango\OneDrive\Desktop\Car project\stages/damage_part_mapping\results")
    vis_dir = out_dir / "visualizations"
    fail_dir = out_dir / "failure_cases"
    
    # Process the first 30 images
    images = list(test_dir.glob("*.jpg"))[:30]
    
    total_damages = 0
    total_mapped = 0
    total_uncertain = 0
    total_time = 0
    
    results_list = []
    
    for idx, img_path in enumerate(images):
        print(f"Processing {idx+1}/30: {img_path.name}")
        
        t0 = time.time()
        res = analyze_vehicle_damage(str(img_path))
        t_ms = (time.time() - t0) * 1000
        total_time += t_ms
        
        raw_damages = res['raw_damages_count']
        damages = res['damages']
        
        total_damages += raw_damages
        
        if len(damages) > 0:
            out_img = vis_dir / img_path.name
            draw_visualizations(img_path, damages, out_img)
            
            for d in damages:
                total_mapped += 1
                
                results_list.append({
                    "image": img_path.name,
                    "damage": d['damage'],
                    "damaged_part": d['damaged_part'],
                    "mapping_score": d['mapping_score']
                })
                
    metrics = {
        "images_tested": len(images),
        "total_raw_damages_detected": total_damages,
        "successfully_mapped": total_mapped,
        "unmapped_filtered_out": total_damages - total_mapped,
        "mapping_rate": round(total_mapped / total_damages * 100, 1) if total_damages > 0 else 0,
        "avg_pipeline_time_ms": round(total_time / len(images), 1)
    }
    
    with open(out_dir / "metrics" / "eval_results.json", "w") as f:
        json.dump({"metrics": metrics, "details": results_list}, f, indent=2)
        
    print("\n--- Evaluation Complete ---")
    for k, v in metrics.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    run_evaluation()
