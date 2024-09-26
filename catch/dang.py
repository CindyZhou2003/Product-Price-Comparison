#
import random
import time
import csv
from DrissionPage import ChromiumPage
from DrissionPage.errors import ElementNotFoundError


def dang(search,page):
    # Open CSV file to write data
    with open('../data/dang.csv', mode='a', encoding='utf-8', newline='') as f:

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
        driver.get('https://www.dangdang.com/')
        # driver.get('https://search.dangdang.com/?key=%CD%BC%CA%E9&act=input&page_index=8')
        time.sleep(random.uniform(2, 5))
        # Perform search
        # driver.ele('css:#key_S').input(search)

        # This will directly execute the JavaScript defined in the button's onclick event
        # driver.run_js("document.getElementById('search_btn').click();")

        print("正在提取商品信息..."+search)

        # Loop through 10 pages
        for i in range(page):

            time.sleep(random.uniform(2, 5))
            # Scroll down gradually
            for scroll_pos in range(1000, 15000, 1000):
                driver.scroll.to_location(0, scroll_pos)
                time.sleep(random.uniform(2, 5))

            driver.scroll.to_bottom()  # Scroll to bottom to load all products
            time.sleep(random.uniform(2, 5))

            # Select all product elements
            lis = driver.eles('css:#search_nature_rg ul li')
            print(search+": page"+str(i))

            # Extract data from each product
            for li in lis:
                """提取商品信息"""

                title = li.ele('css:.name a').text

                try:
                    price = li.ele('css:.price .search_now_price').text
                except ElementNotFoundError:
                    price = li.ele('css:.price .price_n').text

                img = li.ele('css:.pic img').attr('src')

                try:
                    comm = li.ele('css:.search_star_line a').text
                except ElementNotFoundError:
                    try:
                        comm = li.ele('css:.star a').text
                    except ElementNotFoundError:
                        comm ='0'

                try:
                    shop = li.ele('css:.search_shangjia a').text
                except ElementNotFoundError:
                    try:
                        shop = li.ele('css:.link').text
                    except ElementNotFoundError:
                        shop = '自营'

                # Extract product link
                link = li.ele('css:.name a').attr('href')

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
            driver.ele('css:.next').click()

        driver.quit()

goods_dang={
    '图书','电子书','童装童鞋','食品','母婴玩具','运动户外','办公用品'
}
for ty in goods_dang:
    dang(ty, 6)

# dang('图书',3)

urls={
    'https://category.dangdang.com/cid4003900.html',
    'https://category.dangdang.com/cid4003728.html',
}