from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
from urllib.parse import urljoin
from os import makedirs
from os.path import exists
from selenium.webdriver import ChromeOptions
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://spa2.scrape.center/page/{page}'
TIMEOUT = 10
TOTAL_PAGE = 10
option = ChromeOptions()
option.add_argument('--headless')
browser = webdriver.Chrome(options=option)
wait = WebDriverWait(browser, TIMEOUT)

def scrape_page(url, condition, locator):
    logging.info('scraping %s', url)
    try:
        browser.get(url)
        wait.until(condition(locator))
    except TimeoutException:
        logging.error('error occurred while scraping %s', url, exc_info=True)

def scrape_index(page):
    url = INDEX_URL.format(page=page)
    scrape_page(url, condition=EC.visibility_of_all_elements_located,
                locator=(By.CSS_SELECTOR, '#index .item'))
    
def parse_index():
    elements = browser.find_elements(By.CSS_SELECTOR,'#index .item .name')
    for element in elements:
        href = element.get_attribute('href')
        yield urljoin(INDEX_URL, href)

def scrape_detail(url):
    scrape_page(url, condition=EC.visibility_of_element_located,
                locator=(By.TAG_NAME, 'h2'))
    
def parse_detail():
    url = browser.current_url
    name = browser.find_element(By.TAG_NAME,'h2').text
    categories = [element.text for element in browser.find_elements(By.CSS_SELECTOR,'.categories button span')]
    cover = browser.find_element(By.CSS_SELECTOR,'.cover').get_attribute('src')
    score = browser.find_element(By.CLASS_NAME,'score').text
    drama = browser.find_element(By.CSS_SELECTOR,'.drama p').text
    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': score,
        'drama': drama
    }
   
def main():
    try:
        for page in range(1, TOTAL_PAGE + 1):
            scrape_index(page)
            detail_urls = parse_index()
            for detail_url in list(detail_urls):
                logging.info('get detail url %s', detail_url)
                scrape_detail(detail_url)
                detail_data = parse_detail()
                logging.info('detail data %s', detail_data)
    finally:
        browser.close()

main()