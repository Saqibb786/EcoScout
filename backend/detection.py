import cv2
import easyocr
import numpy as np
from ultralytics import YOLO
from utils import preprocess_plate
import os

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False) # Set gpu=True if CUDA is available

# Load YOLO model
# Assuming best.pt is in the root directory of the project, relative to where main.py is run
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best.pt')

print(f"Loading model from: {MODEL_PATH}")
model = YOLO(MODEL_PATH)

def run_inference(image_input, output_path=None):
    """
    Run YOLO detection and EasyOCR on the input image.
    Args:
        image_input: Path to image (str) or image array (numpy.ndarray)
        output_path: Path to save annotated image (optional)
    Returns:
        List of detection records
    """
    if isinstance(image_input, str):
        img = cv2.imread(image_input)
    else:
        img = image_input.copy()
        
    results = model(img)
    
    detection_records = []
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Get bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            conf = float(box.conf[0].cpu().numpy())
            cls = int(box.cls[0].cpu().numpy())
            label = model.names[cls]
            
            record = {
                "violation_type": label,
                "confidence": round(conf * 100, 2),
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "license_plate": "N/A",
                "ocr_confidence": 0.0
            }
            
            # Draw bounding box
            color = (0, 255, 0) # Green
            if label.lower() in ['littering', 'smoke']: # Highlight violations
                color = (0, 0, 255) # Red
            
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, f"{label} {conf:.2f}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # OCR Processing
            # We attempt OCR on the cropped region if it's a vehicle or if we suspect a plate
            # For robustness, we'll try on all detections but filter by confidence
            
            crop = img[y1:y2, x1:x2]
            if crop.size > 0:
                processed_crop = preprocess_plate(crop)
                if processed_crop is not None:
                    ocr_result = reader.readtext(processed_crop, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                    
                    if ocr_result:
                        # Sort results by x-coordinate (left to right)
                        ocr_result.sort(key=lambda x: x[0][0][0])
                        
                        # Concatenate all detected text segments
                        full_text = " ".join([res[1] for res in ocr_result])
                        
                        # Calculate average confidence
                        avg_conf = sum([res[2] for res in ocr_result]) / len(ocr_result)
                        
                        # Stricter threshold for OCR
                        if avg_conf > 0.4 and len(full_text) > 3: 
                            record["license_plate"] = full_text
                            record["ocr_confidence"] = round(avg_conf * 100, 2)
                            
                            # Draw plate text
                            cv2.putText(img, f"Plate: {full_text}", (x1, y2 + 20), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            detection_records.append(record)

    # Save annotated image if output_path is provided
    if output_path:
        cv2.imwrite(output_path, img)
    
    return detection_records
