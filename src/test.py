import requests
import re
from bs4 import BeautifulSoup
from re import RegexFlag
from builtins import exit


res = requests.get('https://www.tennoji-mio.co.jp/products/')
m = re.search('<body(.*?)>(.+)</body>', res.text, flags = RegexFlag.MULTILINE|RegexFlag.DOTALL)
soup = BeautifulSoup(m.group(2), 'html.parser')
links = soup.select('ul.shop_list li a')
if not links:
    print('HTML構造エラー')
    exit

for a in links:
    r = requests.get(a['href'])
    s = BeautifulSoup(r.text, 'html.parser')

    if not s.body.article:
        print('HTML構造エラー')
        continue

    print(s.body.article.get_text())
