from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests, tqdm, os, sys, re, time
import concurrent.futures
from databbase import *
from utils import *

newspaper_base_url = 'https://www.jugantor.com/'
newspaper_archive_base_url = 'https://www.jugantor.com/archive/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

start_date = date(2024, 3, 4)
    
def insert_article(article_title, article_body, date, num_words, url):
    try:
        conn = sqlite3.connect('jugantor.db')
        c = conn.cursor()

        with conn:
            c.execute("INSERT INTO jugantor (year, date, article_title, article_body, wordcount, url) VALUES (?, ?, ?, ?, ?, ?)", 
                        (date.year, date, article_title, article_body, num_words, url))
        # print("Data inserted successfully")
    except Exception as e:
        print("Did not initiate data entry:", e)
    finally:
        conn.close()
        
def crawl(date_str):
    date_str = date_str
    # print(date_str)
    url = newspaper_archive_base_url + str(date_str.year) + "/" + str(date_str.month) + "/" + str(date_str.day)

    archive_soup = requests.get(url)
    print(url)
    soup = BeautifulSoup(archive_soup.content, "html.parser")
    links = []
    links_tag = soup.select('#archive-block .archive-newslist ul li a')
    
    for link_tag in links_tag:
        if 'today' in link_tag['href'] or 'old' in link_tag['href']:
            links.append(link_tag['href'])
    print(f"{len(links)} articles")
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        for _ in tqdm.tqdm(executor.map(get_article, links), total=len(links), desc='', leave=False):
            pass
    
def get_article(url):
    article_data = requests.get(url).text
        
    soup = BeautifulSoup(article_data, "html.parser")
    
    article_title = soup.find(id='news-title').get_text().strip()
    article_title = re.sub(r'\s+', ' ', article_title)
    
    article_body = soup.find(id='myText').get_text().strip()
    article_body = re.sub(r'\s+', ' ', article_body)
    
    num_words = len(article_body.split())
    # print(url)
    # print(article_title)
    # print(num_words)
    insert_article(article_title, article_body, start_date, num_words, url)

def scrape_all_range(start_year, start_month, start_day, end_year, end_month, end_day):
    file_path = os.path.join(BASE_DIR, "downloaded_articles", "bs4_scraped_dates.txt")
    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    total_iterations = (end_date - start_date).days + 1
    
    pbar = tqdm.tqdm(total=total_iterations, desc="Progress", unit="paper")
    current_date = start_date
    scraped_dates = load_info(file_path)
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
                    break
                print("Page Unavailable: Redirecting...")
                # time.sleep(2)
                pass
            if no_exception_found:
                scraped_dates.add(date_str)
                save_info({date_str}, file_path)
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
  

# crawl(start_date)
scrape_all_range(2024, 3, 1, 2024, 3, 3)
