# 
# *************************************************************************************************************
# 
# Depricated code
# 
# Check src directory
# 
# 
# 
# 
# 
# 
# 
# 
# 
# **************************************************************************************************************
# 

from selenium import webdriver
import os
import requests
import time
import sys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import sqlite3
from PIL import Image    
import pytesseract
from datetime import date, timedelta
from tqdm import tqdm

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))       
conn = sqlite3.connect('jugantor.db')

firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument("--headless") 
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), service_args = ['--marionette-port', '2828', '--connect-existing'], options=firefox_options)

def create_table():
    c = conn.cursor()
    c.execute("""CREATE TABLE jugantor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER,
                date INTEGER,
                article_title TEXT,
                article TEXT,
                wordcount INTEGER,
                pagenum INTEGER,
                url TEXT
                )""")
    conn.close()

def insert_to_jugantor(year, date, article_title, article, wordcount, pagenum, url):
        c = conn.cursor()
        with conn:
            c.execute("INSERT INTO jugantor (year, date, article_title, article, wordcount, pagenum, url) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (year, date, article_title, article, wordcount, pagenum, url))
        print("Data inserted successfully")

def gen_prompt(message, value=70, char="-"):
    wrt = " " + message + " "
    sys.stdout.write(f"{wrt.center(value, char)}")
    sys.stdout.flush()

def check_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            return True  
    except requests.RequestException:
        pass  
    return False  

def load_scraped_dates(file_path):
    scraped_dates = set()
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                scraped_dates.add(line.strip())
    return scraped_dates

def save_scraped_dates(scraped_dates, file_path):
    with open(file_path, "a") as file:
        for date in scraped_dates:
            file.write(date + "\n")
def download_image(url, filename, article_no):
    try:
        response = requests.get(url)
        with open(filename, "wb") as f:
            f.write(response.content)
        return f"Article {article_no}"
    except Exception as e:
        return f"Failed to download {filename}: {e}"

def download_images(image_urls, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        sys.stdout.write("\n")

    with ThreadPoolExecutor(max_workers=20) as executor:  
        for i, url in enumerate(image_urls, 1):
            filename = os.path.join(folder_path, f"article_{i}.jpg")
            executor.submit(download_image, url, filename, i)
        sys.stdout.write(f"{len(image_urls)} articles")
    sys.stdout.write("\033[K")  
    sys.stdout.write("\033[F")  
    sys.stdout.write("\033[K") 

def scrape(year: str, month: str, day: str):
    url = f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php"
    # "https://old-epaper.jugantor.com/2020/07/27/index.php"  
    print(f"\nAccessing: {url}")
    driver.get(url)
    try:
        print("\nURL opened")
        image_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
        )
    except:
        print(f"\nCouldn't open URL")
        pass
        
    ul_element = driver.find_element_by_css_selector("ul.jPag-pages")
    li_elements = ul_element.find_elements_by_tag_name("li")
    num_pages = len(li_elements)
    
    for i in range(1, num_pages + 1):
        folder_path = f"downloaded_articles/jugantor/{year}/{month}/{day}/page_{i}"
        
        try:
            image_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
            )
        except:
            pass
        
        if i != 1:
            page_element = f"//*[@id='demo2']/div[2]/ul/li[{i}]/a"
            page = driver.find_element_by_xpath(page_element)
            page.click()
            # time.sleep(2)
            try:
                image_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
                )
            except:
                print("Error: Paper images didn't load")
                pass
        
        gen_prompt(f"Accessed Page {i}")
        
        urls=[link.get_attribute("src")for link in driver.find_elements_by_xpath("//img[contains(@class,'newsImg')]")]   
        modified_urls = [url.rsplit('/', 1)[0] + '/details/' + url.rsplit('/', 1)[1] for url in urls]
         
        download_images(modified_urls, folder_path)
    
    # time.sleep(2)
    
    print(f"\nSuccess: Scraped JUGANTOR-{year}/{month}/{day} \n")
    gen_prompt(f"Success: Scraped JUGANTOR-{year}/{month}/{day}", char="#")
    # driver.quit()
            
def scrape_all_range(start_year, start_month, start_day, end_year, end_month, end_day):
    file_path = os.path.join(BASE_DIR, "downloaded_articles", "scraped_dates.txt")
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
                scrape(year, month, day) 
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
            print(img_location)
            try: 
                article_title, article, num_words, raw_output = extract_article(img_location)
                insert_to_jugantor(year, f"{year}-{month}-{day}", article_title, article, num_words, i, f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php")
            except Exception as e:
                print("Did not initiate data entry:", e)
                pass
    print(f"Success: Article Extraction Completed! JUGANTOR-{year}/{month}/{day}")

if __name__ == "__main__":
    # scrape("2020", "01", "29")
    # extract_all_and_store("2016", "03", "08")
    scrape_all_range("2021", "01", "01", "2022", "07", "31")