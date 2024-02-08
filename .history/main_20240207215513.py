import requests
from bs4 import BeautifulSoup
import os

def download_images(image_urls, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i, url in enumerate(image_urls, 1):
        try:
            response = requests.get(url)
            with open(os.path.join(folder_path, f"image_{i}.jpg"), "wb") as f:
                f.write(response.content)
                print(f"Downloaded image_{i}.jpg")
        except Exception as e:
            print(f"Failed to download image_{i}: {e}")

def scrape_images(url):
    image_urls = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        images = soup.find_all("table")
        
        print(images)
        for img in images:
            image_urls.append(img["src"])
    except Exception as e:
        print(f"Failed to scrape images: {e}")
    return image_urls

def main():
    url = "https://old-epaper.jugantor.com/2020/07/27/index.php"  
    image_urls = scrape_images(url)
    download_images(image_urls, "downloaded_images")

if __name__ == "__main__":
    main()
