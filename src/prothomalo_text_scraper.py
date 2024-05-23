import asyncio
import os
import re
import sys
import sqlite3
import aiohttp
import tqdm
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
from utils import load_info, save_info, check_internet_connection, gen_prompt, date_to_timestamp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from utils import *

class ProthomAloScraper:
    def __init__(self, driver):
        self.driver = driver
        self.newspaper_base_url = 'https://www.jugantor.com/'
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.DATABASE_PATH = os.path.join(self.BASE_DIR, "files", 'prothomalo.db')
        self.stored_dates = os.path.join(self.BASE_DIR, "downloaded_articles", "scraped_dates_prothomalo.txt")
        self.test_date_str = date(2012, 1, 1)

    def load_all_content(self, wait_time=5):
        previous_count = 0
        count = 0
        while True:
            current_count = len(self.driver.find_elements(By.CLASS_NAME, 'K-MQV'))
            
            if current_count == previous_count:
                count += 1
            else:
                count = 0
                
            if count >= 10:
                break

            previous_count = current_count

            try:
                load_more_button = WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.more._7ZpjE .load-more-content._7QoIj'))
                )
                load_more_button.click()
                time.sleep(wait_time)
            except:
                break

    def extract_links(self):
        news_items = self.driver.find_elements(By.CLASS_NAME, 'news_item_content')
        links = []
        print(len(news_items))
        
        for item in news_items:
            link_element = item.find_element(By.CSS_SELECTOR, 'a.title-link')
            link = link_element.get_attribute('href')
            links.append(link)
        secure_links = [re.sub(r'^http://', 'https://', link) for link in links]
        return secure_links

    async def insert_articles(self, articles):
        try:
            conn = sqlite3.connect(self.DATABASE_PATH)
            c = conn.cursor()
            with conn:
                c.executemany("INSERT INTO prothomalo (year, date, article_title, article_body, wordcount, url) VALUES (?, ?, ?, ?, ?, ?)", articles)
            print("Data inserted successfully")
        except Exception as e:
            print("Did not initiate data entry:", e)
        finally:
            conn.close()

    async def crawl(self, date_str):
        print(date_str)
        newspaper_archive_base_url = 'https://www.prothomalo.com/search?'  
        min_ts, max_ts = date_to_timestamp(date_str)  
        url = newspaper_archive_base_url + "published-before=" + str(max_ts) + "&published-after=" + str(min_ts)
        print(url)
        
        if not is_open(self.driver, url):
            self.driver.get(url)

        print("Loading all articles...")
        self.load_all_content(wait_time=0.5)
        links = self.extract_links()
        print(f"\n{len(links)} links")

        tasks = []
        articles = []
        for link in links:
            task = asyncio.create_task(self.get_article(link, articles, date_str))
            tasks.append(task)

        await asyncio.gather(*tasks)
        print(f"{len(articles)} articles gathered from {len(links)} links")
        await self.insert_articles(articles)

    async def get_article(self, url, articles, date):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    article_data = await response.text()
        except Exception as e:
            print("Error: ", e)
            return
        
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
            # print(article_title)
            # print(f"{num_words} words\n")
            articles.append((date.year, date, article_title, article_body, num_words, url))

    async def scrape_all_range_palo(self, start_year, start_month, start_day, end_year, end_month, end_day):
        start_date = date(start_year, start_month, start_day)
        end_date = date(end_year, end_month, end_day)
        total_iterations = (end_date - start_date).days + 1

        pbar = tqdm.tqdm(total=total_iterations, desc="Progress", unit="paper")
        current_date = start_date
        scraped_dates = load_info(self.stored_dates)
        count = 0
        while current_date <= end_date:
            sys.stdout.write("\n\n")
            year = str(current_date.year)
            month = str(current_date.month).zfill(2)
            day = str(current_date.day).zfill(2)
            date_str = f"{year}-{month}-{day}"
            no_exception_found = 1
            if date_str not in scraped_dates:
                print(f"Attempting New Scrape | Year: {year}, Month: {month}, Day: {day}")
                try:
                    await self.crawl(current_date)
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
                    save_info({date_str}, self.stored_dates)
            else:
                pbar.update(1)
                print(f"{date_str} already scraped.")
                current_date += timedelta(days=1)
        pbar.close()
        if count == total_iterations:
            print(f"\nScraping finished from {start_date} to {end_date}")
        else:
            print(f"\nScraping finished from {start_date} to {date_str}")

if __name__ == "__main__":
    firefox_options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), service_args=['--marionette-port', '2828', '--connect-existing'], options=firefox_options)
    scraper = ProthomAloScraper(driver)
    asyncio.run(scraper.scrape_all_range_palo(2012, 1, 1, 2012, 12, 31))
