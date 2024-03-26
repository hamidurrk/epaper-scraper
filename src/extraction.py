import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import concurrent.futures
from datetime import date, timedelta
from tqdm import tqdm
import time
from databbase import *
from utils import *

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'jugantor.db')

def preprocess_image(img):
    current_dpi = img.info.get('dpi', (72, 72))  # Default DPI is 72
    scale_factor = 400 / current_dpi[0]
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)
    img = img.resize((new_width, new_height), resample=Image.LANCZOS)
    img = img.filter(ImageFilter.MedianFilter(size=3))  # Noise reduction
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(6)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.2)
    img = img.point(lambda p: p > 170 and 255)
    return img

def separate_article_title(text):
    lines = text.split('\n', 1)
    if len(lines) > 1:
        first_line = lines[0]
        return first_line, text
    else:
        return "", ""

def extract_article(img_path):
    img = Image.open(img_path)
    img = preprocess_image(img)
    raw_output = pytesseract.image_to_string(img, lang='ben')
    return separate_article_title(raw_output)

def batch_insert_articles(articles):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        with conn:
            c.executemany("INSERT INTO jugantor (year, date, article_title, article, wordcount, pagenum, url) VALUES (?, ?, ?, ?, ?, ?, ?)", articles)
        print("Batch insertion successful")
    except Exception as e:
        print("Error during batch insertion:", e)
    finally:
        conn.close()

def process_image(img_location, year, month, day):
    article_title, article = extract_article(img_location)
    if article_title:
        return (year, f"{year}-{month}-{day}", article_title, article, len(article.split()), f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php")

def extract_all_and_store(year, month, day):
    gen_prompt(f"Started: jugantor/{year}/{month}/{day}")
    num_pages = len(os.listdir(os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day)))
    articles = []
    articles_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(1, num_pages + 1):
            num_articles = len(os.listdir(os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day, f"page_{i}")))
            for j in range(1, num_articles + 1):
                img_location = os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day, f"page_{i}", f"article_{j}.jpg")
                # print(f"jugantor/{year}/{month}/{day}/page_{i}/article_{j}.jpg")
                articles.append((executor.submit(process_image, img_location, year, month, day), (year, month, day)))
        print(articles)
        for future, date_info in tqdm(articles, desc=f"Processing images for {year}-{month}-{day}"):
            result = future.result()
            if result:
                articles_data.append(result)
        print(articles_data)
        # batch_insert_articles(articles_data)

# def extract_article(img_location):
#     raw_output = pytesseract.pytesseract.image_to_string(Image.open(img_location), lang='ben')

#     if len(raw_output) > 1:
#         num_words = len(raw_output.split())

#         article_title, article = separate_article_title(raw_output)
#         # print("Article Title: ", article_title)
#         # print("Article:")
#         # print(article)
#         # print ("Number of Words: ", num_words)
#         return article_title, article, num_words, raw_output
#     else:
#         print("Could not find recognizable characters.")
#         return None
    
# def extract_all_and_store(year, month, day):
#     num_pages = len(os.listdir(os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day)))
#     for i in range(1, num_pages + 1):
#         num_articles = len(os.listdir(os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day, f"page_{i}")))
#         for j in range(1, num_articles + 1):
#             img_location = os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day, f"page_{i}", f"article_{j}.jpg")
#             print(img_location)
#             try: 
#                 article_title, article, num_words, raw_output = extract_article(img_location)
#                 insert_to_jugantor(year, f"{year}-{month}-{day}", f"{j}: {article_title}", article, num_words, i, f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php")
#             except Exception as e:
#                 print("Did not initiate data entry:", e)
#                 pass
#     print(f"Success: Article Extraction Completed! JUGANTOR-{year}/{month}/{day}")
    
# def extract_all_range(start_year, start_month, start_day, end_year, end_month, end_day):
#     file_path = os.path.join(BASE_DIR, "downloaded_articles", "extracted_dates.txt")
#     start_year = int(start_year)
#     start_month = int(start_month)
#     start_day = int(start_day)

#     end_year = int(end_year)
#     end_month = int(end_month)
#     end_day = int(end_day)

#     start_date = date(start_year, start_month, start_day)
#     end_date = date(end_year, end_month, end_day)

#     total_iterations = (end_date - start_date).days + 1
    
#     pbar = tqdm(total=total_iterations, desc="Progress", unit="paper",)
#     current_date = start_date
#     scraped_dates = load_scraped_dates(file_path)
#     count = 0
#     while current_date <= end_date:
#         os.system('cls' if os.name == 'nt' else 'clear')
#         pbar.update(1)
#         sys.stdout.write("\n\n")
#         year = str(current_date.year)
#         month = str(current_date.month).zfill(2)
#         day = str(current_date.day).zfill(2)
#         date_str = f"{year}-{month}-{day}"
#         if date_str not in scraped_dates:
#             gen_prompt(f"Attempting New Extraction | Year: {year}, Month: {month}, Day: {day}", value=100)
            
#             extract_all_and_store(year, month, day) 
#             count += 1
        
#             scraped_dates.add(date_str)
#             save_scraped_dates({date_str}, file_path)
#             current_date += timedelta(days=1)
#             # time.sleep(0.1)
#         else:
#             os.system('cls' if os.name == 'nt' else 'clear')
#             pbar.update(1)
#             print(f"{date_str} already scraped.")
#             current_date += timedelta(days=1)
#             # time.sleep(0.1)
#     pbar.close()
#     if count == total_iterations:
#         print(f"\nExtraction finished from {start_date} to {end_date}")
#     else: 
#         print(f"\nExtraction finished from {start_date} to {date_str}")
  
start_time = time.time()
extract_all_and_store("2012", "01", "01")
end_time = time.time()
execution_time = end_time - start_time

# Print the execution time
print(f"Execution time: {execution_time} seconds")