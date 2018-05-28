# 评论类，用来爬取评论，以及评论的筛选等处理
# Coded by ShiHang

import json
import re
import math
import time
import ResponseText
from bs4 import BeautifulSoup


class Comment:
    def __init__(self, goodsid):
        self.goodsid = goodsid      # 评论从属商品的商品ID

        # 链接参数中，auctionNumId目测是商品ID，rateType是评价种类（1：好评，0：中评，-1：差评）
        self.rateUrl = "https://rate.taobao.com/feedRateList.htm?auctionNumId=" + self.goodsid + "&rateType=&pageSize=20&currentPageNum=1"

        self.rate = 0           # 评论总数
        self.effectrate = 0     # 有效评论数
        self.goodrate = 0       # 好评数
        self.normalrate = 0     # 中评数
        self.badrate = 0        # 差评数

        self.isTaoBao = False   # 判断该评论所属商品是否是淘宝店中的商品。因为发现天猫店的JSON格式和淘宝不同，所以暂时只处理淘宝的。
        self.score = 0          # 本商品的评论分析得分


    def ISTaoBao(self):             # 判断是否是淘宝店的商品
        url = "https://item.taobao.com/item.htm?id=" + self.goodsid + "&abbucket=10"

        RT = ResponseText.ResponseText(url)
        text = RT.getText()

        soup = BeautifulSoup(text, 'lxml')
        result = soup.find_all('link', attrs={'rel': 'canonical'})
        text = str(result[0])

        if text.find('taobao') > -1:
            self.isTaoBao = True
        else:
            self.isTaoBao = False
        return


    def getRateAmount(self):        # 获取评论总数
        RT = ResponseText.ResponseText(self.rateUrl)
        text = RT.getText()

        pattern_1 = re.compile('"total":\d+,')
        t = pattern_1.findall(text)
        pattern_2 = re.compile("\d+")
        rateamount = pattern_2.findall(t[0])
        self.rate = rateamount[0]
        return


    def ScrapeComments(self, commenturl):       # 用来初步抓取一页（20条评论），分析其中有效评论、好评差评中评数量，返回一个字典
        RT = ResponseText.ResponseText(commenturl)
        t = RT.getText()

        # 淘宝的这个ajax是真的恶心，这个json开头结尾用括号括起来。。。。。。(艹皿艹)
        left = t.index('(') + 1
        right = len(t) - 2
        t = t[left: right]
        json_text = json.loads(t, encoding="utf-8")

        # 这个字典用来储存评论的统计分类的结果
        rate_dic = {
            "effectrate": 0,
            "goodrate": 0,
            "normalrate": 0,
            "badrate": 0
        }

        effectrate = 0
        uneffectrate = 0
        goodrate = 0
        normalrate = 0
        badrate = 0

        for li in json_text["comments"]:
            if li["user"]["vipLevel"] >= 3:
                effectrate += 1
                if int(li["rate"]) == 1:
                    goodrate += 1
                elif int(li["rate"]) == 0:
                    normalrate += 1
                elif int(li["rate"]) == -1:
                    badrate += 1
                else:
                    effectrate -= 1
                    uneffectrate += 1
            else:
                uneffectrate += 1

        rate_dic["effectrate"] = effectrate
        rate_dic["goodrate"] = goodrate
        rate_dic["normalrate"] = normalrate
        rate_dic["badrate"] = badrate

        return rate_dic


    def CensusAllRate(self):       # 统计所有的评论情况
        pageamount = int(self.rate)/20
        pageamount = math.ceil(pageamount)      # 页面总数，向上取整

        right = self.rateUrl.index('1')
        url = self.rateUrl[0: right]

        Rate_All_dic = {            # 用以储存总的情况
            "effectrate": 0,
            "goodrate": 0,
            "normalrate": 0,
            "badrate": 0
        }

        pageindex = 0
        while pageindex <= pageamount:
            pageindex += 1
            scrape_url = url + str(pageindex)
            dic = self.ScrapeComments(scrape_url)
            Rate_All_dic["effectrate"] += dic["effectrate"]
            Rate_All_dic["goodrate"] += dic["goodrate"]
            Rate_All_dic["normalrate"] += dic["normalrate"]
            Rate_All_dic["badrate"] += dic["badrate"]
            if pageindex%5 == 0:        # 爬五页停一下
                time.sleep(1)

        self.effectrate = Rate_All_dic["effectrate"]
        self.goodrate = Rate_All_dic["goodrate"]
        self.normalrate = Rate_All_dic["normalrate"]
        self.badrate = Rate_All_dic["badrate"]

        return


    def getScore(self):             # 计算得分
        good_rate_score = int(self.goodrate)/int(self.effectrate)*10      # 好评得分
        normal_rate_score = int(self.normalrate)/int(self.effectrate)*10  # 中评得分
        bad_rate_score = int(self.badrate)/int(self.effectrate)*10        # 差评得分
        effect_rate_score = int(self.effectrate)/int(self.rate)*10 + (1-math.exp(-int(self.effectrate)))*10       # 有效评论得分
        rate_aomunt_score = (1-math.exp(-int(self.rate)))*20         # 评论总数得分

        score = good_rate_score - normal_rate_score - 2*bad_rate_score + effect_rate_score + rate_aomunt_score
        self.score = score
        return
