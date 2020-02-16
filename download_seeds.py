# coding=utf-8


"""
    date: 2020-02-16

    说明:
    下载种子
    遍历每个分类
    然后遍历每个分类
    保存具体的项目
"""

import os
import time
import requests
from lxml import etree


# config

"""
代理的示例:
    PROXIES = {
            "http": "xxxxxxxxxxxxx",
            "https": "xxxxxxxxxxxxx",
        }
如果有代理，这里将 PROXIES 改为自己的代理
"""
PROXIES = None

# main uri
MAIN_URI = 'https://96ii.net'

# file
SEEDS_LIST = './seeds_list.txt'

IMAGE_LIST = './image_list.txt'

#  url链接
URL_DICT = {
    'luyilu': 'https://96ii.net/luyilu/list_5_{}.html',                 # 撸一撸
    'meiyanshe': 'https://96ii.net/meiyanshe/list_13_{}.html',          # 魅妍社
    'AISSaisi': 'https://96ii.net/AISSaisi/list_9_{}.html',             # 爱丝
    'youguo': 'https://96ii.net/youguowang/list_3_{}.html',             # 尤果
    'meiyuanguan': 'https://96ii.net/meiyuanguan/list_2_{}.html',       # 美媛馆
    'tuinvlang': 'https://96ii.net/tuinvlang/list_1_{}.html',           # 推女郎
}

# referer
REFERER = 'https://96ii.net/{}/'

# headers
HEADERS = {
    'Host': '96ii.net',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Wed, 24 Jul 2019 15:01:15 GMT',
    'if-none-match': 'W/"84cac2a33042d51:0"',
    'referer': 'https://96ii.net/tuinvlang/',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}


def get_all_categories():
    """
    遍历每个分类里的找到所有的集合
    """
    for item, link in URL_DICT.items():
        if not os.path.exists('./{}'.format(item)):
            # 按照每个分类创建文件夹
            os.mkdir('./{}'.format(item))
        get_all_pages(item, link)


def get_all_pages(item, link):
    referer = REFERER.format(item)
    HEADERS.update({'referer': referer})
    start = 1
    while True:
        url = link.format(start)
        print('当前{}\t第\t{}\t页'.format(item, start))
        html = request_url(url)
        if html:
            next_page = parse_items(html, item)
            if not next_page:
                break
        start += 1
        time.sleep(3)


def request_url(url):
    retry = 3
    html = None
    while retry > 0:
        try:
            resp = requests.get(url=url, headers=HEADERS, proxies=PROXIES, timeout=15) \
                if PROXIES \
                else requests.get(url=url, headers=HEADERS, timeout=15)
            if resp.status_code < 300:
                html = resp.content.decode('gbk')
                break
        except Exception as e:
            print('请求出错\t{}'.format(e))
            time.sleep(5)
        retry -= 1
    return html


def parse_items(html, item):
    has_next_page = True
    selector = etree.HTML(html)
    items_list = selector.xpath('//article[@class="excerpt excerpt-one"]')
    for each in items_list:
        title = each.xpath('header/h2/a/@title')[0]
        uri = each.xpath('header/h2/a/@href')[0]
        with open(SEEDS_LIST, 'a', encoding='utf-8') as f:
            f.write('{}\u0001{}\u0001{}'.format(item, title, uri) + '\n')
    # 找到下一页
    next_page = selector.xpath('//div[@class="pagination pagination-multi"]/ul/li[@class="next-page"]')
    if not next_page:
        has_next_page = False
    return has_next_page


def get_all_image_url():
    """请求每一个链接，然后获取其内容的url"""
    n = 1
    for i in seed_generator():
        print(n)
        get_image_url(i)
        n += 1


def get_image_url(seed):
    url = ''.join([MAIN_URI, seed[-1]])
    uri = seed[-1].split('.')
    uri = ''.join([uri[0] + '_{}.', uri[1]])
    start = 1
    while True:
        print('当前\t{}\t第\t{}\t页'.format(seed[1], start))
        if start != 1:
            url = ''.join([MAIN_URI, uri.format(start)])
        html = request_url(url)
        if html:
            next_page = parse_image_url(html, seed)
            if not next_page:
                break
        start += 1
        time.sleep(1)


def seed_generator():
    for i in open(SEEDS_LIST, 'r', encoding='utf-8'):
        yield i.strip().split('\u0001')


def parse_image_url(html, seed):
    has_next_page = True
    selector = etree.HTML(html)
    image_list = selector.xpath('//article[@class="article-content"]/p/img')
    for each in image_list:
        url = each.xpath('@src')
        with open(IMAGE_LIST, 'a', encoding='utf-8') as f:
            f.write('{}\u0001{}\u0001{}\n'.format(seed[0], seed[1], url))
    # 找到下一页
    next_page = selector.xpath('//div[@class="pagination pagination-multi"]/ul/li[@class="next-page"]')
    if not next_page:
        has_next_page = False
    return has_next_page


if __name__ == '__main__':
    # 先遍历所有的类别
    get_all_categories()
    # 找到每个类别拥有的图片
    get_all_image_url()
