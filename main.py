# 主函数
# Coded by ShiHang


import Comments
import Goods
import Shop
import SourceCrawler

'''
source = SourceCrawler.SourceCrawler('air+jordan', '0')
nidlist = source.scrape()

result = list()

for li in nidlist:
    comment = Comments.Comment(li)
    comment.ISTaoBao()
    if comment.isTaoBao == True:
        comment.getRateAmount()
        comment.CensusAllRate()
        comment.getScore()
        dic = {"id": li, "amount": comment.score}
        result.append(dic)
'''

c = Comments.Comment("563486552382")
c.getRateAmount()
c.CensusAllRate()
c.getScore()
print(c.score)
