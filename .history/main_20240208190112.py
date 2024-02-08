from selenium import webdriver
import os
import requests
import time
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument("--headless") 
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

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

def main():
    url = "https://old-epaper.jugantor.com/2020/07/27/index.php"  
    folder_path = "downloaded_images"
    
    driver.get(url)
    try:
        image_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
        )
    except:
        driver.quit()
        
    print(image_elements)
    urls=[link.get_attribute("src")for link in driver.find_elements_by_xpath("//img[contains(@class,'newsImg')]")]
    # print(urls)
    
    # modified_urls = [url.rsplit('/', 1)[0] + '/details/' + url.rsplit('/', 1)[1] for url in urls]

    # for modified_url in modified_urls:
    #     print(modified_url)
        
    pages = driver.find_elements_by_xpath("//ul[contains(@class,'jPag-pages')]")
    print(pages)
    
    # download_images(modified_urls, folder_path)
    
    # for _ in range(25):
    #     driver.execute_script("goToNextPage();return false;")
    #     time.sleep(2)
    
    # //*[@id="demo2"]/div[2]/ul/li[7]/a
    # //*[@id="demo2"]/div[2]/ul/li[14]/a
    # //*[@id="demo2"]/div[2]/ul/li[14]/a
    # //*[@id="demo2"]/div[2]/ul
    driver.quit()

if __name__ == "__main__":
    main()