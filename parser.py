# -*- encoding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

target_url = "http://www.livelib.ru/books/top"

request = requests.get(target_url)
request.encoding = 'utf-8'

soup = BeautifulSoup(request.text, "html.parser")
top_titles = soup.find_all("a", class_="tag-book-title")

with open('output.txt', 'w', encoding='utf8') as f:
    for book in list(top_titles):
        book = str(book)
        f.write(book[(book[:-4].index('>')+1):-4]+"\n")
    f.close()
