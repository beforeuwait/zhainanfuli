# coding=utf-8

"""
    date: 2020-02-16

    说明:
    下载所有的图片
    这里用到多进程
"""

import os
import requests
from multiprocessing import Pool


# proxies
"""
代理的示例:
    PROXIES = {
            "http": "xxxxxxxxxxxxx",
            "https": "xxxxxxxxxxxxx",
        }
如果有代理，这里将 PROXIES 改为自己的代理
"""
PROXIES = None

# file
IMAGE_LIST = './image_list.txt'

# headers
HEADERS = {
    'Host': 'www.images.96xxpic.com:8819',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Sat, 15 Feb 2020 07:01:22 GMT',
    'if-none-match': '6a4d25bbcde3d51:0',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

# Pool 进程数
POOL = 10


def image_list_generator():
    for i in open(IMAGE_LIST, 'r', encoding='utf-8'):
        yield i.strip().split('\u0001')


def downloader():
    pool = Pool(POOL) 
    for i in image_list_generator():
        if not os.path.exists('./{}/{}'.format(i[0], i[1])):
            os.mkdir('./{}/{}'.format(i[0], i[1]))
        pool.apply_async(download_img, (i,))
    pool.close()
    pool.join()


def check_existed_image(path):
    is_ok = False
    if os.path.exists(path):
        print('已存在:\t', path)
        with open(path, 'rb') as f:
            ctx = f.read()
            if ctx.endswith(b'\xd9'):
                is_ok = True
    return is_ok


def check_download_image(ctx):
    return ctx.endswith(b'\xd9')


def download_img(info):
    cate = info[0]
    title = info[1]
    url = info[2]
    name = info[2].split('-')[1]
    is_existed = check_existed_image('./{}/{}/{}'.format(cate, title, name))
    if not is_existed:
        retry = 3
        print('开始下载:\t', cate, title, name)
        while retry > 0:
            try:
                resp = requests.get(url=url, headers=HEADERS, proxies=PROXIES, timeout=10) \
                    if PROXIES \
                    else requests.get(url=url, headers=HEADERS, timeout=10)
                if resp.status_code < 300:
                    html = resp.content
                    if check_download_image(html):
                        # 保存图片
                        with open('./{}/{}/{}'.format(cate, title, name), 'wb') as f:
                            f.write(html)
                        break
            except Exception as e:
                print('请求出错\t{0}'.format(e))
            retry -= 1


if __name__ == '__main__':
    downloader()