
from PIL import Image
import pytesseract
import enum

class OS(enum.Enum):                                                            #setup for Mac or Windows
    Mac = 0
    Windows = 1

class Languages(enum.Enum):                                                     #to add languages
    ENG = 'eng'
    RUS = 'rus'
    ITA = 'ita'

class ImageReader:                                                              #setup for tesseract
    def __init__(self, os: OS):
        if os == OS.Windows:                                                    #if mac need to add elif
            windows_path = r'C:/Program Files/Tesseract-OCR/tesseract.exe'      
            pytesseract.tesseract_cmd = windows_path
            print('Running on Windows')

    def extract_text(self, image: str, lang: str) -> str:                       #extract the image into string and the ouput will also be string
        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img, lang=lang)
        return extracted_text

if __name__ == '__main__':
    ir = ImageReader(OS.Windows)
    text = ir.extract_text('Image/CV_ResumeExample.jpg', lang='eng')
    print(text)

