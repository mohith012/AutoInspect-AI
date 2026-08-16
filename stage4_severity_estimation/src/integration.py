from PIL import Image

def integrate_severity_into_pipeline(full_image_path, pipeline_results, severity_predictor, padding_ratio=0.15):
    """
    Integrates severity estimation into the existing Stage 3 pipeline results.
    
    Args:
        full_image_path (str): Path to the original full image.
        pipeline_results (list): List of dictionaries containing the mapping results from Stage 3.
                                 e.g., [{"damaged_part": "front_bumper", "damage_type": "dent", "damage_bbox": [x1, y1, x2, y2], ...}]
        severity_predictor (SeverityPredictor): Initialized severity predictor.
        padding_ratio (float): Contextual padding to add around the damage bounding box.
        
    Returns:
        list: Updated pipeline results including severity.
    """
    img = Image.open(full_image_path).convert('RGB')
    img_width, img_height = img.size
    
    integrated_results = []
    
    for result in pipeline_results:
        # Check if we have the damage bounding box from Model 1
        if "damage_bbox" not in result:
            result["severity"] = "unknown"
            result["severity_confidence"] = 0.0
            integrated_results.append(result)
            continue
            
        x1, y1, x2, y2 = result["damage_bbox"]
        
        # Calculate padding
        width = x2 - x1
        height = y2 - y1
        pad_w = int(width * padding_ratio)
        pad_h = int(height * padding_ratio)
        
        # Apply padding and ensure it stays within image boundaries
        crop_x1 = max(0, x1 - pad_w)
        crop_y1 = max(0, y1 - pad_h)
        crop_x2 = min(img_width, x2 + pad_w)
        crop_y2 = min(img_height, y2 + pad_h)
        
        # Crop the damaged region
        damage_crop = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
        
        # Predict severity
        severity_result = severity_predictor.predict_severity(damage_crop)
        
        # Update result dictionary
        result["severity"] = severity_result["severity"]
        result["severity_confidence"] = severity_result["confidence"]
        
        # Optional: Add probabilities for further analysis
        # result["severity_probabilities"] = severity_result["probabilities"]
        
        integrated_results.append(result)
        
    return integrated_results
