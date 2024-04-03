import os
import requests
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def check_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            return True  
    except requests.RequestException:
        pass  
    return False  

def compare_dates(date_str1, date_str2):
    # Parse the dates
    date1 = datetime.strptime(date_str1, "%A, %b %d, %Y")
    date2 = datetime.strptime(date_str2, "%m/%d/%Y")
    
    # Compare the dates
    return date1.date() == date2.date()

def load_info(file_path):
    scraped_dates = set()
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                scraped_dates.add(line.strip())
    return scraped_dates

def save_info(scraped_dates, file_path):
    with open(file_path, "a") as file:
        for date in scraped_dates:
            file.write(date + "\n")
            
def clear_last_lines(x):
    for _ in range(x):
        sys.stdout.write("\033[F")  
        sys.stdout.write("\033[K")  
        
def gen_prompt(message, value=70, char="-"):
    wrt = " " + message + " "
    sys.stdout.write(f"{wrt.center(value, char)}")
    sys.stdout.flush()
    sys.stdout.write("\n")

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
        print("Download started...")
        # sys.stdout.write("\n")

    with ThreadPoolExecutor(max_workers=20) as executor:  
        for i, url in enumerate(image_urls, 1):
            filename = os.path.join(folder_path, f"article_{i}.jpg")
            executor.submit(download_image, url, filename, i)
        print(f"{len(image_urls)} articles downloaded")
    #     sys.stdout.write(f"{len(image_urls)} articles")
    # sys.stdout.write("\033[K")  
    # sys.stdout.write("\033[F")  
    # sys.stdout.write("\033[K")
