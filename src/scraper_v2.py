
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import re
import concurrent.futures
from databbase import *

newspaper_base_url = 'https://www.jugantor.com/'
newspaper_archive_base_url = 'https://www.jugantor.com/archive/'

start_date = date(2024, 3, 4)
    
def insert_article(article_title, article_body, date, num_words, url):
    try:
        conn = sqlite3.connect('jugantor.db')
        c = conn.cursor()

        with conn:
            c.execute("INSERT INTO jugantor (year, date, article_title, article_body, wordcount, url) VALUES (?, ?, ?, ?, ?, ?)", 
                        (date.year, date, article_title, article_body, num_words, url))
        print("Data inserted successfully")
    except Exception as e:
        print("Did not initiate data entry:", e)
    finally:
        conn.close()
        
def crawl(date_str):
    date_str = date_str
    print(date_str)
    url = newspaper_archive_base_url + str(date_str.year) + "/" + str(date_str.month) + "/" + str(date_str.day)
    try:
        archive_soup = requests.get(url)
    except:
        print("No response for links in archive,trying to reconnect")
        time.sleep(2)
    print(url)
    soup = BeautifulSoup(archive_soup.content, "html.parser")
    links = []
    links_tag = soup.select('#archive-block .archive-newslist ul li a')
    
    for link_tag in links_tag:
        if 'today' in link_tag['href'] or 'old' in link_tag['href']:
            links.append(link_tag['href'])
    print(links)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(get_article, links)
    
def get_article(url):
    try:
        article_data = requests.get(url).text
    except:
        print("No response for content in link,trying to reconnect")
        time.sleep(2)
        
    soup = BeautifulSoup(article_data, "html.parser")
    
    article_title = soup.find(id='news-title').get_text().strip()
    article_title = re.sub(r'\s+', ' ', article_title)
    
    article_body = soup.find(id='myText').get_text().strip()
    article_body = re.sub(r'\s+', ' ', article_body)
    
    num_words = len(article_body.split())
    print(url)
    print(article_title)
    print(num_words)
    insert_article(article_title, article_body, start_date, num_words, url)

        
crawl(start_date)
