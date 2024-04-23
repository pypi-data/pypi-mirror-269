import getopt
import sys

from spidersearch.element import element
from spidersearch.handler import resource
from spidersearch import spidersearch

from selenium.webdriver.common.by import By


def start(conf):
    url = conf.get('url', None)
    directory = conf.get('directory', None)
    if not url or not directory:
        raise Exception('parameter "-u(url)" and "-d(directory)" required. conf={}'.format(conf))

    download_option = resource.DownloadOption(
        download_now=True,
        directory=directory,
        name_property_option=element.PropertyOption(element.ElementTextExtractor(),
                                                    anchor_point=element.ElementAnchorPoint(By.CLASS_NAME,
                                                                                            'xgplayer-name')),
        source_property_option=element.PropertyOption(
            element.ElementAttrExtractor(attr_key='src')),
        with_name_prefix=True)
    spidersearch.ResourceSpider(url,
                                element.ElementAnchorPoint(By.TAG_NAME, 'audio'),
                                resource_handler=resource.ResourceHandler(download_option),
                                next_btn_anchor_point=element.ElementAnchorPoint(
                                    By.XPATH, "//a[contains(@href, 'javascript:xia()')]")) \
        .search()


def print_help():
    # For example: python3 demo/ychy_downloader.py -d /tmp/wyyj/ -u http://m.ychy.cc/play/6311-0-1.html
    print('python ychy_downloader.py -d <directory> -u <url>')


if __name__ == '__main__':
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'hd:u:')
    except getopt.GetoptError:
        sys.exit(1)

    conf = {}
    for opt, arg in opts:
        if opt == '-d':
            conf['directory'] = arg
        elif opt == '-u':
            conf['url'] = arg
        elif opt == '-h':
            print_help()
            sys.exit(0)

    start(conf)
