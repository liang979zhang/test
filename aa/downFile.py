import requests


def run():
    response = requests.get("http://www.newsimg.cn/big201710leaderreports/xibdj20171030.jpg")
    with open("C:/Users/Public/Pictures/xijinping.jpg", "wb") as f:
        f.write(response.content)
        f.close


if __name__ == '__main__':
    run()
