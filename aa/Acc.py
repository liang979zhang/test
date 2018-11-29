import os
import threading  # 多线程模块
import re  # 正则表达式模块
import time  # 时间模块

import requests

all_urls = []  # 头地址存放列表
all_img_urls = []  # 图片列表页面的数组
g_lock = threading.Lock()  # 初始化一个锁
pic_links = []  # 图片地址列表


# 消费者  获取每个子界面里的具体的图片地址
class Consumer(threading.Thread):
    def run(self):
        global all_img_urls
        print("%s is running " % threading.current_thread)
        while len(all_img_urls) > 0:
            g_lock.acquire()  # 在访问all_urls的时候，需要使用锁机制
            img_url = all_img_urls.pop()
            g_lock.release()
            try:
                response = requests.get(img_url)
                response.encoding = 'gb2312'  # 由于我们调用的页面编码是GB2312，所以需要设置一下编码
                title = re.search('<title>(.*?) | 妹子图</title>', response.text).group(1)
                all_pic_src = re.findall('<img alt=.*?src="(.*?)" /><br />', response.text, re.S)
                print(all_pic_src)
                pic_dict = {title: all_pic_src}  # python字典
                global pic_links
                g_lock.acquire()
                pic_links.append(pic_dict)  # 字典数组
                # print(title + " 获取成功")
                g_lock.release()

            except:
                pass
            time.sleep(0.5)


# 生产者，负责从每个页面提取图片列表链接
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
                global all_img_urls
                g_lock.acquire()  # 这里还有一个锁
                all_img_urls += all_pic_link  # 这个地方注意数组的拼接，没有用append直接用的+=也算是python的一个新语法吧
                # print(all_img_urls)
                g_lock.release()  # 释放锁
                time.sleep(0.5)

            except:
                pass
        time.sleep(0.5)


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


class DownPic(threading.Thread):
    def run(self):
        while True:
            global pic_links
            # 上锁
            g_lock.acquire()
            if len(pic_links)==0:
                # 不管什么情况，都要释放锁
                g_lock.release()
                continue

            else:
                pic = pic_links.pop()
                g_lock.release()
                # 遍历字典列表
                for key, values in pic.items():
                    path = key.rstrip("\\")
                    is_exists = os.path.exists(path)
                    # 判断结果
                    if not is_exists:
                        # 如果不存在则创建目录
                        # 创建目录操作函数
                        os.makedirs(path)

                        print(path + '目录创建成功')

                    else:
                        # 如果目录存在则不创建，并提示目录已存在
                        print(path + ' 目录已存在')
                    for pic in values:
                        filename = path + "/" + pic.split('/')[-1]
                        if os.path.exists(filename):
                            continue
                        else:
                            try:
                                response = requests.get(pic)
                                with open(filename, 'wb') as f:
                                    f.write(response.content)
                                    f.close
                            except Exception as e:
                                print(e)
                                pass



# 入口
if __name__ == "__main__":
    # run()
    target_url = 'http://www.meizitu.com/a/pure_%d.html'
    spider = Spider(target_url)
    spider.getUrls(1, 16)
    print(len(all_urls))
    threads = []
    for x in range(2):
        t = Producer()
        t.start()
        threads.append(t)

    for tt in threads:
        tt.join()

    #     # 开启10个线程去获取链接
    for x in range(10):
        ta = Consumer()
        ta.start()
