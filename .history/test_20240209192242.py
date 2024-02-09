from PIL import Image    
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

def separate_article_title(text):
    lines = text.split('\n', 1)
    if len(lines) > 1:
        first_line = lines[0]
        remaining_text = lines[1]
        return first_line, remaining_text
    else:
        return text, ""

def extract_article(img_location):
    raw_output = pytesseract.pytesseract.image_to_string(Image.open(img_location), lang='ben')

    if len(raw_output) > 1:
        num_words = len(raw_output.split())
        # print(raw_output)

        article_title, article = separate_article_title(raw_output)
        print("Article Title: ", article_title)
        print("Article:")
        print(article)
        print ("Number of Words: ", num_words)
        return article_title, article, num_words, raw_output
    else:
        print("Could not find recognizable characters.")
        return None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))        
print(BASE_DIR)

year, month, day = "2020", "07", "27"

num_pages = os.listdir(os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day))

print(num_pages)

# for i in range(1, num_pages):
#     for j in range(1, num_articles):
#         os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day, page, article)


img_location = 'C:/Users/hamid/OneDrive/Documents/epaper-scraper/downloaded_articles/jugantor/2020/07/27/page_10/article_12.jpg'
