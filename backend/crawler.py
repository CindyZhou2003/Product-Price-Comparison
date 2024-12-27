import os
import pickle
from hashlib import sha256

import django
from selenium.common import NoSuchElementException

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')  # 替换'myproject'为你的项目名称
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
from backend.models import Products,Likes,Prices
from selenium.webdriver.chrome.service import Service
from DrissionPage import ChromiumPage

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
                        platform=product['platform'],
                        link_hash = product['link_hash']
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
            link_hash = sha256(link.encode('utf-8')).hexdigest()
            product = {
                'title': title,
                'price': price,
                'deal': deal,
                'shop': shop,
                'link': link,
                'img': img,
                'platform': '淘宝',
                'link_hash': link_hash,
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
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    # 指定浏览器和驱动路径

    # driver_path = "/usr/bin/chromedriver"  # 替换为实际的 ChromeDriver 路径
    # driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})

    driver.get("https://www.taobao.com")
    driver.maximize_window()
    # 加载 Cookies
    # with open("tb_cookies.pkl", "rb") as file:
    #     cookies = pickle.load(file)
    #     for cookie in cookies:
    #         driver.add_cookie(cookie)
    #
    # driver.refresh()  # 刷新页面以应用 Cookies
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

    input('请先登录')

    search_goods(keyword, 1, 1)  # 爬取1页数据
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
                # 检查是否已存在相同商品（根据链接判断）
                if not Products.objects.filter(link=product['link']).exists():
                    Products.objects.create(
                        title=product['title'],
                        price=product['price'],
                        info=product['comments'],
                        shop=product['shop'],
                        img=product['img'],
                        link=product['link'],
                        platform='京东'  # 添加平台名称
                    )
            except Exception as e:
                print(f"保存商品时出错: {e}")

    # 初始化浏览器
    driver = ChromiumPage()
    driver.get('https://www.jd.com')
    time.sleep(random.uniform(2, 5))
    input("等待登录....")
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
            """提取商品信息"""
            try:
                title = li.ele('css:.p-name a em').text
                price = li.ele('css:.p-price strong i').text
                price = float(price) if price else 0.0  # 转为浮点数，默认为 0.0
                if price == 0.0:  # 过滤价格为 0 的商品
                    continue

                img = li.ele('css:.p-img a img').attr('src')
                comments = li.ele('css:.p-commit strong a').text

                # 尝试获取店铺名
                try:
                    shop = li.ele('css:.hd-shopname').text
                except ElementNotFoundError:
                    shop = '京东自营'

                # 商品链接
                link = li.ele('css:.p-img a').attr('href')
                if not link.startswith("http"):
                    link = f"https:{link}"

                # 构建商品信息字典
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

        # 保存数据到数据库
        save_to_db(filtered_products)

        # 翻页操作
        try:
            driver.ele('css:.pn-next').click()
        except ElementNotFoundError:
            print("未找到下一页按钮，爬取结束")
            break

    driver.quit()
# def crawl_jd(keyword):
#     """
#     爬取京东商品并保存到 Django 数据库的 Products 表。
#     :param keyword: 搜索关键词
#     """
#
#     def save_to_db(products):
#         """将商品数据保存到 Django 数据库"""
#         for product in products:
#             try:
#                 if not Products.objects.filter(link=product['link']).exists():
#                     Products.objects.create(
#                         title=product['title'],
#                         price=product['price'],
#                         info=product['comments'],
#                         shop=product['shop'],
#                         img=product['img'],
#                         link=product['link'],
#                         link_hash=product['link_hash'],
#                         platform='京东'
#                     )
#             except Exception as e:
#                 print(f"保存商品时出错: {e}")
#
#     # 配置无头模式
#     chrome_options = Options()
#     # chrome_options.add_argument("--headless")
#     # chrome_options.add_argument("--disable-gpu")
#     # chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
#
#     # driver_path = "/usr/bin/chromedriver"  # 替换为实际的 ChromeDriver 路径
#
#     # 初始化浏览器
#     # driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get('https://www.jd.com')
#     driver.maximize_window()
#
#     # with open("jd_cookies.pkl", "rb") as file:
#     #     cookies = pickle.load(file)
#     #     for cookie in cookies:
#     #         driver.add_cookie(cookie)
#     #
#     # driver.refresh()  # 刷新页面以应用 Cookies
#     time.sleep(random.uniform(2, 5))
#
#     # 搜索商品
#     # input('请登录后按回车键继续')
#     search_box = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "#key"))
#     )
#     search_box.send_keys(keyword)
#     driver.find_element(By.CSS_SELECTOR, '.button').click()
#
#     print(f"正在提取商品信息: {keyword}")
#
#     for page in range(1):
#         time.sleep(random.uniform(2, 5))
#
#         # 滑动页面，加载商品信息
#         for scroll_pos in range(1000, 10000, 1000):
#             driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
#             time.sleep(random.uniform(2, 3))
#
#         # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(random.uniform(2, 5))
#
#         # 提取商品列表
#         lis = driver.find_elements(By.CSS_SELECTOR, '.gl-item')
#         print(f"{keyword}: 正在处理第 {page + 1} 页")
#
#         filtered_products = []
#         for li in lis:
#             try:
#                 title = li.find_element(By.CSS_SELECTOR, '.p-name a em').text
#                 price = li.find_element(By.CSS_SELECTOR, '.p-price strong i').text
#                 price = float(price) if price else 0.0
#                 if price == 0.0:
#                     continue
#
#                 img = li.find_element(By.CSS_SELECTOR, '.p-img a img').get_attribute('src')
#                 comments = li.find_element(By.CSS_SELECTOR, '.p-commit strong a').text
#
#                 try:
#                     shop = li.find_element(By.CSS_SELECTOR, '.hd-shopname').text
#                 except:
#                     shop = '京东自营'
#
#                 link = li.find_element(By.CSS_SELECTOR, '.p-img a').get_attribute('href')
#                 if not link.startswith("http"):
#                     link = f"https:{link}"
#                 link_hash = sha256(link.encode('utf-8')).hexdigest()
#                 product = {
#                     'title': title,
#                     'price': price,
#                     'comments': comments,
#                     'shop': shop,
#                     'img': img,
#                     'link': link,
#                     'link_hash':link_hash
#                 }
#                 filtered_products.append(product)
#                 print(product)
#             except Exception as e:
#                 print(f"提取商品时出错: {e}")
#
#         save_to_db(filtered_products)
#
#         try:
#             next_button = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, ".pn-next"))
#             )
#             next_button.click()
#         except:
#             print("未找到下一页按钮，爬取结束")
#             break

    driver.quit()

def tb_update_price(good,url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # options.add_argument("--headless")  # 无头模式
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    # driver_path = "/usr/bin/chromedriver"

    # 初始化 Selenium 驱动
    # driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver =webdriver.Chrome(options=options)

    try:
        # 反爬机制
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                               {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
        driver.get(url)
        driver.maximize_window()

        # 手动扫码登录
        # with open("tb_cookies.pkl", "rb") as file:
        #     cookies = pickle.load(file)
        #     for cookie in cookies:
        #         driver.add_cookie(cookie)
        #
        # driver.refresh()  # 刷新页面以应用 Cookies
        wait = WebDriverWait(driver, 5)
        input("请先登录...后按回车键继续")
        time.sleep(random.uniform(3, 5))  # 额外等待时间，确保 JavaScript 内容加载完成

        # 获取页面 HTML 源代码
        html = driver.page_source
        doc = pq(html)

        current_price = doc('div.originPrice--UnZ18wCd .priceText--gdYzG_l_').eq(0).text()
        # current_price = doc('div.extraPrice--Y7SiNGXT .priceText--gdYzG_l_.extraPriceText--aysuZjG_').text()

        if current_price:
            good.price=current_price
            good.save()
        else:
            # 尝试获取单一价格
            current_price = doc('div.highlightPrice--OOP9oDP8 .text--fZ9NUhyQ').eq(0).text()
            if current_price:
                good.price=current_price
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


# def jd_update_price(good, url):
#     """从京东获取商品价格并更新。"""
#
#     # 指定浏览器和驱动路径
#     # driver_path = "/usr/bin/chromedriver"  # 替换为实际的 ChromeDriver 路径
#     #
#     # # 如果 Cookies 文件不存在，启动有头模式保存 Cookies
#     # if not os.path.exists("jd_cookies.pkl"):
#     #     save_jd_cookies(driver_path)
#
#     # 配置 Chrome 浏览器选项
#     chrome_options = webdriver.ChromeOptions()
#     # chrome_options.add_argument("--headless")  # 无头模式
#     # chrome_options.add_argument("--disable-gpu")
#     # chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     )
#
#     # 初始化 Selenium 驱动
#     # driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
#     driver = webdriver.Chrome(options=chrome_options)
#     try:
#         # 打开指定 URL
#         driver.get(url)
#         driver.maximize_window()
#         # 加载保存的 Cookies
#         # with open("jd_cookies.pkl", "rb") as file:
#         #     cookies = pickle.load(file)
#         #     for cookie in cookies:
#         #         # if "domain" in cookie:
#         #         #     cookie["domain"] = ".jd.com"  # 确保域名正确
#         #         driver.add_cookie(cookie)
#         #
#         # driver.refresh()  # 刷新页面以应用 Cookies
#         input("请先登陆...")
#         time.sleep(random.uniform(2, 5))  # 模拟人工延迟
#
#         print("Successfully loaded the product page, fetching the price...")
#         driver.get(url)
#         # 定位并获取价格元素
#         try:
#             price_element = driver.find_element(By.CSS_SELECTOR, ".price")
#             price_float = float(price_element.text)
#         except NoSuchElementException:
#             price_element = driver.find_element(By.CSS_SELECTOR, ".p-price")
#             price_cleaned = price_element.text.replace('￥', '').strip()
#             price_float = float(price_cleaned)
#
#         print(f"Current Product Price: {price_float}")
#
#         # 更新商品价格并保存
#         good.modify_price(price_float)
#         good.save()
#
#         # 将价格加入历史价格表
#         product_new_price = Prices(product=good, price=price_float)
#         product_new_price.save()
#
#     except NoSuchElementException:
#         print("Error: Unable to find the price element on the page.")
#     finally:
#         driver.quit()

def jd_update_price(good,url):
    driver = ChromiumPage()
    try:
        # Open the specified URL
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Simulate a human interaction delay
        input("请先登录后按回车键继续")

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

        good.price=price_float
        good.save()
        # 将价格加入历史价格表
        product_new_price = Prices(product=good, price=price_float)
        product_new_price.save()

    except ElementNotFoundError:
        print("Error: Unable to find the price element on the page.")
    finally:
        driver.quit()  # Ensure the browser closes after the task

def save_tb_cookies():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})

    try:
        driver.get("https://www.taobao.com")
        driver.maximize_window()

        # 等待用户手动登录
        # input("请手动完成登录后按 Enter 键继续...")
        time.sleep(20)

        # 保存 Cookies 到文件
        with open("tb_cookies.pkl", "wb") as file:
            pickle.dump(driver.get_cookies(), file)

        print("Cookies 已保存")
    finally:
        driver.quit()

def save_jd_cookies(driver_path):
    """启动有头模式浏览器保存用户登录的 Cookie。"""
    options = webdriver.ChromeOptions()
    options.add_argument("--remote-debugging-port=9222")  # 开启远程调试
    options.add_argument("--disable-dev-shm-usage")  # 使用 /dev/shm 以避免共享内存不足
    options.add_argument("--disable-extensions")  # 禁用扩展
    options.add_argument("--disable-software-rasterizer")  # 禁用软件光栅化器
    options.add_argument("--disable-setuid-sandbox")  # 禁用 setuid 沙盒
    options.add_argument("--remote-debugging-port=9222")  # 远程调试端口
    options.add_argument("--single-process")  # 强制单进程模式

    driver = webdriver.Chrome(service=Service(driver_path), options=options)

    try:
        # 打开京东主页并等待用户登录
        driver.get("https://www.jd.com")
        driver.maximize_window()
        print("请手动完成登录...")
        time.sleep(20)
        # 保存 Cookies 到文件
        with open("jd_cookies.pkl", "wb") as file:
            pickle.dump(driver.get_cookies(), file)
        print("Cookies 已保存")
    finally:
        driver.quit()

