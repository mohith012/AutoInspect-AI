import cv2
import numpy as np
from pathlib import Path

def draw_visualizations(image_path, mapped_damages, output_path):
    """
    Draws vehicle-part boxes (blue) and damage boxes (red) on the image.
    Labels are grouped to indicate mapping (e.g. 'front_bumper -> dent').
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Cannot load image {image_path}")
        
    # Blue for parts, Red for damages, Orange for uncertain
    COLOR_PART = (255, 144, 30)   # Blueish (BGR)
    COLOR_DAMAGE = (30, 30, 255)  # Red
    COLOR_UNCERTAIN = (0, 165, 255) # Orange
    
    overlay = img.copy()
    
    for d in mapped_damages:
        # Draw damage box
        dx1, dy1, dx2, dy2 = map(int, d['damage_bbox'])
        cv2.rectangle(img, (dx1, dy1), (dx2, dy2), COLOR_DAMAGE, 2)
        
        part_name = d['damaged_part']
        is_uncertain = (part_name == 'uncertain')
        
        # Draw part box if available
        if not is_uncertain and d.get('part_bbox'):
            px1, py1, px2, py2 = map(int, d['part_bbox'])
            cv2.rectangle(overlay, (px1, py1), (px2, py2), COLOR_PART, 2)
            
        # Draw label near damage box
        label = f"{part_name.upper()} -> {d['damage'].upper()}"
        conf = f"(M:{d['mapping_score']:.2f})"
        
        bg_color = COLOR_UNCERTAIN if is_uncertain else COLOR_DAMAGE
        
        cv2.rectangle(img, (dx1, max(dy1-25, 0)), (dx1+len(label)*9+50, max(dy1-25, 0)+25), bg_color, -1)
        cv2.putText(img, f"{label} {conf}", (dx1+5, max(dy1-7, 18)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        
    # Blend overlay for part boxes
    result = cv2.addWeighted(overlay, 0.4, img, 0.6, 0)
    
    cv2.imwrite(str(output_path), result)
    return output_path
