import os
import sys
from crawler import util


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
            f.write('<img src="./{}.jpg">'.format(i + 1))
        f.write('</body></html>')


def crawl_next_page(url: str) -> (str, str):
    """Return a 2-tuple (string, string)

    :param url: the image page url
    :return: the image source url and the next image page url
    """
    soup = util.get_html_soup(url)
    try:
        image_url = soup.find(id='i3').a.img.get('src')
        next_page = soup.find(id='i3').a.get('href')
    except AttributeError:
        return '', ''
    return image_url if image_url is not None else '', next_page if next_page is not None else ''


def crawl_book(dist: str, url: str) -> (bool, str):
    """Return a 2-tuple (boolean, string)

    Crawling steps:
    1. Check the download destination
    2. Get the home page of the book, and extract title, total pages, and url to first page
    3. Create the directory for the book
    4. Get each page of the book
    5. Create HTML viewer

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
        infos = home_soup.find(id='gdd').table.find_all('td', attrs={'class': 'gdt2'})
        pages = int([info.text.split()[0] for info in infos if 'page' in info.text][0])
        first = home_soup.find('div', attrs={'class': 'gdtm'})
    except (AttributeError, IndexError, TypeError):
        return False, 'Not a valid e-hentai url'

    # Step 3
    title = title.replace('/', ' ')
    print('Crawl e-hentai book {}.'.format(title))
    path = os.path.join(dist, title)
    if not util.create_dir(path):
        return False, 'Failed to create directory for book'

    # Step 4
    link = first.div.a.get('href')
    for i in range(pages):
        img, link = crawl_next_page(link)
        print('Download image {}.'.format(i + 1))
        util.download_image(path, str(i + 1), img)

    # Step 5
    create_viewer(path, title, pages)

    return True, ''


if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit()
    crawl_book(sys.argv[1], sys.argv[2])
    exit()
