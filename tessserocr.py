import time
import re
import tesserocr
from selenium import webdriver
from io import BytesIO
from PIL import Image
from retrying import retry
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import numpy as np
from selenium.webdriver import ChromeOptions

def preprocess(image):
    image = image.convert('L')
    array = np.array(image)
    array = np.where(array > 50, 255, 0)
    image = Image.fromarray(array.astype('uint8'))
    return image


@retry(stop_max_attempt_number=10, retry_on_result=lambda x: x is False)
def login():
    browser.get('https://captcha7.scrape.center/')
    browser.get_screenshot_as_file('try_to_login.png')
    browser.find_element(By.CSS_SELECTOR,'.username input[type="text"]').send_keys('admin')
    browser.find_element(By.CSS_SELECTOR,'.password input[type="password"]').send_keys('admin')
    captcha = browser.find_element(By.CSS_SELECTOR,'#captcha')
    image = Image.open(BytesIO(captcha.screenshot_as_png))
    image = preprocess(image)
    captcha = tesserocr.image_to_text(image)
    captcha = re.sub('[^A-Za-z0-9]', '', captcha)
    browser.find_element(By.CSS_SELECTOR,'.captcha input[type="text"]').send_keys(captcha)
    browser.find_element(By.CSS_SELECTOR,'.login').click()
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[contains(., "登录成功")]')))
        browser.get_screenshot_as_file('sucessful_login.png')
        time.sleep(10)
        browser.close()
        return True
    except TimeoutException:
        return False


if __name__ == '__main__':
    option = ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(options=option)
    login()