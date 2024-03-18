import os
from PIL import Image
import pytesseract
import concurrent.futures
from datetime import date, timedelta
from tqdm import tqdm
from databbase import *
from utils import *

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def separate_article_title(text):
    lines = text.split('\n', 1)
    if len(lines) > 1:
        first_line = lines[0]
        remaining_text = text
        return first_line, remaining_text
    else:
        return text, ""

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
#         print("Could not find recognizable characters")
#         return None
        
# def process_image(img_location, year, month, day, i, j):
#     try:
#         conn = sqlite3.connect('jugantor.db')
#         c = conn.cursor()

#         extracted_obj = extract_article(img_location)
#         if extracted_obj is not None:
#             article_title, article, num_words, raw_output = extracted_obj
#             with conn:
#                 c.execute("INSERT INTO jugantor (year, date, article_title, article, wordcount, pagenum, url) VALUES (?, ?, ?, ?, ?, ?, ?)", 
#                           (year, f"{year}-{month}-{day}", f"{j}: {article_title}", article, num_words, i, f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php"))
#             print("Data inserted successfully")
#             return article_title, article, num_words, raw_output
#         else:
#             print("Data is a NoneType object")
#     except Exception as e:
#         print("Did not initiate data entry:", e)
#     finally:
#         conn.close()

# def extract_all_and_store(year, month, day):
#     gen_prompt(f"Started: jugantor/{year}/{month}/{day}")
#     num_pages = len(os.listdir(os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day)))
#     with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
#         futures = []
#         for i in range(1, num_pages + 1):
#             num_articles = len(os.listdir(os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day, f"page_{i}")))
#             for j in range(1, num_articles + 1):
#                 img_location = os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day, f"page_{i}", f"article_{j}.jpg")
#                 print(f"jugantor/{year}/{month}/{day}/page_{i}/article_{j}.jpg")
#                 futures.append(executor.submit(process_image, img_location, year, month, day, i, j))
#         for future in concurrent.futures.as_completed(futures):
#             result = future.result()
#             if result:
#                 # article_title, article, num_words, raw_output = result
#                 # print(f"{article_title}: {num_words} words")
#                 pass

def extract_article(img_location):
    raw_output = pytesseract.pytesseract.image_to_string(Image.open(img_location), lang='ben')

    if len(raw_output) > 1:
        num_words = len(raw_output.split())

        article_title, article = separate_article_title(raw_output)
        # print("Article Title: ", article_title)
        # print("Article:")
        # print(article)
        # print ("Number of Words: ", num_words)
        return article_title, article, num_words, raw_output
    else:
        print("Could not find recognizable characters.")
        return None
    
def extract_all_and_store(year, month, day):
    num_pages = len(os.listdir(os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day)))
    for i in range(1, num_pages + 1):
        num_articles = len(os.listdir(os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day, f"page_{i}")))
        for j in range(1, num_articles + 1):
            img_location = os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day, f"page_{i}", f"article_{j}.jpg")
            print(img_location)
            try: 
                article_title, article, num_words, raw_output = extract_article(img_location)
                insert_to_jugantor(year, f"{year}-{month}-{day}", f"{j}: {article_title}", article, num_words, i, f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php")
            except Exception as e:
                print("Did not initiate data entry:", e)
                pass
    print(f"Success: Article Extraction Completed! JUGANTOR-{year}/{month}/{day}")
    
def extract_all_range(start_year, start_month, start_day, end_year, end_month, end_day):
    file_path = os.path.join(BASE_DIR, "downloaded_articles", "extracted_dates.txt")
    start_year = int(start_year)
    start_month = int(start_month)
    start_day = int(start_day)

    end_year = int(end_year)
    end_month = int(end_month)
    end_day = int(end_day)

    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    total_iterations = (end_date - start_date).days + 1
    
    pbar = tqdm(total=total_iterations, desc="Progress", unit="paper",)
    current_date = start_date
    scraped_dates = load_scraped_dates(file_path)
    count = 0
    while current_date <= end_date:
        os.system('cls' if os.name == 'nt' else 'clear')
        pbar.update(1)
        sys.stdout.write("\n\n")
        year = str(current_date.year)
        month = str(current_date.month).zfill(2)
        day = str(current_date.day).zfill(2)
        date_str = f"{year}-{month}-{day}"
        if date_str not in scraped_dates:
            gen_prompt(f"Attempting New Extraction | Year: {year}, Month: {month}, Day: {day}", value=100)
            
            extract_all_and_store(year, month, day) 
            count += 1
        
            scraped_dates.add(date_str)
            save_scraped_dates({date_str}, file_path)
            current_date += timedelta(days=1)
            # time.sleep(0.1)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            pbar.update(1)
            print(f"{date_str} already scraped.")
            current_date += timedelta(days=1)
            # time.sleep(0.1)
    pbar.close()
    if count == total_iterations:
        print(f"\nExtraction finished from {start_date} to {end_date}")
    else: 
        print(f"\nExtraction finished from {start_date} to {date_str}")
  