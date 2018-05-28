# 为了不重复造轮子，写了这个类，看一下应该能知道是干嘛的。。。(｀・ω・´)
# Coded by ShiHang

import requests


class ResponseText:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        }


    def getText(self):
        response = requests.get(url=self.url, headers=self.headers)
        while response.text=="":
            response = requests.get(url=self.url, headers=self.headers)
        return response.text
