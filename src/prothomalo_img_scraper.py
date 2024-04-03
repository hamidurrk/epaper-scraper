import os
import sys
import time
from datetime import date, timedelta
from tqdm import tqdm
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from utils import *

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), service_args=['--marionette-port', '2828', '--connect-existing'], options=firefox_options)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

base_url = f"https://epaper.prothomalo.com/Home/"
print(f"Accessed Prothom Alo")
driver.get(base_url)

def scrape_jugantor(year: str, month: str, day: str):
    url = f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php"
    print(f"\nAccessing: {url}")
    driver.get(url)
    try:
        print("\nURL opened")
        image_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
        )
    except:
        print(f"\nCouldn't open URL")
        pass
        
    ul_element = driver.find_element_by_css_selector("ul.jPag-pages")
    li_elements = ul_element.find_elements_by_tag_name("li")
    num_pages = len(li_elements)
    
    for i in range(1, num_pages + 1):
        folder_path = f"downloaded_articles/jugantor/{year}/{month}/{day}/page_{i}"
        
        try:
            image_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
            )
        except:
            pass
        
        if i != 1:
            page_element = f"//*[@id='demo2']/div[2]/ul/li[{i}]/a"
            page = driver.find_element_by_xpath(page_element)
            page.click()
            try:
                image_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
                )
            except:
                print("Error: Paper images didn't load")
                pass
        
        gen_prompt(f"Accessed Page {i}")
        
        urls=[link.get_attribute("src")for link in driver.find_elements_by_xpath("//img[contains(@class,'newsImg')]")]   
        modified_urls = [url.rsplit('/', 1)[0] + '/details/' + url.rsplit('/', 1)[1] for url in urls]
         
        download_images(modified_urls, folder_path)
    
    print(f"\nSuccess: Scraped JUGANTOR-{year}/{month}/{day} \n")
    gen_prompt(f"Success: Scraped JUGANTOR-{year}/{month}/{day}", char="#")

def scrape_old_jugantor(year: str, month: str, day: str):
    url = f"https://old-epaper.jugantor.com/{year}/{month}/{day}/index.php"
    print(f"\nAccessing: {url}")
    driver.get(url)
    try:
        print("\nURL opened")
        image_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
        )
    except:
        print(f"\nCouldn't open URL")
        pass
            
    i = 0
    while(True):
        i += 1
        folder_path  = os.path.join(BASE_DIR, "downloaded_articles", "jugantor", year, month, day, f"page_{i}")
        
        try:
            image_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
            )
        except:
            break
              
        if i != 1:
            next_page_link = driver.find_element_by_xpath("//a[@onclick='goToNextPage();return false;']")
            next_page_link.click()
            
            try:
                error_element = driver.find_element(By.XPATH, "//h1[contains(text(), 'Not Found')]")
                if error_element:
                    break
            except:
                pass
            
            try:
                image_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "newsImg"))
                )
            except Exception as e:
                print("Error: Paper images didn't load", e)
                break
        
        gen_prompt(f"Accessed Page {i}")
        
        urls=[link.get_attribute("src")for link in driver.find_elements_by_xpath("//img[contains(@class,'newsImg')]")]   
        modified_urls = [url.rsplit('/', 1)[0] + '/details/' + url.rsplit('/', 1)[1] for url in urls]
        
        download_images(modified_urls, folder_path)
    
    print(f"\nSuccess: Scraped JUGANTOR-{year}/{month}/{day} \n")
    gen_prompt(f"Success: Scraped JUGANTOR-{year}/{month}/{day}", char="#")
   
# ------------------------------------- scrape_recent_jugantor ----------------------------------------/
def wait_until_visible(class_name):
    try:
        image_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, f"{class_name}"))
        )
    except:
        print(f"\nCouldn't open URL")
        pass
def load_paper(year: str, month: str, day: str): 
    wait_until_visible("pagerectangle")
    date_to_set = f"{day}/{month}/{year}"  
    script = f"""
        SetCDNUrl('https://epaper.prothomalo.com/');
        // SAM calling
        SAM_PageFirstLoad();
        SAM_Pageload();
        moblayoutPageLoad();
        if (IsDateChangedFromUrl == 0) setcookies("changeddate", '{date_to_set}');
        
        $('[data-toggle="tooltip"]').tooltip();
        $("#datepicker").datepicker("setDate", '{date_to_set}');

        if ('0' != '' && '0' != '0') setcookies("PageId", '0');
        
        setcookies("EditionId", '1');
        setcookies("MainEditionId", '1');
        ShowDatePopUp();
        document.querySelector('.ui-datepicker-current-day').click();
    """
    driver.execute_script(script)
    # wait_until_visible("ui-widget-content")
    # element = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, "ui-datepicker-current-day"))
    # )
    # element.click()

def get_orgid():
    orgid_elements = driver.find_elements_by_class_name("pagerectangle")

    orgid_values = []
    for element in orgid_elements:
        orgid = element.get_attribute("orgid")
        orgid_values.append(orgid)

    print(orgid_values)
    return orgid_values
     


async def fetch_image_urls(session, api_url, area_data):
    async with session.get(api_url, params=area_data) as response:
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            img_tags = soup.find('div', class_='img-ScrollBar').find_all('img')
            img_urls = [img_tag['src'] for img_tag in img_tags]
            return img_urls
        else:
            return []

async def scrape_page(session, api_url, area_data_list):
    tasks = []
    for area_data in area_data_list:
        tasks.append(fetch_image_urls(session, api_url, area_data))
    
    try:
        img_urls = await asyncio.gather(*tasks)
        img_urls = [url for sublist in img_urls for url in sublist]
        print("API requests successful")
        return img_urls
    except Exception as e:
        print("API request failed!")
        return None

async def main(driver, year, month, day):
    load_paper(year, month, day)
    while(1):
        try:
            paper_date_element = driver.find_element_by_id("article_list_date_mobile")
            paper_date = paper_date_element.text
            # print("waiting")
            time.sleep(0.2)
            if compare_dates(paper_date, f"{month}/{day}/{year}"):
                page_html = driver.page_source
                soup = BeautifulSoup(page_html, 'html.parser')
                li_elements = soup.find_all(class_="owl-item")
                num_pages = len(li_elements)
                # print(num_pages)
                if num_pages > 5:
                    break
        except:
            pass
    print(num_pages)
        
    
    # async with aiohttp.ClientSession() as session:
    #     for i in range(1, num_pages + 1):
    #         folder_path = f"downloaded_articles/jugantor/{year}/{month}/{day}/page_{i}"
    #         try:
    #             image_elements = WebDriverWait(driver, 10).until(
    #                 EC.presence_of_element_located((By.CLASS_NAME, "view_modal"))
    #             )
    #             gen_prompt(f"Accessed Page {i}")
    #         except:
    #             print("Error: Paper page didn't load")
    #             continue
            
    #         if i != 1:
    #             page = driver.find_element_by_class_name("nextPageButton")
    #             page.click()
            
    #         edition_id = driver.find_element_by_id("edition_id").get_attribute("value")
    #         area_tags = driver.find_elements_by_css_selector('area.view_modal')

    #         area_data_list = []
    #         for area_tag in area_tags:
    #             data_mapid = area_tag.get_attribute('data-mapid')
    #             coords = area_tag.get_attribute('coords')
    #             area_data_list.append({'coords': coords, 'edition_id': edition_id, 'ed_map_id': data_mapid})
    #         print("\nAPI params extracted. Making API requests...")
            
    #         img_urls = await scrape_page(session, api_url, area_data_list)
            
    #         download_images(img_urls, folder_path)
    #         clear_last_lines(5)

    # print(f"\nSuccess: Scraped JUGANTOR-{year}/{month}/{day} \n")

asyncio.run(main(driver, "2012", "01", "01"))

# ------------------------------------- scrape_recent_jugantor end ----------------------------------------/

def scrape_all_range(start_year, start_month, start_day, end_year, end_month, end_day):
    file_path = os.path.join(BASE_DIR, "downloaded_articles", "scraped_dates.txt")
    start_year = int(start_year)
    start_month = int(start_month)
    start_day = int(start_day)

    end_year = int(end_year)
    end_month = int(end_month)
    end_day = int(end_day)

    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    total_iterations = (end_date - start_date).days + 1
    
    pbar = tqdm(total=total_iterations, desc="Progress", unit="paper",)
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
                asyncio.run(main(driver, year, month, day)) 
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
  

