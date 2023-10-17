import pytesseract
from PIL import Image
import cv2
import numpy as np

def process_cv_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Preprocess the image (grayscale, filtering, binarization)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Perform OCR using Tesseract
    extracted_text = pytesseract.image_to_string(Image.fromarray(binary))

    # Further data extraction and analysis can be done here
    # e.g., parsing contact information, work experience, education, etc.

    return extracted_text

# Example usage with your CV image path:
cv_image_path = r'Image/CV_Image2.jpg'
cv_text = process_cv_image(cv_image_path)
print(cv_text)