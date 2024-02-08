from autoocr import AutoOCR # import the AutoOCR class

oa = AutoOCR(lang='bangla') # specify the language code

oa.set_datapath('C:/Users/hamid/OneDrive/Documents/epaper-scraper/downloaded_articles/jugantor/2020/07/27/page_10')

out_text = oa.get_text('image_ocr.jpg')

print(out_text)