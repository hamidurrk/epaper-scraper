import os
import requests
import sys
from concurrent.futures import ThreadPoolExecutor

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

def gen_prompt(message, value=70, char="-"):
    wrt = " " + message + " "
    sys.stdout.write(f"{wrt.center(value, char)}")
    sys.stdout.flush()

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
