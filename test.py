import requests
from bs4 import BeautifulSoup
response = requests.get('http://47.76.46.130/')
response.encoding = "utf-8"
soup=BeautifulSoup(response.text,'lxml')

print(soup.p)