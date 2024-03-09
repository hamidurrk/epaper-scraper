from selenium import webdriver
import os
import requests
import time
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from PIL import Image    
import pytesseract

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
    conn.close()

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

def scrape(day: str, month: str, year: str):
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
            article_title, article, num_words, raw_output = extract_article(img_location)
            insert_to_jugantor(year, f"{year}-{month}-{day}", article_title, article, num_words, i, f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php")
            

if __name__ == "__main__":
    # scrape("29", "01", "2020")
    extract_all_and_store("2020", "07", "27")