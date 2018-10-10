# ！usr/bin/env python

__author__ = 'Camille'

import requests
import os
from bs4 import BeautifulSoup

from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument('headless')

browser = webdriver.Chrome("C:/Users/xinzha4/Downloads/chromedriver.exe", chrome_options=option)


def req_url():
    response = requests.get(
        'http://dongphim.net/movie/dien-hy-cong-luoc-story-of-yanxi-palace-2018_cEsXzQg9.html').content
    soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
    tags = soup.find_all('a', class_="movie-eps-item ")
    urls = []
    for tag in tags:
        urls.append(tag['href'])
    return urls


def download(url, file_path):
    for _u in url:
        print(_u)
        browser.get(_u)
        soup = BeautifulSoup(browser.page_source, 'html.parser', from_encoding='utf-8')
        _tags = soup.find_all('h1', class_='movie-title')
        title = ''
        for t in _tags:
            title = t.span.text[-3:].strip('')
        tags = soup.find_all('video', class_='clhvjs-tech')

        for tag in tags:
            videosrc = tag['src'].replace('amp;', '')
            r = requests.get(videosrc, stream=True)
            with open(file_path + '/' + title + '.mp4', "wb") as code:
                print('开始下载', file_path + '/' + title + '.mp4')
                code.write(r.content)


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return path
    else:
        print(path + ' 目录已存在')
        return path


if __name__ == '__main__':
    urls = req_url()
    path = 'C:/Users/xinzha4/PycharmProjects/Spider_video/mp4'
    file_path = mkdir(path)
    download(urls, file_path)
