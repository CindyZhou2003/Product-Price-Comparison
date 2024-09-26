import json
import re
import requests
import pprint
import csv
import time
import random
from DrissionPage import ChromiumPage

driver = ChromiumPage()
driver.get('https://mobile.yangkeduo.com/')
time.sleep(random.uniform(2, 5))

driver.ele('css:#q').input("手机")
driver.ele('css:.btn-search.tb-bg').click()
time.sleep(random.uniform(2, 5))

response = driver.listen.wait().response
mtopjsonp = response.body
mtopjson = re.findall('mtopjsonp\d+\((.*)\)', mtopjsonp)[0]

print(mtopjson)

mtop_data = json.loads(mtopjson)

itemsArray = mtop_data['data']['itemsArray']

for item in itemsArray:
    title = item['title']
    priceWap = item['priceWap']
    realSales = item['realSales']
    procity = item['procity']
    nick = item['nick']
    shopTitle = item['shopInfo']['title']
    auctionUrl = item['auctionUrl']
    pic_path = item['picPath']
    dit = {
        'title': title,
        'price': priceWap,
        'realSales': realSales,
        'shop': shopTitle,
        'nick': nick,
        'procity': procity,
        'link': auctionUrl,
        'pic_path': pic_path,
    }
    print(dit)