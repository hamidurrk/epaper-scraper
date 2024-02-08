from PIL import Image    
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

img_location = 'C:/Users/hamid/OneDrive/Documents/epaper-scraper/downloaded_articles/jugantor/2020/07/27/page_10/article_12.jpg'

output = pytesseract.pytesseract.image_to_string(Image.open(img_location), lang='ben')
num_words = len(output.split())
print(output)
print (num_words)