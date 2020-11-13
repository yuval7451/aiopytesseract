
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract-OCR\tesseract.exe"

# Simple image to string
print(pytesseract.image_to_string(Image.open('test.png')))