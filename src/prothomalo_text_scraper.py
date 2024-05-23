import asyncio
import os
import re
import sys
import sqlite3
import aiohttp
import tqdm
import time
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from datetime import date, timedelta
from bs4 import BeautifulSoup
from utils import load_info, save_info, check_internet_connection, gen_prompt, date_to_timestamp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.firefox import GeckoDriverManager
from utils import *

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), service_args=['--marionette-port', '2828', '--connect-existing'], options=firefox_options)

newspaper_base_url = 'https://www.jugantor.com/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "files", 'prothomalo.db')
stored_dates = os.path.join(BASE_DIR, "downloaded_articles", "scraped_dates_prothomalo.txt")

test_date_str = date(2012, 1, 1)

def load_all_content(driver, wait_time=5):
    previous_count = 0
    count = 0
    while True:
        current_count = len(driver.find_elements(By.CLASS_NAME, 'K-MQV'))
        
        if current_count == previous_count:
            count+=1
        else:
            count = 0
            
        if count >= 10:
            break

        previous_count = current_count

        try:
            load_more_button = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.more._7ZpjE .load-more-content._7QoIj'))
            )
            load_more_button.click()
            time.sleep(wait_time)
        except:
            break

def extract_links(driver):
    news_items = driver.find_elements(By.CLASS_NAME, 'news_item_content')

    links = []
    print(len(news_items))
    
    for item in news_items:
        link_element = item.find_element(By.CSS_SELECTOR, 'a.title-link')
        link = link_element.get_attribute('href')
        links.append(link)
    secure_links = [re.sub(r'^http://', 'https://', link) for link in links]
    return secure_links

async def insert_articles(articles):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()

        with conn:
            c.executemany("INSERT INTO prothomalo (year, date, article_title, article_body, wordcount, url) VALUES (?, ?, ?, ?, ?, ?)", articles)
        print("Data inserted successfully")
    except Exception as e:
        print("Did not initiate data entry:", e)
    finally:
        conn.close()


async def crawl(date_str):
    print(date_str)
    newspaper_archive_base_url = 'https://www.prothomalo.com/search?'  
    min, max = date_to_timestamp(date_str)  
    url = newspaper_archive_base_url + "published-before=" + str(max) + "&published-after=" + str(min)
    print(url)
    
    if not is_open(driver, url):
        driver.get(url)
        

    load_all_content(driver, 0.5)
    links = []
    links = extract_links(driver)
    # for link in links:
    #     print(link)
    print(f"\n{len(links)} articles")

    tasks = []
    articles = []
    for link in links:
        task = asyncio.create_task(get_article(link, articles, date_str))
        tasks.append(task)

    await asyncio.gather(*tasks)
    print(len(articles), "Articles Gathered.")
    await insert_articles(articles)


async def get_article(url, articles, date):
    # print(url)
    # print(type(url))
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                article_data = await response.text()
                # print(f"response{await response)}")
    except Exception as e:
        print("Error: ", e)
    soup = BeautifulSoup(article_data, "lxml")
    article_title_obj = soup.find('div', class_='story-title-info')
    if article_title_obj is not None:
        article_title_obj = article_title_obj.find('h1')
        article_title = article_title_obj.get_text(strip=True)
        article_title = re.sub(r'\s+', ' ', article_title)

        article_body = soup.find('div', class_='story-element')
        article_body = article_body.find('p')
        article_body = article_body.get_text(strip=True)
        article_body = re.sub(r'\s+', ' ', article_body)

        num_words = len(article_body.split())
        print(article_title)
        print(f"{num_words} words\n")
        articles.append((date.year, date, article_title, article_body, num_words, url))


async def scrape_all_range(start_year, start_month, start_day, end_year, end_month, end_day):
    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    total_iterations = (end_date - start_date).days + 1

    pbar = tqdm.tqdm(total=total_iterations, desc="Progress", unit="paper")
    current_date = start_date
    scraped_dates = load_info(stored_dates)
    count = 0
    while current_date <= end_date:
        # os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.write("\n\n")
        year = str(current_date.year)
        month = str(current_date.month).zfill(2)
        day = str(current_date.day).zfill(2)
        date_str = f"{year}-{month}-{day}"
        no_exception_found = 1
        if date_str not in scraped_dates:
            print(f"Attempting New Scrape | Year: {year}, Month: {month}, Day: {day}")
            try:
                await crawl(current_date)
                pbar.update(1)
                count += 1
            except Exception as e:
                no_exception_found = 0
                print("Scraping error: ", e)
                print(f"Error on: Year: {year}, Month: {month}, Day: {day}")
                if check_internet_connection():
                    print("Internet connection is available.")
                else:
                    print("No internet connection.")
                    time.sleep(2)
                    pass
                print("Page Unavailable: Redirecting...")
                pass
            if no_exception_found:
                current_date += timedelta(days=1)
                scraped_dates.add(date_str)
                save_info({date_str}, stored_dates)
            # time.sleep(0.1)
        else:
            # os.system('cls' if os.name == 'nt' else 'clear')
            pbar.update(1)
            print(f"{date_str} already scraped.")
            current_date += timedelta(days=1)
            # time.sleep(0.1)
    pbar.close()
    if count == total_iterations:
        print(f"\nScraping finished from {start_date} to {end_date}")
    else:
        print(f"\nScraping finished from {start_date} to {date_str}")


# await crawl(test_date_str)

asyncio.run(scrape_all_range(2012, 1, 1, 2012, 1, 1))
