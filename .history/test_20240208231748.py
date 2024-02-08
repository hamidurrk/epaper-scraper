from PIL import Image    
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

def separate_article_heading(text):
    lines = text.split('\n', 1)
    if len(lines) > 1:
        first_line = lines[0]
        remaining_text = lines[1]
        return first_line, remaining_text
    else:
        return text, ""

img_location = 'C:/Users/hamid/OneDrive/Documents/epaper-scraper/downloaded_articles/jugantor/2020/07/27/page_10/article_12.jpg'

output = pytesseract.pytesseract.image_to_string(Image.open(img_location), lang='ben')

if len(output) > 1:
    num_words = len(output.split())
    # print(output)
    print (num_words)

    article_heading, remaining_text = separate_article_heading(output)
    print("Article Heading:", article_heading)
    print("Remaining text:")
    print(remaining_text)
else:
    print("Could not find recognizable characters.")
    