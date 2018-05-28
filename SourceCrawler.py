# 源页面资源爬取
# Coded by ShiHang

import ResponseText
import re


class SourceCrawler:
    def __init__(self, keywords, offset):
        # keywords即搜索商品的关键词；offset即起始商品偏移量，一页显示二十个商品
        self.url = "https://shopsearch.taobao.com/search?app=shopsearch&q=" + keywords + "&js=1&initiative_id=staobaoz_20180526&ie=utf8&s=" + offset


    def scrape(self):       # 爬取初始页的相关商品ID
        RT = ResponseText.ResponseText(self.url)
        text = RT.getText()

        pattern = re.compile(r'"nid":"\d+","picUrl"')
        lists = pattern.findall(text)

        pattern_2 = re.compile(r'\d+')
        nid_list = list()       # 返回商品的ID的list
        for li in lists:
            nid_list.append(pattern_2.search(li).group())

        return nid_list
