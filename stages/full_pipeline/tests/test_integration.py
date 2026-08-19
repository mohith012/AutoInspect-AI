import os
import glob
import json
import time
from tqdm import tqdm
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from stages.full_pipeline.core.pipeline import analyze_vehicle_damage
from stages.full_pipeline.core.visualization import draw_visualizations

def run_integration_tests(test_images_dir, num_images=30, output_dir="../results"):
    os.makedirs(output_dir, exist_ok=True)
    vis_dir = os.path.join(output_dir, "visualizations")
    os.makedirs(vis_dir, exist_ok=True)
    
    # Get test images
    image_paths = glob.glob(os.path.join(test_images_dir, "*.jpg"))
    if not image_paths:
        print(f"No images found in {test_images_dir}")
        return
        
    test_paths = image_paths[:num_images]
    print(f"Running full integration pipeline on {len(test_paths)} unseen images...")
    
    all_results = []
    
    for img_path in tqdm(test_paths, desc="Processing Images"):
        img_name = os.path.basename(img_path)
        
        try:
            # 1. Run pipeline
            # Note: save_crops is True by default in pipeline
            result = analyze_vehicle_damage(img_path, save_crops=True)
            all_results.append(result)
            
            # 2. Save Visualization
            out_vis = os.path.join(vis_dir, f"{os.path.splitext(img_name)[0]}_integrated.jpg")
            draw_visualizations(img_path, result, out_vis)
            
        except Exception as e:
            print(f"Failed to process {img_name}: {e}")
            all_results.append({
                "image": img_name,
                "error": str(e)
            })
            
    # Save the consolidated JSON report
    report_path = os.path.join(output_dir, "integration_test_report.json")
    with open(report_path, "w") as f:
        json.dump(all_results, f, indent=4)
        
    print(f"Integration test complete! Saved report to {report_path}")

if __name__ == "__main__":
    test_dir = r"C:\Users\sango\OneDrive\Desktop\Car project\CarDD_release\CarDD_release\CarDD_COCO\test2017"
    run_integration_tests(test_dir, num_images=30)
