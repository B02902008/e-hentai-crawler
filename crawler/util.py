import os
import time
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def download_image(base: str, num: str, url: str) -> bool:
    """Return a boolean

    :param base: the download destination directory
    :param num: index of the the image
    :param url: the image page url
    :return: whether the download succeed
    """
    soup = get_html_soup(url)
    try:
        link = soup.find(id='img').get('src')
    except AttributeError:
        return False
    request.urlretrieve(link, os.path.join(base, '{}.jpg'.format(num)))
    return True


def create_dir(path: str) -> bool:
    """Return a boolean

    :param path: the new directory name
    :return: whether the creation succeed
    """
    if os.path.exists(path) and os.path.isdir(path):
        return True
    try:
        os.mkdir(path)
    except OSError:
        return False
    return True


def get_html_soup(url: str) -> BeautifulSoup:
    """Return a BeautifulSoup object

    :param url: the query URL
    :return: the parsed content in BeautifulSoup if receive 200, else an empty BeautifulSoup
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=url, headers=headers)
    try:
        response = request.urlopen(req)
    except HTTPError:
        time.sleep(5)
        response = request.urlopen(req)
    if response.getcode() != 200:
        return BeautifulSoup('', 'html5lib')
    return BeautifulSoup(response.read().decode('utf-8'), 'html5lib')


if __name__ == '__main__':
    exit()