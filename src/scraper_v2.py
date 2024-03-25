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
from utils import load_info, save_info, check_internet_connection, gen_prompt

newspaper_base_url = 'https://www.jugantor.com/'
newspaper_archive_base_url = 'https://www.jugantor.com/archive/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

async def insert_articles(articles):
    try:
        conn = sqlite3.connect('jugantor.db')
        c = conn.cursor()

        with conn:
            c.executemany("INSERT INTO jugantor (year, date, article_title, article_body, wordcount, url) VALUES (?, ?, ?, ?, ?, ?)", articles)
        # print("Data inserted successfully")
    except Exception as e:
        print("Did not initiate data entry:", e)
    finally:
        conn.close()


async def crawl(date_str):
    date_str = date_str
    # print(date_str)
    url = newspaper_archive_base_url + str(date_str.year) + "/" + str(date_str.month) + "/" + str(date_str.day)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            archive_soup = BeautifulSoup(await response.text(), "lxml")

    # print(url)
    links = []
    links_tag = archive_soup.select('#archive-block .archive-newslist ul li a')

    for link_tag in links_tag:
        if 'today' in link_tag['href'] or 'old' in link_tag['href']:
            links.append(link_tag['href'])
    print(f"\n{len(links)} articles")

    tasks = []
    articles = []
    for link in links:
        task = asyncio.create_task(get_article(link, articles, date_str))
        tasks.append(task)

    await asyncio.gather(*tasks)
    await insert_articles(articles)


async def get_article(url, articles, date_str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            article_data = await response.text()

    soup = BeautifulSoup(article_data, "lxml")

    article_title = soup.find(id='news-title').get_text().strip()
    article_title = re.sub(r'\s+', ' ', article_title)

    article_body = soup.find(id='myText').get_text().strip()
    article_body = re.sub(r'\s+', ' ', article_body)

    num_words = len(article_body.split())

    articles.append((date_str.year, date_str, article_title, article_body, num_words, url))


async def scrape_all_range(start_year, start_month, start_day, end_year, end_month, end_day):
    file_path = os.path.join(BASE_DIR, "downloaded_articles", "bs4_scraped_dates.txt")
    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    total_iterations = (end_date - start_date).days + 1

    pbar = tqdm.tqdm(total=total_iterations, desc="Progress", unit="paper")
    current_date = start_date
    scraped_dates = load_info(file_path)
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
                save_info({date_str}, file_path)
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


# crawl(start_date)
asyncio.run(scrape_all_range(2018, 1, 1, 2024, 3, 20))
