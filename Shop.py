# 店铺类
# Coded by ShiHang

import ResponseText
import re
from bs4 import BeautifulSoup

class Shop:
    def __init__(self, shopid):    # 初始化函数
        self.shopname = ''      # 店铺名称
        self.shopID = shopid    # 店铺ID
        self.shopURL = ''       # 店铺链接
        self.score = 0          # 店铺可信度评分


    def Reliablity_Score(self):     # 计算可信度得分
        score = 100             # 计算得分
        self.score = score      # 赋分
        return


    def getParams(self):
        self.shopURL = "https://shop" + self.shopID + ".taobao.com/"

        RT = ResponseText.ResponseText(self.shopURL)
        text = RT.getText()

        soup = BeautifulSoup(text, 'lxml')
        result = soup.find_all('title')

        pattern = re.compile("-(.*)-")
        name = pattern.search(str(result[0]))
        self.shopname = name.group()
        return
