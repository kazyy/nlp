import sys
import pprint
import requests
import re
from bs4 import BeautifulSoup
import unicodedata
import cabochaparser as parser
from sklearn.feature_extraction.text import TfidfVectorizer


t = '''
2019.06.05

大人気定番シリーズからマルチケースのご紹介です♡

税込12,960円

ゴールドバーにお花、ストーン、リボンのモチーフが付いており、

カラーも沢山ご用意しておりますので、

ご自身にピッタリのものが見つかりますよ♡

マルチケースですので、中にはカード、コインなど何でも入れて頂けます!

裏はパスケースにもなっていますので、

一つ持っているととても便利です!

是非店頭にお越し下さいませ!

#人気
#定番
#カードケース
#ミニ財布
#パスケース
#コンパクト
#サマンサタバサプチチョイス
#コインケース
#サマンサタバサ
#サマンサ
#マルチケース
'''

t = unicodedata.normalize('NFKC', t)
t = t.replace('\n', '')
print(f'元データ{t}')
sentences, chunks, tokens = parser.parse(t)

pprint.pprint(sentences, width=128)
pprint.pprint(chunks, width=128)
pprint.pprint(tokens, width=128)
sys.exit(0)

res = requests.get('https://www.tennoji-mio.co.jp/products/')
m = re.search('<body(.*?)>(.+)</body>', res.text, re.S)
soup = BeautifulSoup(m.group(2), 'lxml')
links = soup.select('ul.shop_list li a')
if not links:
    print('HTML構造エラー')
    sys.exit(1)

for a in links:
    r = requests.get(a['href'])
    s = BeautifulSoup(r.text, 'html.parser')

    if not s.body.article:
        print('HTML構造エラー')
        continue

    t = s.body.article.get_text()
    t = unicodedata.normalize('NFKC', t)
    t = t.replace('\r', '')
    print(f'元データ{t}')
    sentences, chunks, tokens = parser.parse(t)

    print(sentences)
    print(chunks)
    print(tokens)
