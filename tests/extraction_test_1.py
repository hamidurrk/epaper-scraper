from tesserocr import PyTessBaseAPI
from PIL import Image
import time
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
# PyTessBaseAPI(path='C:\\Program Files (x86)\\Tesseract-OCR\\tessdata')
# print(tesserocr.tesseract_version())  # print tesseract-ocr version
# print(tesserocr.get_languages())  # prints tessdata path and list of available languages
start_time = time.time()
# image = Image.open('C:/Users/hamid/OneDrive/Documents/epaper-scraper/tests/processed_image.jpg')


# with PyTessBaseAPI(path='C:\\Program Files (x86)\\Tesseract-OCR\\tessdata',lang='ben') as api:
#     api.SetImage(image)
#     ocr = api.GetUTF8Text()
#     # confidence = api.AllWordConfidences()
#     print(ocr)
#     num_words = len(ocr.split())
#     print(num_words)

def separate_article_title(text):
    lines = text.split('\n', 1)
    if len(lines) > 1:
        first_line = lines[0]
        remaining_text = text
        return first_line, remaining_text
    else:
        return text, ""
    
def extract_article(img_location):
    raw_output = pytesseract.pytesseract.image_to_string(Image.open(img_location), lang='ben')

    if len(raw_output) > 1:
        num_words = len(raw_output.split())
        
        # print("Article Title: ", article_title)
        # print("Article:")
        # print(article)
        print ("Number of Words: ", num_words)
    else:
        print("Could not find recognizable characters.")
        return None

extract_article('C:/Users/hamid/OneDrive/Documents/epaper-scraper/tests/processed_image.jpg')

end_time = time.time()
execution_time = end_time - start_time

# Print the execution time
print(f"Execution time: {execution_time} seconds")
