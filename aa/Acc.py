import threading  # 多线程模块
import re  # 正则表达式模块
import time  # 时间模块

import requests

all_urls = []  # 头地址存放列表
all_img_urls = []  # 图片列表页面的数组
g_lock = threading.Lock()  # 初始化一个锁


class Producer(threading.Thread):
    def run(self):
        global all_urls
        while len(all_urls) > 0:  # 因为下面all_urls 使用一个移除一个,所以以all_urls的长度做循环条件
            g_lock.acquire()  # 在访问all_urls的时候，需要使用锁机制
            page_url = all_urls.pop()  # 获取列表最后一个地址并删除这一地址
            g_lock.release()  # 使用完成之后及时把锁给释放，方便其他线程使用
            try:
                print("分析" + page_url)
                response = requests.get(page_url)
                all_pic_link = re.findall('<a target=\'_blank\' href="(.*?)">', response.text, re.S)


            except:
                pass


# 拼接 图片地址
class Spider():
    def __init__(self, target_url):
        self.target_url = target_url

    def getUrls(self, start_page, page_num):
        global all_urls
        for i in range(start_page, page_num + 1):
            url = self.target_url % i
            all_urls.append(url)


# 下载图片
def run():
    response = requests.get("http://www.baidu.com")
    response.encoding = "utf-8"
    print(response.text)


# 入口
if __name__ == "__main__":
    # run()
    target_url = 'http://www.meizitu.com/a/pure_%d.html'
    spider = Spider(target_url)
    spider.getUrls(1, 16)
    print(all_urls)
