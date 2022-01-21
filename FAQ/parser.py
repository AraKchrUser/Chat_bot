from bs4 import BeautifulSoup
import requests


url = 'https://habr.com/ru/post/544828/'
page = requests.get(url)
if page.status_code == 200:
    print('200 ok')
else:
    print('no ok')
