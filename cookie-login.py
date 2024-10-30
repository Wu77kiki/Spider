from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import requests
import time

BASE_URL='https://login2.scrape.center/'
LOGIN_URL =urljoin(BASE_URL,'/login')
INDEX_URL = urljoin(BASE_URL,'/page/1')
USERNAME ='admin'
PASSWORD='admin'

option = ChromeOptions()
option.add_argument('--headless')
browser = webdriver.Chrome(options=option)
browser.get(BASE_URL)
browser.find_element(By.CSS_SELECTOR,'input[name="username"]').send_keys(USERNAME)
browser.find_element(By.CSS_SELECTOR,'input[name="password"]').send_keys(PASSWORD)
browser.find_element(By.CSS_SELECTOR,'input[type="submit"]').click()
time.sleep(10)

cookies=browser.get_cookies()
print('Cookies',cookies)
browser.close()

session=requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'],cookie['value'])
responese_index=session.get(INDEX_URL)
print('Response Status',responese_index.status_code)
print('Response URL',responese_index.url)