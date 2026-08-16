import cv2
import numpy as np
import os
from pathlib import Path

def draw_visualizations(image_path, pipeline_result, output_path):
    """
    Draws vehicle-part boxes (blue) and damage boxes (red) on the image.
    Labels include Part, Damage, and Severity.
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Cannot load image {image_path}")
        
    COLOR_PART = (255, 144, 30)   # Blueish (BGR)
    COLOR_DAMAGE = (30, 30, 255)  # Red
    COLOR_UNCERTAIN = (0, 165, 255) # Orange
    
    overlay = img.copy()
    
    damages = pipeline_result.get("damages", [])
    
    for d in damages:
        # Check if we have valid bbox
        if not d.get('damage_bbox'):
            continue
            
        # Draw damage box
        dx1, dy1, dx2, dy2 = map(int, d['damage_bbox'])
        cv2.rectangle(img, (dx1, dy1), (dx2, dy2), COLOR_DAMAGE, 2)
        
        part_name = d.get('damaged_part', 'uncertain')
        is_uncertain = (part_name == 'uncertain' or part_name == 'body')
        
        # Draw part box if available
        if not is_uncertain and d.get('part_bbox'):
            px1, py1, px2, py2 = map(int, d['part_bbox'])
            cv2.rectangle(overlay, (px1, py1), (px2, py2), COLOR_PART, 2)
            
        # Construct label text
        damage_type = d.get('damage_type', 'unknown').upper()
        severity = d.get('severity', 'unknown').upper()
        recommendation = d.get('recommendation', 'INSPECT').upper()
        
        label1 = f"{part_name.upper()} -> {damage_type}"
        label2 = f"SEV: {severity} ({d.get('severity_confidence', 0):.2f})"
        label3 = f"REC: {recommendation}"
        
        bg_color = COLOR_UNCERTAIN if is_uncertain else COLOR_DAMAGE
        
        # Draw background rect
        max_len = max(len(label1), len(label2), len(label3))
        cv2.rectangle(img, (dx1, max(dy1-55, 0)), (dx1+max_len*9+10, max(dy1-55, 0)+55), bg_color, -1)
        
        # Draw texts
        cv2.putText(img, label1, (dx1+5, max(dy1-37, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img, label2, (dx1+5, max(dy1-22, 30)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img, label3, (dx1+5, max(dy1-7, 45)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        
    # Blend overlay for part boxes
    result = cv2.addWeighted(overlay, 0.4, img, 0.6, 0)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(str(output_path), result)
    return output_path

if __name__ == "__main__":
    pass
