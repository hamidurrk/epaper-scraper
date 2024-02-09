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

conn = sqlite3.connect('jugantor.db')

def create_table():
    c = conn.cursor()
    c.execute("""CREATE TABLE jugantor (
                id integer primary key,
                year integer,
                date integer,
                article_title text,
                article text,
                wordcount integer,
                pagenum integer,
                url text
                )""")
    conn.close()

def insert_emp(year, date, article_title, article, wordcount, pagenum, url):
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO jugantor VALUES (:first, :last, :pay)", 
                  {'year': year, 'date': date, 'article_title': article_title, 'article': article, 'wordcount': wordcount, 'pagenum': pagenum, 'url': url})
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
    
    for i in range(1, num_pages):
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

def separate_article_heading(text):
    lines = text.split('\n', 1)
    if len(lines) > 1:
        first_line = lines[0]
        remaining_text = lines[1]
        return first_line, remaining_text
    else:
        return text, ""

if __name__ == "__main__":
    scrape("29", "01", "2020")