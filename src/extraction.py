import os
from PIL import Image
import pytesseract
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

def extract_article(img_location):
    raw_output = pytesseract.pytesseract.image_to_string(Image.open(img_location), lang='ben')

    if len(raw_output) > 1:
        num_words = len(raw_output.split())

        article_title, article = separate_article_title(raw_output)
        print("Article Title: ", article_title)
        print("Article:")
        print(article)
        print ("Number of Words: ", num_words)
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
            print(f"jugantor/{year}/{month}/{day}/page_{i}/article_{j}.jpg")
            try: 
                article_title, article, num_words, raw_output = extract_article(img_location)
                # insert_to_jugantor(year, f"{year}-{month}-{day}", article_title, article, num_words, i, f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php")
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
        no_exception_found = 1
        if date_str not in scraped_dates:
            gen_prompt(f"Attempting New Scrape | Year: {year}, Month: {month}, Day: {day}", value=100)
            try: 
                # scrape_old_jugantor(year, month, day) 
                count += 1
            except Exception as e:
                no_exception_found = 0
                print("Scraping error: ", e)
                print(f"Error on: Year: {year}, Month: {month}, Day: {day}")  
                if check_internet_connection():
                    print("Internet connection is available.")
                else:
                    print("No internet connection.") 
                    break
                print("Page Unavailable: Redirecting...")
                # time.sleep(2)
                pass
            if no_exception_found:
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
        print(f"\nScraping finished from {start_date} to {end_date}")
    else: 
        print(f"\nScraping finished from {start_date} to {date_str}")
  