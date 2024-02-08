from selenium import webdriver
import os
import time
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uuid

# Configure Firefox webdriver
firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument("--headless") 
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
# driver = webdriver.Firefox(executable_path='/Users/hamid/OneDrive/Documents/geckodriver.exe', options=firefox_options)

# Function to download and store images
def download_images(elements, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i, element in enumerate(elements, 1):
        try:
            image_data = element.screenshot_as_png
            with open(os.path.join(folder_path, f"image_{uuid.uuid4()}.png"), "wb") as f:
                f.write(image_data)
                print(f"Downloaded image_{i}.png")
        except Exception as e:
            print(f"Failed to download image_{i}: {e}")

# Main function
def main():
    url = "https://old-epaper.jugantor.com/2020/07/27/index.php"  # Replace this with the actual URL
    folder_path = "downloaded_images"
    
    # Scrape image URLs
    driver.get(url)
    try:
        image_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
        )
    except:
        driver.quit()
    # image_elements = driver.find_element_by_name("n1_r2_c2")
    print(image_elements)
    
    # image_urls = [img_element.get_attribute("src") for img_element in image_elements]
    
    # # Download images
    # download_images(image_urls, folder_path)
    download_images(image_elements, folder_path)
    
    # Close the webdriver
    driver.quit()

if __name__ == "__main__":
    main()
