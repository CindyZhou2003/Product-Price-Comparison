
import random
import time
import csv
from DrissionPage import ChromiumPage
from DrissionPage.errors import ElementNotFoundError
from DrissionPage._configs.chromium_options import ChromiumOptions


def sn(search,page):
    # Open CSV file to write data
    with open('../data/sn.csv', mode='a', encoding='utf-8', newline='') as f:

        csv_writer = csv.DictWriter(f, fieldnames=['title', 'price', 'comments', 'shop', 'img', 'link'])

        # Only write the header if the file is empty
        if f.tell() == 0:
            csv_writer.writeheader()

        # Set up Chromium options for headless mode
        # options = ChromiumOptions()  # Create a ChromiumOptions object from DrissionPage
        # options.headless = True  # Enable headless mode
        # options.set_argument('--headless=True')  # Sometimes explicitly setting this argument can help
        # options.set_argument('--disable-gpu')  # Disable GPU rendering
        # options.set_argument('--no-sandbox')  # Disable sandboxing (might be required for headless mode)
        # options.set_argument('--disable-dev-shm-usage')  # Overcome limited resource problems in environments like Docker
        # options.set_argument('--remote-debugging-port=9222')  # Disable remote debugging window opening
        # Initialize the browser with the specified options
        # Optional: Add more arguments to ensure headless mode works properly on some environments
        # options.set_argument('--window-size=1920x1080')  # Set a window size to avoid errors in headless mode
        driver = ChromiumPage()  # Pass the options to ChromiumPage
        # driver = ChromiumPage(options)  # Pass the options to ChromiumPage
        driver.get('https://www.suning.com/')

        # Perform search
        driver.ele('css:#searchKeywords').input(search)
        driver.ele('css:#searchSubmit').click()
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
            lis = driver.eles('css:#product-list ul li')
            print(search+": page"+str(i))

            # Extract data from each product
            for li in lis:
                """提取商品信息"""
                title = li.ele('css:.title-selling-point a').text
                price = li.ele('css:.def-price').text
                img = li.ele('css:.img-block a img').attr('src')
                try:
                    comm = li.ele('css:.info-evaluate a').text
                except ElementNotFoundError:
                    comm = '0'
                # Try to get the shop name, default to '京东自营' if not found
                try:
                    shop = li.ele('css:.store-stock').text
                except ElementNotFoundError:
                    shop = '未知'

                # Extract product link
                link = li.ele('css:.title-selling-point a').attr('href')

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
            driver.ele('css:#nextPage').click()

        driver.quit()

goodstype_sn = {
    '家电','童装','内衣','男鞋','文具','潮玩','宠物','运动','生鲜',
    '洗护','酒类','乐器','珠宝','食品','美妆','箱包','女装','男装',
    '办公','母婴','图书','鲜花','家具','厨具','配饰','女鞋',
    }

# '手机','电脑',
for ty in goodstype_sn:
    sn(ty,5)