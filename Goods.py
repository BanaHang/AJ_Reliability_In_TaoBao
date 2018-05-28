# 商品类，用来爬取商品
# Coded by ShiHang

import Comments
import re
import ResponseText
from bs4 import BeautifulSoup

class Goods:
    def __init__(self, goodsid):
        self.ID = goodsid       # 商品ID
        self.comment = Comments.Comment(self.ID)
        self.ShopID = ""        # 商品从属店铺ID
        self.url = "https://item.taobao.com/item.htm?id=" + self.ID + "&abbucket=10"

    def getAttrs(self):      # 抓商品的属性。。。。。。其实就爬了个所属店铺的ID
        RT = ResponseText.ResponseText(self.url)
        text = RT.getText()

        soup = BeautifulSoup(text, 'lxml')
        lists = soup.find_all("meta", attrs={'name': 'microscope-data'})

        pattern_1 = re.compile(r"shopId=\d+;")
        sid = pattern_1.findall(str(lists[0]))
        pattern_2 = re.compile(r"\d+")
        shopid = pattern_2.search(str(sid[0])).group()

        self.ShopID = shopid
        return

