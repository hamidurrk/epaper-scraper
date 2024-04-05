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

load_element = driver.find_element_by_class_name("more")
prev_num_articles = 0
count = 0
while(1):
    link_elements = driver.find_elements_by_class_name("title-link")
    print(len(link_elements))
    num_articles = len(link_elements)
    if count >= 10:
        break
    if prev_num_articles == num_articles:
        count += 1
    else:
        load_element.click()
    prev_num_articles = num_articles