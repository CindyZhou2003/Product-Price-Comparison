import os
import pickle
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')  # 替换'myproject'为你的项目名称
django.setup()

import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from DrissionPage import ChromiumPage
from selenium.webdriver.chrome.options import Options
from DrissionPage.errors import ElementNotFoundError
from pyquery import PyQuery as pq
from .models import Products,Likes,Prices

def crawl_tb(keyword):
    """
    爬取淘宝商品并保存到 Django 数据库的 Products 表。
    :param keyword: 关键词
    """
    def save_to_db(products):
        """将商品数据保存到 Django 数据库"""
        for product in products:
            try:
                # 检查是否已存在相同商品（根据链接判断）
                if not Products.objects.filter(link=product['link']).exists():
                    Products.objects.create(
                        title=product['title'],
                        price=product['price'],
                        info=product['deal'],
                        shop=product['shop'],
                        img=product['img'],
                        link=product['link'],
                        platform=product['platform']
                    )
            except Exception as e:
                print(f"保存商品时出错: {e}")

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

        html = driver.page_source
        with open(f"page_{page}.html", "w", encoding="utf-8") as f:
            f.write(html)  # 保存源码
        doc = pq(html)
        # items = doc('div.contentInner--xICYBlag > a').items()
        items = doc('a.doubleCardWrapperAdapt--mEcC7olq').items()

        filtered_products = []
        for item in items:
            title = item.find('.title--qJ7Xg_90 span').text()
            price_int = item.find('.priceInt--yqqZMJ5a').text()
            price_float = item.find('.priceFloat--XpixvyQ1').text()
            try:
                if price_int and price_float:
                    price = float(f"{price_int}{price_float}")
                    print(price)
                else:
                    price = 0.0
            except ValueError:
                price = 0.0

            if price == 0.0:
                continue

            deal = item.find('.realSales--XZJiepmt').text()
            shop = item.find('.shopNameText--DmtlsDKm').text()
            t_url = item.attr('href')
            link = "https:" + t_url if t_url.startswith("//") else t_url
            # img = item.find('.mainPicWrapper--qRLTAeii img').attr('src')
            img = item.find('img.mainPic--Ds3X7I8z').attr('src')

            product = {
                'title': title,
                'price': price,
                'deal': deal,
                'shop': shop,
                'link': link,
                'img': img,
                'platform': '淘宝'
            }
            print(f"准备保存的商品：{product}")
            filtered_products.append(product)
        # print("当前页爬取的商品：", filtered_products)
        # 保存数据到数据库
        save_to_db(filtered_products)

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

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})

    driver.get("https://www.taobao.com")
    driver.maximize_window()
    # 加载 Cookies
    with open("cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

    driver.refresh()  # 刷新页面以应用 Cookies
    wait = WebDriverWait(driver, 5)

    try:
        driver.execute_script("""
            var closeButton = document.querySelector('.closeIconWrapper');
            if (closeButton) {
                closeButton.click();
                console.log("弹窗已关闭");
            }
        """)
    except Exception as e:
        print("通过 JavaScript 关闭弹窗失败:", e)

    input('...')
    search_goods(keyword, 1, 2)  # 从第一页爬取两页数据
    # 爬取数据逻辑
    print(f"所有关键词爬取完成，数据已存储到数据库！")

def crawl_jd(keyword):
    """
    爬取京东商品并保存到 Django 数据库的 Products 表。
    :param keyword: 搜索关键词
    """

    def save_to_db(products):
        """将商品数据保存到 Django 数据库"""
        for product in products:
            try:
                if not Products.objects.filter(link=product['link']).exists():
                    Products.objects.create(
                        title=product['title'],
                        price=product['price'],
                        info=product['comments'],
                        shop=product['shop'],
                        img=product['img'],
                        link=product['link'],
                        platform='京东'
                    )
            except Exception as e:
                print(f"保存商品时出错: {e}")

    # 配置无头模式
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # 初始化浏览器
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.jd.com')
    driver.maximize_window()
    time.sleep(random.uniform(2, 5))

    # 搜索商品
    # input('请登录后按回车键继续')
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#key"))
    )
    search_box.send_keys(keyword)
    driver.find_element(By.CSS_SELECTOR, '.button').click()

    print(f"正在提取商品信息: {keyword}")

    for page in range(2):
        time.sleep(random.uniform(2, 5))

        # 滑动页面，加载商品信息
        for scroll_pos in range(1000, 10000, 1000):
            driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
            time.sleep(random.uniform(2, 3))

        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 5))

        # 提取商品列表
        lis = driver.find_elements(By.CSS_SELECTOR, '.gl-item')
        print(f"{keyword}: 正在处理第 {page + 1} 页")

        filtered_products = []
        for li in lis:
            try:
                title = li.find_element(By.CSS_SELECTOR, '.p-name a em').text
                price = li.find_element(By.CSS_SELECTOR, '.p-price strong i').text
                price = float(price) if price else 0.0
                if price == 0.0:
                    continue

                img = li.find_element(By.CSS_SELECTOR, '.p-img a img').get_attribute('src')
                comments = li.find_element(By.CSS_SELECTOR, '.p-commit strong a').text

                try:
                    shop = li.find_element(By.CSS_SELECTOR, '.hd-shopname').text
                except:
                    shop = '京东自营'

                link = li.find_element(By.CSS_SELECTOR, '.p-img a').get_attribute('href')
                if not link.startswith("http"):
                    link = f"https:{link}"

                product = {
                    'title': title,
                    'price': price,
                    'comments': comments,
                    'shop': shop,
                    'img': img,
                    'link': link,
                }
                filtered_products.append(product)
                print(product)
            except Exception as e:
                print(f"提取商品时出错: {e}")

        save_to_db(filtered_products)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pn-next"))
            )
            next_button.click()
        except:
            print("未找到下一页按钮，爬取结束")
            break

    driver.quit()

def tb_update_price(good,url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)

    try:
        # 反爬机制
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                               {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
        driver.get(url)
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)
        # 手动扫码登录
        input("请在浏览器中扫码登录，完成后按回车继续...")
        # time.sleep(10)
        time.sleep(random.uniform(3, 5))  # 额外等待时间，确保 JavaScript 内容加载完成

        # 获取页面 HTML 源代码
        html = driver.page_source
        doc = pq(html)

        current_price = doc('div.originPrice--UnZ18wCd .priceText--gdYzG_l_').eq(0).text()
        # current_price = doc('div.extraPrice--Y7SiNGXT .priceText--gdYzG_l_.extraPriceText--aysuZjG_').text()

        if current_price:
            good.modify_price(current_price)
            good.save()
        else:
            # 尝试获取单一价格
            current_price = doc('div.highlightPrice--OOP9oDP8 .text--fZ9NUhyQ').eq(0).text()
            if current_price:
                good.modify_price(current_price)
                good.save()
            else:
                print("未找到任何价格信息")
        print("current price:", current_price)
        # 将价格加入历史价格表
        product_new_price = Prices(product=good, price=current_price)
        product_new_price.save()
    except ElementNotFoundError:
        print("Error: Unable to find the price element on the page.")
    # 关闭浏览器
    finally:
        driver.quit()

def jd_update_price(good,url):
    driver = ChromiumPage()
    try:
        # Open the specified URL
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Simulate a human interaction delay
        time.sleep(10) # 手动登录
        print("Successfully loaded the product page, fetching the price...")

        # Locate and fetch the price element on the page
        price_float = float(driver.ele('css:.price').text)
        if price_float:
            print(f"Current Product Price:{price_float}")
        else:
            price = driver.ele('css:.p-price').text
            price_cleaned = price.replace('￥', '').strip()
            # 转换为 float 类型
            price_float = float(price_cleaned)
            print(f"Current Product Price: {price_float}")

        good.modify_price(price_float)
        good.save()
        # 将价格加入历史价格表
        product_new_price = Prices(product=good, price=price_float)
        product_new_price.save()

    except ElementNotFoundError:
        print("Error: Unable to find the price element on the page.")
    finally:
        driver.quit()  # Ensure the browser closes after the task

from django.db import transaction
from django.core.paginator import Paginator


def update_favorite_prices():
    """
    后端管理员手动对用户关注的商品进行价格更新
    用户关注表Likes
    """
    try:
        # 批量处理商品，设置每页处理数量
        batch_size = 5

        # 获取用户关注的所有商品，并根据平台分类
        favorite_products = Products.objects.filter(
            id__in=Likes.objects.values_list('product_id', flat=True).distinct()
        )
        print(f"喜欢的商品数: {Likes.objects.count()}")
        print(f"关注商品的ID列表: {Likes.objects.values_list('product_id', flat=True).distinct()}")
        print(f"过滤后的商品数: {favorite_products.count()}")

        # 淘宝商品价格更新
        tb_products = favorite_products.filter(platform="淘宝").order_by('id')
        tb_paginator = Paginator(tb_products, batch_size)
        print(f"淘宝商品数: {tb_products.count()}")


        for page_number in tb_paginator.page_range:
            try:
                with transaction.atomic():
                    page = tb_paginator.page(page_number)
                    for product in page.object_list:
                        try:
                            tb_update_price(product, product.link)
                        except Exception as e:
                            # 捕获单个商品更新异常并记录日志
                            print(f"Failed to update price for 淘宝商品 {product.id}: {e}")
            except Exception as e:
                # 捕获分页事务异常并记录日志
                print(f"Transaction failed for 淘宝商品 batch {page_number}: {e}")

        # 京东商品价格更新
        jd_products = favorite_products.filter(platform="京东").order_by('id')
        jd_paginator = Paginator(jd_products, batch_size)
        print(f"京东商品数: {jd_products.count()}")

        for page_number in jd_paginator.page_range:
            try:
                with transaction.atomic():
                    page = jd_paginator.page(page_number)
                    for product in page.object_list:
                        try:
                            jd_update_price(product, product.link)
                        except Exception as e:
                            # 捕获单个商品更新异常并记录日志
                            print(f"Failed to update price for 京东商品 {product.id}: {e}")
            except Exception as e:
                # 捕获分页事务异常并记录日志
                print(f"Transaction failed for 京东商品 batch {page_number}: {e}")

    except Exception as e:
        # 捕获整个更新过程中的异常
        print(f"Overall update_prices process failed: {e}")

def save_cookies():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})

    driver.get("https://www.taobao.com")
    driver.maximize_window()

    # 等待用户手动登录
    input("请手动完成登录后按 Enter 键继续...")

    # 保存 Cookies 到文件
    with open("cookies.pkl", "wb") as file:
        pickle.dump(driver.get_cookies(), file)

    print("Cookies 已保存")
    driver.quit()

if __name__ == "__main__":
    # update_favorite_prices()
    # save_cookies()
    crawl_tb('台灯')