#
import random
import time
import csv
from DrissionPage import ChromiumPage
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage.errors import ElementNotFoundError

"""
根据特定商品的URL更新价格，要求已经登陆过该网站的账号
"""
def find_specific_product(url, web):
    # options = ChromiumOptions()  # Create a ChromiumOptions object from DrissionPage
    # options.headless = True  # Enable headless mode
    # options.set_argument('--headless=True')  # Sometimes explicitly setting this argument can help
    # options.set_argument('--disable-gpu')  # Disable GPU rendering
    # options.set_argument('--no-sandbox')  # Disable sandboxing (might be required for headless mode)
    # options.set_argument('--disable-dev-shm-usage')  # Overcome limited resource problems in environments like Docker
    # options.set_argument('--remote-debugging-port=9222')  # Disable remote debugging window opening
    driver = ChromiumPage()# Pass the options to ChromiumPage
    # login
    # driver.get('https://passport.suning.com/ids/login')
    # driver.ele('css:.login-tab .tab-item:nth-child(2)').click()
    # driver.ele('css:.username-box .input-box').input('13917199624')
    # driver.ele('css:.password-box .input-box').input('092903Cindy')
    # driver.ele('css:.button').click()
    # time.sleep(random.uniform(2, 5))

    driver.get(url)
    time.sleep(random.uniform(2, 5))

    if web== 'suning':
        print("成功搜到该商品，正在获取新价格...")
        price = driver.ele('css:.mainprice').text
        print(price)

    if web== 'jingdong':
        print("成功搜到该商品，正在获取新价格...")
        price = driver.ele('css:.p-price').text
        print(price)


url='https://item.jd.com/100044834023.html'
web='jingdong'
find_specific_product(url, web)