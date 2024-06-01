from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), service_args=['--marionette-port', '2828', '--connect-existing'], options=firefox_options)
base_url = f"https://epaper.prothomalo.com/Home/"
print(driver.current_url)    

target_url = "https://epaper.prothomalo.com/Home/DIndex"

if not target_url in driver.current_url:
    driver.get(base_url)
    