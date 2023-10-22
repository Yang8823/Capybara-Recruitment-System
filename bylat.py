import pytesseract
from PIL import Image
import cv2
import numpy as np

# Initialize the image rating variable
image_rating = 0

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

    # Define the first specific text
    first_specific_text = "Employment History"
    
    print(extracted_text)
    # Check if the first specific text is found
    if first_specific_text in extracted_text:
        print(f"Title: {first_specific_text}")

        # Search for the second specific text only after the first specific text
        second_specific_text = "Software Developer"
        second_text_index = extracted_text.find(second_specific_text, extracted_text.find(first_specific_text) + len(first_specific_text))
        if second_text_index != -1:
            print(f"Found: {second_specific_text}")

            # Increase the image rating by 1
            global image_rating
            image_rating += 1
        else:
            print(f"Not found: {second_specific_text}")
    else:
        print(f"Not found: {first_specific_text}")

    # Further data extraction and analysis can be done here

    return extracted_text

cv_image_path = r'Image/CV_Image2.jpg'
cv_text = process_cv_image(cv_image_path)

# Display the image rating
print(f"Image Rating: {image_rating}")