# -*- encoding: utf-8 -*-
import requests
import sys
from bs4 import BeautifulSoup

try:
	target_url = sys.argv[1][1:]
except IndexError:
	target_url = "http://www.livelib.ru/books/top"
request = requests.get(target_url)
request.encoding = 'utf-8'

soup = BeautifulSoup(request.text, "html.parser")
top_titles = soup.find_all("a", class_="tag-book-title")

with open('output.txt','w',encoding='utf8') as f:
    for line in top_titles:
        f.write(line.get_text() + '\n')
