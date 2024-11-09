import random
import time
from DrissionPage import ChromiumPage
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage.errors import ElementNotFoundError
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
import csv

def find_specific_product(url):
    # Initialize the ChromiumPage with headless options
    # driver = ChromiumPage()
    # driver.get(url)
    # time.sleep(random.uniform(2, 5))  # Simulate a human interaction delay
    #
    # print("Successfully loaded the product page, fetching the price...")
    #
    # # JD: Locate and fetch the price element on the page
    # price = driver.ele('css:.p-price').text


    # TB
    # 启动ChromeDriver服务
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)

    # 反爬机制
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
    driver.get(url)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    # 手动扫码登录
    input("请在浏览器中扫码登录，完成后按回车继续...")

    def get_price():
        try:
            # 尝试查找第一个选择器
            price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.text--lKftOoXS')))
            return price_element.text
        except:
            pass

        try:
            # 如果第一个选择器不存在，则尝试第二个选择器
            price_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.priceText--gdYzG_l_.extraPriceText--aysuZjG_')))
            return price_element.text
        except:
            return None

    # 获取价格
    price = get_price()
    if price:
        print(f"Product Price: {price}")
    else:
        print("未找到价格信息")

    # 关闭浏览器
    driver.quit()


# Example usage with a JD.com product URL
url = 'https://detail.tmall.com/item.htm?priceTId=2147828717308928536503612e802f&utparam=%7B%22aplus_abtest%22%3A%22d2acb0219a96a8f84963167dce4783d5%22%7D&id=811164706452&ns=1&abbucket=11&xxc=taobaoSearch&skuId=5631698725936'
find_specific_product(url)

