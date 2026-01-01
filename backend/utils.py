import cv2
import numpy as np

def preprocess_plate(plate_img):
    """
    Preprocess the license plate image for better OCR accuracy.
    """
    if plate_img is None or plate_img.size == 0:
        return None

    # Convert to grayscale
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

    # Resize for OCR accuracy (2x)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Contrast enhancement using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Denoise while keeping edges
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Light thresholding (Otsu's binarization)
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    
    return thresh
