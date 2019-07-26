import os
import sys
from crawler import util
from bs4 import BeautifulSoup


def create_viewer(base: str, title: str, num: int):
    """Return nothing

    :param base: the base directory
    :param title: the book title
    :param num: the number of images
    :return: no return value
    """
    path = os.path.join(base, 'viewer.html')
    with open(path, 'w') as f:
        f.write('<html><head><title>{}</title></head><body>'.format(title))
        for i in range(num):
            f.write('<img src="./{}.jpg">'.format(i))
        f.write('</body></html>')


def crawl_page(base: str, soup: BeautifulSoup) -> int:
    """Return an integer

    :param base: 
    :param soup: the beautiful soup of the target page
    :return: return the max page number of downloaded image
    """
    max_index = 0
    images = soup.find_all('div', attrs={'class': 'gdtm'})
    for image in images:
        if image.find('a') is None or image.find('a').get('href') is None:
            continue
        link = image.find('a').get('href')
        index = link.split('-')[-1]
        print('Getting image {} ...'.format(index))
        if util.download_image(base, index, link):
            max_index = max(max_index, int(index))
    return max_index


def crawl_book(dist: str, url: str) -> (bool, str):
    """Return a 2-tuple (boolean, string)

    Crawling steps:
    1. Check the download destination
    2. Get the home page of the book, and extract title and page tabs
    3. Create the directory for the book
    4. Get each page of the book
    5. Get each image of each page
    6. Create HTML viewer

    :param dist: the download destination directory
    :param url: the e-hentai url to download
    :return: whether the crawling succeed, and error message if failed
    """
    # Step 1
    if not os.path.exists(dist) or not os.path.isdir(dist):
        return False, 'The download destination is not a directory'

    # Step 2
    home_soup = util.get_html_soup(url)
    try:
        title = home_soup.find(id='gj').text
        pagetabs = home_soup.find('table', attrs={'class': 'ptt'}).find_all('td')[2:-1]
    except (AttributeError, IndexError):
        return False, 'Not a valid e-hentai url'

    # Step 3
    title = title.replace('/', ' ')
    print('Crawl e-hentai book {}.'.format(title))
    path = os.path.join(dist, title)
    if not util.create_dir(path):
        return False, 'Failed to create directory for book'

    # Step 4
    pages = [home_soup]
    for pagetab in pagetabs:
        if pagetab.find('a') is None or pagetab.find('a').get('href') is None:
            continue
        link = pagetab.find('a').get('href')
        print('Getting page {} ...'.format(int(link.split('=')[-1]) + 1))
        pages.append(util.get_html_soup(link))

    # Step 5
    max_page = 0
    for page in pages:
        max_page = max(max_page, crawl_page(path, page))

    # Step 6
    create_viewer(path, title, max_page)

    return True, ''


if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit()
    crawl_book(sys.argv[1], sys.argv[2])
    exit()
