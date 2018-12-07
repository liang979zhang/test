import os

import requests

path = 'E:\妹子图\image'
url = 'http://www.meizitu.com/'


def test():
    r = requests.get(url)
    r.encoding = 'utf-8'
    print(r.text)


if __name__ == '__main__':
    if not os.path.exists(path):
        os.mkdir(path)
    test()
