from selenium import webdriver
import os
import requests
import time
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from PIL.ExifTags import TAGS

firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument("--headless") 
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

def add_url_metadata(image_path, url):
    # Open the image file
    img = Image.open(image_path)
    
    # Get Exif data (if available)
    exif_data = img.getexif()
    
    # Define a custom Exif tag for the URL metadata
    custom_exif_tag = 40000
    
    # Create a dictionary to store the custom metadata
    custom_metadata = {custom_exif_tag: url}
    
    # Convert the custom metadata dictionary to a format suitable for Exif
    exif_bytes = {TAGS[key]: custom_metadata[key] for key in custom_metadata}
    
    # Update the image Exif data with the custom metadata
    img_exif = img.info.get('exif', {})
    img_exif.update(exif_bytes)
    
    # Save the image with the updated Exif data
    img.save(image_path, exif=img_exif)
    

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
            add_url_metadata(image_path, url)
        except Exception as e:
            print(f"Failed to download article_{url}: {e}")

def main():
    day = "27"
    month = "07"
    year = "2020"

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

if __name__ == "__main__":
    main()