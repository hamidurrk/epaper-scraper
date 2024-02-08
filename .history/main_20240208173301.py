from selenium import webdriver
import os
import time

# Configure Firefox webdriver
firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument("--headless") 
driver = webdriver.Firefox(options=firefox_options)

# Function to download and store images
def download_images(image_urls, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i, url in enumerate(image_urls, 1):
        try:
            driver.get(url)
            time.sleep(2)  # Wait for the image to load (adjust as needed)
            img_element = driver.find_element_by_tag_name("img")
            image_data = img_element.screenshot_as_png
            with open(os.path.join(folder_path, f"image_{i}.png"), "wb") as f:
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
    image_elements = driver.find_element
    image_urls = [img_element.get_attribute("src") for img_element in image_elements]
    
    # Download images
    download_images(image_urls, folder_path)
    
    # Close the webdriver
    driver.quit()

if __name__ == "__main__":
    main()
