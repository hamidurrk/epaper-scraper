import os
import re
import sys
import time
import asyncio
import aiohttp
import requests
from tqdm import tqdm
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.firefox import GeckoDriverManager
from utils import *

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), service_args=['--marionette-port', '2828', '--connect-existing'], options=firefox_options)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

base_url = f"https://epaper.prothomalo.com/Home/"
print(f"Accessed Prothom Alo")
# driver.get(base_url)

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
    except Exception as e:
        print(e)
        # raise Exception(f"\nCouldn't open URL: '{class_name}' not visible")
        
    
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

def get_orgid():
    orgid_elements = driver.find_elements_by_class_name("pagerectangle")

    orgid_values = []
    for element in orgid_elements:
        orgid = element.get_attribute("orgid")
        orgid_values.append(orgid)

    return orgid_values

def process_for_article_image(html_content, output_directory):
    soup = BeautifulSoup(html_content, 'html.parser')

    pagerectangle_page_ids = set(div['pageid'] for div in soup.find_all("div", class_="pagerectangle"))
    print("Pagerectangle page IDs:", pagerectangle_page_ids)

    os.makedirs(output_directory, exist_ok=True)

    for img_tag in soup.find_all('img', class_='img_jpg'):
        img_page_id = img_tag.get('page_id')
        
        if img_page_id in pagerectangle_page_ids:
            image_layer_elements = [div for div in soup.find_all("div", class_="image_layer") if div['id'].replace('image_layer', '') in pagerectangle_page_ids]
            # print(image_layer_elements)
            for image_layer in image_layer_elements:
                print(f"Found image_layer with page_id: {image_layer['id'].replace('image_layer', '')}")
                print(image_layer['style'])
                style_string = image_layer['style']
                width_pattern = r'width:\s*([\d.]+)px'
                height_pattern = r'height:\s*([\d.]+)px'
                
                width_match = re.search(width_pattern, style_string)
                height_match = re.search(height_pattern, style_string)
                
                total_width = float(width_match.group(1)) if width_match else None
                total_height = float(height_match.group(1)) if height_match else None
            
            image_url = img_tag['xhighres']
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            # image = image.resize((869, 1373))
            image_width, image_height = image.size

            div_elements = [div for div in soup.find_all("div", class_="pagerectangle") if div['pageid'] == img_page_id]


            for div in div_elements:
                top = int(div['style'].split(';')[0].split(':')[1].strip().replace('px', ''))
                left = int(div['style'].split(';')[1].split(':')[1].strip().replace('px', ''))
                width = int(div['style'].split(';')[2].split(':')[1].strip().replace('px', ''))
                height = int(div['style'].split(';')[3].split(':')[1].strip().replace('px', ''))

                # total_width = 869
                # total_height = 1373

            rectangles = []
            for i, div in enumerate(div_elements):
                top = int(div['style'].split(';')[0].split(':')[1].strip().replace('px', '')) * image_height / total_height
                left = int(div['style'].split(';')[1].split(':')[1].strip().replace('px', '')) * image_width / total_width
                width = int(div['style'].split(';')[2].split(':')[1].strip().replace('px', '')) * image_width / total_width
                height = int(div['style'].split(';')[3].split(':')[1].strip().replace('px', '')) * image_height / total_height

                cropped_image = image.crop((left, top, left + width, top + height))
                cropped_image.save(os.path.join(output_directory, f"article_{img_page_id}_{i+1}.jpg"))

                rectangles.append((left, top, left + width, top + height))

            draw = ImageDraw.Draw(image)

            for rect in rectangles:
                draw.rectangle(rect, outline="red")
            
            image.save(os.path.join(output_directory, f"output_image_{img_page_id}.jpg"))

            print("Total Width:", total_width)
            print("Total Height:", total_height)
        else:
            # print(f"Image with page_id {img_page_id} not found")
            pass

     
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
    wait_until_visible("article_list_date_mobile")
    paper_date_element = driver.find_element_by_id("article_list_date_mobile")
    paper_date = paper_date_element.text
    time.sleep(0.2)
    if not compare_dates(paper_date, f"{month}/{day}/{year}"):
        try:
            load_paper(year, month, day)
        except Exception as e:
            print(f"{e}\nAccess denied for {day}-{month}-{year}: Possible subscription/login issue.\nPlease check if you're logged in or have valid subscription.")
    while(1):
        try:
            paper_date_element = driver.find_element_by_id("article_list_date_mobile")
            paper_date = paper_date_element.text
            # print("waiting")
            time.sleep(0.2)
            if compare_dates(paper_date, f"{month}/{day}/{year}"):
                print(paper_date)
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
        
    prev_orgid_values = None
    for i in range(1, num_pages + 1):
        folder_path = f"downloaded_articles/prothomalo/{year}/{month}/{day}/page_{i}"
        
        if i != 1:
            next_page_script = """
                if (IsImageCropping == '1')
                    removeCrop();

                prevPageFlag = 0;
                nextPageFlag = 1;
                var cur_pg = $("#div_flipbook").turn("page");
                var pagename = $(this).siblings('p').text();
                var item = $("#div_flipbook").find("div.turn-page-wrapper").find("div.turn-page.p" + ((cur_pg) + (1))).find("img.img_jpg");
                var pageId = $(item).attr('page_id');
                var sequence = $("#pg_id_" + pageId).attr('sequence');
                var _pageNo = $("#pg_id_" + pageId).attr('pageno');
                _pgCount = $("#pg_id_" + pageId).attr('paywallpage');
                if (showSignInWall(sequence, _pageNo)) {
                    if (!validateToken()) {
                    return false;
                    }
                } else if (checkNthPageCount(sequence, _pageNo)) {
                    if (!validateSubForNthPage()) {
                    return false;
                    }
                }
                $("#div_flipbook").turn("next");

                var cur_pg = $("#div_flipbook").turn("page");
                if (totalpages == cur_pg) {
                    $(".nextpage").hide();
                } else {
                    $(".nextpage").show();
                }
                
                """
            driver.execute_script(next_page_script)
        
        gen_prompt(f"Accessed page: {i}")
        page_wrapper_elements = driver.find_elements_by_class_name("turn-page-wrapper")
        dom_page_num = []
        for page_wrapper_element in page_wrapper_elements:
            if page_wrapper_element.value_of_css_property("display") != "none":
                dom_page_num.append(page_wrapper_element.get_attribute("page"))
        dom_page_num = str(dom_page_num[:1])
        print(dom_page_num)

        count = 0
        while True:
            try:
                orgid_elements = driver.find_elements_by_class_name("pagerectangle")
                orgid_values = []
                for element in orgid_elements:
                    orgid = element.get_attribute("orgid")
                    orgid_values.append(orgid)
                count += 1
                # print(orgid_values)
                if count > 300:
                    break
                if not orgid_values == prev_orgid_values:
                    print(orgid_values)
                    page_html = driver.page_source
                    
                    # with open("test.html", "w", encoding="utf-8") as file:
                    #     file.write(page_html)

                    # print("HTML content saved")
                    
                    # clean_html = retain_specific_classes(page_html, ['pagerectangle', 'img_jpg'])
                    # print("cleaned:", clean_html)
                    process_for_article_image(page_html, "cropped_images")
                    
                    break
            except StaleElementReferenceException:
                # print("StaleElementReferenceException: Element reference is stale. Retrying...")
                continue
        prev_orgid_values = orgid_values
            
            # area_data_list = []
            # for area_tag in area_tags:
            #     data_mapid = area_tag.get_attribute('data-mapid')
            #     coords = area_tag.get_attribute('coords')
            #     area_data_list.append({'coords': coords, 'edition_id': edition_id, 'ed_map_id': data_mapid})
            # print("\nAPI params extracted. Making API requests...")
            
            # img_urls = await scrape_page(session, api_url, area_data_list)
            
            # download_images(img_urls, folder_path)
            # clear_last_lines(5)

    print(f"\nSuccess: Scraped JUGANTOR-{year}/{month}/{day} \n")

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
  

