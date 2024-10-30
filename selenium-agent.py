from selenium import webdriver
proxy='133.18.234.13:80'
options =webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--proxy-server=http://'+ proxy)
browser =webdriver.Chrome(options=options)
browser.get('http://www.httpbin.org/get')
# browser.get('http://47.76.46.130/')
print(browser.page_source)
browser.close()
