from selenium import webdriver
import os
import requests
import time
import sys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from PIL import Image    
import pytesseract
from datetime import date, timedelta
from tqdm import tqdm

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))       
conn = sqlite3.connect('jugantor.db')

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
    # conn.close()

def download_images(image_urls, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i, url in enumerate(image_urls, 1):
        try:
            response = requests.get(url)
            image_path = os.path.join(folder_path, f"article_{i}.jpg")
            with open(image_path, "wb") as f:
                f.write(response.content)
                print(f"Downloaded article_{i}.jpg")
        except Exception as e:
            print(f"Failed to download article_{url}: {e}")

def scrape(year: str, month: str, day: str):
    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument("--headless") 
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    url = f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php"
    # "https://old-epaper.jugantor.com/2020/07/27/index.php"  
    
    driver.get(url)
    try:
        image_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
        )
    except:
        driver.quit()
        
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
            driver.quit()
            
        if i != 1:
            page_element = f"//*[@id='demo2']/div[2]/ul/li[{i}]/a"
            page = driver.find_element_by_xpath(page_element)
            page.click()

        urls=[link.get_attribute("src")for link in driver.find_elements_by_xpath("//img[contains(@class,'newsImg')]")]   
        modified_urls = [url.rsplit('/', 1)[0] + '/details/' + url.rsplit('/', 1)[1] for url in urls]
         
        download_images(modified_urls, folder_path)
    
    time.sleep(2)
    
    print(f"Success: Scraped JUGANTOR-{year}/{month}/{day}")
    driver.quit()
    
def scrape_all_range(start_year, start_month, start_day, end_year, end_month, end_day):
    start_year = int(start_year)
    start_month = int(start_month)
    start_day = int(start_day)

    # end_year = date.today().year
    # end_month = date.today().month
    # end_day = date.today().day

    end_year = int(end_year)
    end_month = int(end_month)
    end_day = int(end_day)

    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    total_days = (end_date - start_date).days + 1
    with tqdm(total=total_days, position=1) as pbar:
        current_date = start_date
        while current_date <= end_date:
            year = str(current_date.year)
            month = str(current_date.month).zfill(2)
            day = str(current_date.day).zfill(2)
            sys.stdout.write(f"\rYear: {year}, Month: {month}, Day: {day}")
            # sys.stdout.flush()
            # print(f"Year: {year}, Month: {month}, Day: {day}")
            scrape(year, month, day)
            current_date += timedelta(days=1)
            time.sleep(0.1)
            pbar.update(1)
    print(f"\nScraping finished from {start_date} to {end_date}")

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
    conn.close()

if __name__ == "__main__":
    # scrape("2020", "01", "29")
    # extract_all_and_store("2020", "07", "27")
    scrape_all_range("2024", "01", "01", "2024", "03", "01")