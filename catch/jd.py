# jd爬虫代码
import random
import time
import csv
from DrissionPage import ChromiumPage
from DrissionPage.errors import ElementNotFoundError

def jd(search, page):
    # Open CSV file to write data
    # f = open(file, mode='w', encoding='utf-8', newline='') # 新建写
    # f = open('jd.csv', mode='a', encoding='utf-8', newline='') # 追加
    with open('../data/jd.csv', mode='a', encoding='utf-8', newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=['title', 'price', 'comments', 'shop', 'img', 'link'])
        # Only write the header if the file is empty
        if f.tell() == 0:
            csv_writer.writeheader()

        # Initialize the browser
        driver = ChromiumPage()
        driver.get('https://www.jd.com')
        time.sleep(random.uniform(2, 5))

        # Perform search for '手机'
        driver.ele('css:#key').input(search)
        driver.ele('css:.button').click()

        print("正在提取商品信息..."+search)
        # Loop through 10 pages
        for i in range(page):

            time.sleep(random.uniform(2, 5))
            # Scroll down gradually
            for scroll_pos in range(1000, 10000, 1000):
                driver.scroll.to_location(0, scroll_pos)
                time.sleep(random.uniform(2, 5))

            driver.scroll.to_bottom()  # Scroll to bottom to load all products
            time.sleep(random.uniform(2, 5))

            # Select all product elements
            lis = driver.eles('css:.gl-item')

            print(search+": page"+str(i))

            # Extract data from each product
            for li in lis:
                """提取商品信息"""
                title = li.ele('css:.p-name a em').text
                price = li.ele('css:.p-price strong i').text
                img = li.ele('css:.p-img a img').attr('src')
                comm = li.ele('css:.p-commit strong a').text

                # Try to get the shop name, default to '京东自营' if not found
                try:
                    shop = li.ele('css:.hd-shopname').text
                except ElementNotFoundError:
                    shop = '京东自营'

                # Extract product link
                link = li.ele('css:.p-img a').attr('href')

                # Create dictionary with extracted data
                dit = {
                    'title': title,
                    'price': price,
                    'comments': comm,
                    'shop': shop,
                    'img': img,
                    'link': link,
                }
                # Write the data to CSV
                csv_writer.writerow(dit)
                print(dit)
            # Click the next page button
            driver.ele('css:.pn-next').click()

        driver.quit()




goodstype_jd = {
    '家电','童装','内衣','男鞋','文具','潮玩','宠物','运动','生鲜',
    '洗护','酒类','乐器','珠宝','食品','美妆','箱包','女装','男装',
    '办公','电脑','母婴','图书','鲜花','手机','家具','厨具','配饰','女鞋',
    }

for ty in goodstype_jd:
    jd(ty,5)





