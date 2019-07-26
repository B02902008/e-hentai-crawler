import configparser
from crawler.crawler import crawl_book


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini', 'utf-8')
    result, msg = crawl_book(config['PATH']['download_dir'], config['PATH']['e_hentai_url'])
    if result:
        print('Crawling successful.')
    else:
        print('Crawling failed due to: {}.'.format(msg))
    exit()
