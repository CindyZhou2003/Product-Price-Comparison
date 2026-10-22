import os
import pickle
from hashlib import sha256
from pathlib import Path

import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from DrissionPage.errors import ElementNotFoundError
from pyquery import PyQuery as pq
from backend.models import Products, Prices
from DrissionPage import ChromiumPage

TB_COOKIE_FILE = Path(__file__).resolve().parent / 'tb_cookies.pkl'
USER_AGENT = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


def tb_driver(headless):
    """
    创建隐藏了 webdriver 特征的 Chrome 驱动，用于淘宝
    """
    options = Options()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_argument(USER_AGENT)

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})
    return driver


def load_tb_cookies(driver):
    """
    载入预先保存的淘宝登录 Cookie，代替在请求中等待人工登录
    """
    if not TB_COOKIE_FILE.exists():
        raise RuntimeError("缺少淘宝登录 Cookie，请先运行 python manage.py login_crawler taobao")

    # 只能给当前页面所在域名添加 Cookie
    driver.get("https://www.taobao.com")
    with open(TB_COOKIE_FILE, "rb") as file:
        for cookie in pickle.load(file):
            driver.add_cookie(cookie)


def login_crawler(platform):
    """
    打开有界面的浏览器供人工登录，保存登录状态供之后的爬虫使用（命令行中执行）
    :param platform: 'taobao' 或 'jd'
    """
    if platform == 'taobao':
        driver = tb_driver(headless=False)
        try:
            driver.get("https://www.taobao.com")
            input("请在浏览器中完成淘宝登录后按回车键继续...")
            with open(TB_COOKIE_FILE, "wb") as file:
                pickle.dump(driver.get_cookies(), file)
        finally:
            driver.quit()
    else:
        # DrissionPage 使用固定的浏览器用户目录，登录状态会保留到之后的爬取
        driver = ChromiumPage()
        try:
            driver.get('https://www.jd.com')
            input("请在浏览器中完成京东登录后按回车键继续...")
        finally:
            driver.quit()


def save_products(products):
    """
    按链接哈希去重后保存到 Products 表
    """
    for product in products:
        try:
            Products.objects.get_or_create(
                link_hash=sha256(product['link'].encode('utf-8')).hexdigest(),
                defaults=product,
            )
        except Exception as e:
            print(f"保存商品时出错: {e}")


def crawl_tb(keyword):
    """
    爬取淘宝商品并保存到 Django 数据库的 Products 表。
    :param keyword: 关键词
    """
    def get_goods(page):
        """爬取当前页面商品信息"""
        time.sleep(random.uniform(2, 5))  # 等待加载
        print(f"开始爬取第 {page} 页")

        # 滚动到页面底部，模拟加载
        screen_height = driver.execute_script("return window.innerHeight")
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        current_position = 0

        while current_position < scroll_height - screen_height:
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            current_position += screen_height
            time.sleep(random.uniform(2, 5))

        doc = pq(driver.page_source)
        items = doc('a.doubleCardWrapperAdapt--mEcC7olq').items()

        filtered_products = []
        for item in items:
            title = item.find('.title--qJ7Xg_90 span').text()
            price_int = item.find('.priceInt--yqqZMJ5a').text()
            price_float = item.find('.priceFloat--XpixvyQ1').text()
            try:
                price = float(f"{price_int}{price_float}") if price_int and price_float else 0.0
            except ValueError:
                price = 0.0

            if price == 0.0:
                continue

            t_url = item.attr('href')
            filtered_products.append({
                'title': title,
                'price': price,
                'info': item.find('.realSales--XZJiepmt').text(),
                'shop': item.find('.shopNameText--DmtlsDKm').text(),
                'link': "https:" + t_url if t_url.startswith("//") else t_url,
                'img': item.find('img.mainPic--Ds3X7I8z').attr('src'),
                'platform': '淘宝',
            })
        save_products(filtered_products)

    def search_goods(keyword, start_page, total_pages):
        """搜索商品并爬取多页"""
        print(f"正在搜索关键词：{keyword}")
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        input_box.send_keys(keyword)
        search_button.click()
        time.sleep(3)

        get_goods(start_page)
        for i in range(start_page + 1, total_pages + 1):
            print(f"翻页至第 {i} 页")
            next_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.next-btn.next-medium.next-btn-normal.next-pagination-item.next-next')
            ))
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(random.uniform(3, 5))
            get_goods(i)

    driver = tb_driver(headless=True)
    try:
        load_tb_cookies(driver)
        driver.refresh()  # 刷新页面以应用 Cookies
        driver.maximize_window()
        wait = WebDriverWait(driver, 5)

        driver.execute_script("""
            var closeButton = document.querySelector('.closeIconWrapper');
            if (closeButton) {
                closeButton.click();
            }
        """)

        search_goods(keyword, 1, 1)  # 爬取1页数据
        print(f"所有关键词爬取完成，数据已存储到数据库！")
    finally:
        driver.quit()


def crawl_jd(keyword):
    """
    爬取京东商品并保存到 Django 数据库的 Products 表。
    需要先运行 python manage.py login_crawler jd 登录
    :param keyword: 搜索关键词
    """
    driver = ChromiumPage()
    try:
        driver.get('https://www.jd.com')
        time.sleep(random.uniform(2, 5))
        # 搜索商品
        driver.ele('css:#key').input(keyword)
        driver.ele('css:.button').click()

        print(f"正在提取商品信息: {keyword}")

        for page in range(1):
            time.sleep(random.uniform(2, 5))

            # 滑动页面，加载商品信息
            for scroll_pos in range(1000, 10000, 1000):
                driver.scroll.to_location(0, scroll_pos)
                time.sleep(random.uniform(2, 3))

            driver.scroll.to_bottom()
            time.sleep(random.uniform(2, 5))

            # 提取商品列表
            lis = driver.eles('css:.gl-item')
            print(f"{keyword}: 正在处理第 {page + 1} 页")

            filtered_products = []
            for li in lis:
                try:
                    price = li.ele('css:.p-price strong i').text
                    price = float(price) if price else 0.0
                    if price == 0.0:  # 过滤价格为 0 的商品
                        continue

                    # 尝试获取店铺名
                    try:
                        shop = li.ele('css:.hd-shopname').text
                    except ElementNotFoundError:
                        shop = '京东自营'

                    link = li.ele('css:.p-img a').attr('href')
                    if not link.startswith("http"):
                        link = f"https:{link}"

                    filtered_products.append({
                        'title': li.ele('css:.p-name a em').text,
                        'price': price,
                        'info': li.ele('css:.p-commit strong a').text,
                        'shop': shop,
                        'img': li.ele('css:.p-img a img').attr('src'),
                        'link': link,
                        'platform': '京东',
                    })
                except Exception as e:
                    print(f"提取商品时出错: {e}")

            save_products(filtered_products)

            # 翻页操作
            try:
                driver.ele('css:.pn-next').click()
            except ElementNotFoundError:
                print("未找到下一页按钮，爬取结束")
                break
    finally:
        driver.quit()


def record_price(good, price):
    """
    更新商品当前价格并写入历史价格表
    """
    good.price = price
    good.save()
    Prices.objects.create(product=good, price=price)


def tb_update_price(good, url):
    driver = tb_driver(headless=False)
    try:
        load_tb_cookies(driver)
        driver.get(url)
        driver.maximize_window()
        time.sleep(random.uniform(3, 5))  # 额外等待时间，确保 JavaScript 内容加载完成

        doc = pq(driver.page_source)
        # 优先取原价区域的价格，没有时取单一价格
        current_price = (doc('div.originPrice--UnZ18wCd .priceText--gdYzG_l_').eq(0).text()
                         or doc('div.highlightPrice--OOP9oDP8 .text--fZ9NUhyQ').eq(0).text())
        if not current_price:
            raise RuntimeError("未找到任何价格信息")

        print("current price:", current_price)
        record_price(good, float(current_price))
    finally:
        driver.quit()


def jd_update_price(good, url):
    """
    需要先运行 python manage.py login_crawler jd 登录
    """
    driver = ChromiumPage()
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Simulate a human interaction delay

        try:
            price_float = float(driver.ele('css:.price').text)
        except (ElementNotFoundError, ValueError):
            price_float = float(driver.ele('css:.p-price').text.replace('￥', '').strip())

        print(f"Current Product Price: {price_float}")
        record_price(good, price_float)
    finally:
        driver.quit()
