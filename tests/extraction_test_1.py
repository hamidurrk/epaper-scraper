import tesserocr
from tesserocr import PyTessBaseAPI
from PIL import Image

# PyTessBaseAPI(path='C:\\Program Files (x86)\\Tesseract-OCR\\tessdata')
# print(tesserocr.tesseract_version())  # print tesseract-ocr version
# print(tesserocr.get_languages())  # prints tessdata path and list of available languages

image = Image.open('C:/Users/hamid/OneDrive/Documents/epaper-scraper/downloaded_articles/jugantor/2024/01/01/page_1/article_10.jpg')
# print(tesserocr.image_to_text(image))  # print ocr text from image
# or
# print(tesserocr.file_to_text('/article_10.jpg'))

with PyTessBaseAPI(path='C:\\Program Files (x86)\\Tesseract-OCR\\tessdata',lang='ben') as api:
    api.SetImage(image)
    ocr = api.GetUTF8Text()
    # confidence = api.AllWordConfidences()
    print(ocr)
    num_words = len(ocr.split())
    print(num_words)