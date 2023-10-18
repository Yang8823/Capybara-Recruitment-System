import pytesseract
from PIL import Image
import cv2
import numpy as np

def process_cv_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Preprocess the image: convert to grayscale, apply adaptive thresholding
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 10)

    # Perform OCR using Tesseract
    custom_config = r'--oem 3 --psm 6'
    extracted_text = pytesseract.image_to_string(Image.fromarray(binary), config=custom_config)

    # Further data extraction and analysis can be done here

    return extracted_text

cv_image_path = r'Image/CV_Image2.jpg'
cv_text = process_cv_image(cv_image_path)
print(cv_text)

specific_text = "John Meehan"
if specific_text in cv_text:
    print(f"Found: {specific_text}")
else:
    print(f"Not found: {specific_text}")