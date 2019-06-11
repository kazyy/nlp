import sys
import requests
from bs4 import BeautifulSoup
from datastore import Datastore

res = requests.get('https://www.tennoji-mio.co.jp/products/')
soup = BeautifulSoup(res.text, 'lxml')
links = soup.select('ul.shop_list li a')
if not links:
    print('HTML構造エラー')
    sys.exit(1)

with Datastore() as d:
    for a in links:
        r = requests.get(a['href'])
        s = BeautifulSoup(r.text, 'lxml')

        if not s.body.article:
            print('HTML構造エラー')
            continue

        content = s.body.article.get_text()
        d.save(a['href'], content)
