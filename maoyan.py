#!usr/bin/env python
# coding=utf-8

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import json


def get_current_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except RequestException:
        return None


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    dd = soup.select('dd')
    for result in dd:
        yield {
            'index': result.select_one('.board-index').text,
            'title': result.select_one('.image-link')['title'],
            'image': result.select_one('.poster-default')['src'],
            'star': result.select_one('.star').text.strip(),
            'realeasetime': result.select_one('.releasetime').text.strip(),
            'score': result.select_one('.integer').text + result.select_one('.fraction').text
        }


def save_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset * 10)
    html = get_current_page(url)
    for result in parse_html(html):
        print(result)
        save_to_file(result)


if __name__ == '__main__':
    depth = 10
    for i in range(depth):
        main(i)
