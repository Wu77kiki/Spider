from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import requests
import time

BASE_URL = 'https://login3.scrape.center/login'
LOGIN_URL = urljoin(BASE_URL, '/api/login')
INDEX_URL = urljoin(BASE_URL, '/api/book')
USERNAME = 'admin'
PASSWORD = 'admin'


option = ChromeOptions()
option.add_argument('--headless')
browser = webdriver.Chrome(options=option)
browser.get(BASE_URL)
browser.find_element(By.CSS_SELECTOR,'input[type="text"]').send_keys(USERNAME)
browser.find_element(By.CSS_SELECTOR,'input[type="password"]').send_keys(PASSWORD)
browser.find_element(By.CSS_SELECTOR,'button[type="button"]').click()
time.sleep(10)

jwt_token = browser.execute_script("return sessionStorage.getItem('token');")
print(jwt_token)