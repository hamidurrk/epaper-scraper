# from autoocr import AutoOCR # import the AutoOCR class

# oa = AutoOCR(lang='bangla') # specify the language code

# oa.set_datapath('C:/Users/hamid/OneDrive/Documents/epaper-scraper/downloaded_articles/jugantor/2020/07/27/page_10')

# out_text = oa.get_text('image_ocr.jpg')

# print(out_text)

from PIL import Image    
import pytesseract

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

print (tess.image_to_string(Image.open('C:/Users/hamid/OneDrive/Documents/epaper-scraper/downloaded_articles/jugantor/2020/07/27/page_10/article_13.jpg'), lang='ben'))