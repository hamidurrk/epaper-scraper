import os
import re
import sys
import sqlite3
import requests
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
from utils import load_info, save_info, check_internet_connection, gen_prompt

newspaper_base_url = 'https://www.jugantor.com/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

test_date_str = date(2016, 3, 4)

def insert_articles(articles):
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

def crawl(date_str):
    print(date_str)
    if date_str.year >= 2018:
        newspaper_archive_base_url = 'https://www.jugantor.com/archive/'    
    else:
        newspaper_archive_base_url = 'https://www.jugantor.com/news-archive/'
    url = newspaper_archive_base_url + str(date_str.year) + "/" + str(date_str.month) + "/" + str(date_str.day)
    response = requests.get(url)
    archive_soup = BeautifulSoup(response.text, "lxml")

    links = []
    links_tag = archive_soup.select('#archive-block .archive-newslist ul li a')

    for link_tag in links_tag:
        link_tag['href']
        if 'today' in link_tag['href'] or 'old' in link_tag['href']:
            links.append(link_tag['href'])
    print(f"\n{len(links)} articles")

    articles = []
    for link in links:
        get_article(link, articles, date_str)

    # insert_articles(articles)

def get_article(url, articles, date):
    print(url)
    print(type(url))
    try:
        session = requests.Session()
        response = session.get(url, allow_redirects=False)
        redirect_url = response.headers['Location']
        # now we can manually inspect and fix the redirect url if necessary and then follow it:
        response2 = session.get(redirect_url, allow_redirects=False)
        # response = requests.get(url)
        # article_data = response.text
        print(f"response: {response.headers['Location']}")
        print(f"response: {response2}")
    except Exception as e:
        print("Error: ", e)
    soup = BeautifulSoup(response2.text, "lxml")

    article_title = soup.find(id='news-title').get_text().strip()
    article_title = re.sub(r'\s+', ' ', article_title)

    article_body = soup.find(id='myText').get_text().strip()
    article_body = re.sub(r'\s+', ' ', article_body)

    num_words = len(article_body.split())
    print(f"\n{num_words} words")
    articles.append((date.year, date, article_title, article_body, num_words, url))

def scrape_all_range(start_year, start_month, start_day, end_year, end_month, end_day):
    file_path = os.path.join(BASE_DIR, "downloaded_articles", "bs4_scraped_dates.txt")
    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    total_iterations = (end_date - start_date).days + 1

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
                crawl(current_date)
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
            print(f"{date_str} already scraped.")
            current_date += timedelta(days=1)
            # time.sleep(0.1)
    if count == total_iterations:
        print(f"\nScraping finished from {start_date} to {end_date}")
    else:
        print(f"\nScraping finished from {start_date} to {date_str}")

# crawl(start_date)
scrape_all_range(2016, 1, 1, 2024, 3, 20)
