# -*- encoding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup

target_url = "http://www.livelib.ru/books/top"

r = requests.get(target_url)
r.encoding = 'utf-8'

soup = BeautifulSoup(r.text,  "html.parser")
top_titles = soup.find_all("a", class_="tag-book-title")

with open('output.txt','w',encoding='utf8') as f:
	