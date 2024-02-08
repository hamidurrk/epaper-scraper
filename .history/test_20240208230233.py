from PIL import Image    
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

def separate_first_line(text):
    # Split the text at the first newline character
    lines = text.split('\n', 1)
    
    # Check if the text has multiple lines
    if len(lines) > 1:
        first_line = lines[0]
        remaining_text = lines[1]
        return first_line, remaining_text
    else:
        return text, ""

img_location = 'C:/Users/hamid/OneDrive/Documents/epaper-scraper/downloaded_articles/jugantor/2020/07/27/page_10/article_12.jpg'

output = pytesseract.pytesseract.image_to_string(Image.open(img_location), lang='ben')
num_words = len(output.split())
# print(output)
print (num_words)

first_line, remaining_text = separate_first_line(output)
print("First line:", first_line)
print("Remaining text:")
print(remaining_text)