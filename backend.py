# -*- encoding: utf-8 -*-
import collections as cl
import re

import requests
from bs4 import BeautifulSoup
#Функционал легко расширить за счет кликов по полям с книгами

class Site():
    def __init__(self, url):
        self.url = url
        self.name = re.findall('(\w+\.\w+)\/', url)[0]

    def parse(self):
        r = requests.get(self.url)
        r.encoding = 'utf-8'

        return BeautifulSoup(r.text, 'html.parser')

    def get_tags(self):
        # Возвращает авторов и названия книг под тегами
        # аргументы для поиска в супе определены в классах сайтов ниже
        soup = self.parse()
        container = soup.find(self.container_tag, attrs=self.container_attrs)
        taged_titles = container.find_all(self.title_tag, attrs=self.title_attrs)
        taged_authors = container.find_all(self.authors_tag, attrs=self.authors_attrs)

        return taged_authors, taged_titles

    def get_books_list(self):
        # Возвращает список записей в формате: (номер п.п). (имя(имена) автора(ов)) \n "(название книги)"
        if self.cashed_data:
            return self.cashed_data
        else:
            taged_authors, taged_titles = self.get_tags()
            head = 'Топ 100 книг по версии ' + self.name + ', проверяйте'
            books = [head]
            counter = range(len(taged_titles))
            for num, author, title in zip(counter, taged_authors, taged_titles):
                try:
                    title = title.get_text().strip()
                    author = author.get_text()
                    string = '{0}. {1} \n "{2}"'.format(num + 1, author, title)
                    books.append(string)
                except AttributeError:
                    # Исключения поднимутся в случаях, когда в результате парсинга некоторые элементы будут не типа Tag
                    # В этом случае предусмотрено поведение для типов str и list, которые появятся в списке тегов, если автора нет или их несколько
                    if isinstance(author, str):
                        string = '{0}. {1} "{2}"'.format(num + 1, '-ошибка парсинга-', title)
                    elif isinstance(author, list):
                        authors = ', '.join(map(lambda x: x.get_text(), author)) # Сложна?
                        string = '{0}. {1} "{2}"'.format(num + 1, authors, title)
                        books.append(string)
            #в классы сайтов добавил аттрибут для кэша данных
            self.cashed_data = books

            return books


class LiveLib(Site):
    def __init__(self, url):
        Site.__init__(self, url)
        self.container_tag, self.container_attrs = 'table', {'class': "linear-list"}
        self.title_tag, self.title_attrs = 'a', {'class': "tag-book-title"}
        self.authors_tag, self.authors_attrs = 'a', {'class': 'tag-book-author'}
        self.cashed_data = []

class ReadRate(Site):
    def __init__(self, url):
        Site.__init__(self, url)
        self.container_tag, self.container_attrs = 'div', {'class': "books-list"}
        self.title_tag, self.title_attrs = 'div', {'class': "title"}
        self.authors_tag, self.authors_attrs = 'li', {'class': 'contributor item'}
        self.cashed_data = []

class Libs(Site):
    def __init__(self, url):
        Site.__init__(self, url)
        self.container_tag, self.container_attrs = 'div', {'class': "posts doocode_book_result_filter"}
        self.title_tag, self.title_attrs = 'h2', {}
        self.authors_tag, self.authors_attrs = 'a', {'href': re.compile('/a/*')}
        self.cashed_data = []

    def get_tags(self):
        taged_titles, taged_authors = Site.get_tags(self)
        taged_authors.insert(26, 'Error') # в книге под номером 26 не указан автор Мариам Петросян, но никого это не волнует

        return taged_authors, taged_titles


class Readly(Site):
    def __init__(self, url):
        Site.__init__(self, url)
        self.container_tag, self.container_attrs = 'div', {'class': 'book-list-view'}
        self.title_tag, self.title_attrs = 'h3', {'class': 'blvi__title'}
        self.authors_tag, self.authors_attrs = 'div', {'class': 'blvi__book_info'}
        self.cashed_data = []

    def get_tags(self):
        #Переопределяем функцию, ибо авторы перечислены в тегах, а не лежат в отдельном объекте
        book_infos, taged_titles = Site.get_tags(self)
        taged_authors = []

        for book in book_infos:
            temp = book.find_all('a', href=re.compile('/author/*'))
            if len(temp) == 1:
                taged_authors += temp
            else:
                taged_authors.append(temp)

        return taged_authors, taged_titles

#Ниже - спорное решение, оптимизируйте =)

LL = 'http://www.livelib.ru/books/top'
RR = 'http://readrate.com/rus/ratings/top100'
L = 'http://libs.ru/best-100'
R = 'http://readly.ru/books/top'
urls = [LL, RR, L, R]
cashed_data = {}

livelib = LiveLib(LL)
readrate = ReadRate(RR)
libs = Libs(L)
readly = Readly(R)

sites = {'LiveLib': livelib,
         'ReadRate': readrate,
         'Libs': libs,
         'Readly': readly
         }
#readly.get_books_list() #для тестов удобно