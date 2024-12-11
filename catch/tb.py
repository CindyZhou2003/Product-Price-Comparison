import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
import csv

# 输入“关键词”，搜索，并进行首次爬取
def search_goods(KEYWORD, start_page, total_pages):

    print('正在搜索: ')
    # 找到搜索“输入框”
    input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
    # 找到“搜索”按钮
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
    # 输入框写入“关键词KeyWord”
    input.send_keys(KEYWORD)
    # 点击“搜索”按键
    submit.click()
    # 搜索商品后会再强制停止5秒，如有滑块请手动操作
    # time.sleep(5)

    # 如果不是从第一页开始爬取，就滑动到底部输入页面然后跳转
    if start_page != 1:
        # 滑动到页面底端
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 滑动到底部后停留3s
        time.sleep(3)
        # 找到输入“页面”的表单，输入“起始页”
        pageInput = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="pageContent"]/div[1]/div[3]/div[4]/div/div/span[3]/input')))
        pageInput.send_keys(start_page)
        # 找到页面跳转的“确定”按钮，并且点击
        admit = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="pageContent"]/div[1]/div[3]/div[4]/div/div/button[3]')))
        admit.click()

    # 获取商品信息
    get_goods(start_page)

    # 翻页操作
    for i in range(start_page + 1, total_pages + 1):
        page_turning(i)

# 翻页函数
def page_turning(page_number):
    print('正在翻页: ', page_number)

    # 强制等待几秒后翻页
    time.sleep(random.uniform(3, 5))

    # 找到“下一页”的按钮并点击
    submit = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button.next-btn.next-medium.next-btn-normal.next-pagination-item.next-next')))
    # submit.click()
    # 使用 JavaScript 点击
    driver.execute_script("arguments[0].click();", submit)

    # 判断页数是否相等
    # wait.until(EC.text_to_be_present_in_element(
    #     (By.XPATH, '//*[@id="search-content-leftWrap"]/div[3]/div[4]/div/div/span[1]/em'), str(page_number)))
    time.sleep(random.uniform(1, 2))
    print('翻页成功')
    # 获取商品信息
    get_goods(page_number)

# 获取每一页的商品信息；
def get_goods(page):

    # 获取商品前固定等待10秒,刷新/滑动界面，使所有信息都加载完成
    time.sleep(random.uniform(2, 5))
    print('界面加载完毕，即将开始爬取')
    # if input('确认界面加载完毕，输入数字“1”开始爬取-->') == 1:
    #     pass
    # 滚动页面，模拟慢慢滚动到页面底部
    screen_height = driver.execute_script("return window.innerHeight")  # 获取浏览器视口高度
    scroll_height = driver.execute_script("return document.body.scrollHeight")  # 获取页面总高度
    current_position = 0  # 当前滚动位置

    # 滚动到页面底部，模拟慢慢滚动
    while current_position < scroll_height-screen_height:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        current_position += screen_height
        time.sleep(random.uniform(2, 5))

    html = driver.page_source
    doc = pq(html)
    # 提取所有商品的共同父元素的类选择器
    items = doc('div.contentInner--xICYBlag > a').items()

    for item in items:
        # 定位商品标题
        title = item.find('.title--qJ7Xg_90 span').text()
        # 定位价格
        price_int = item.find('.priceInt--yqqZMJ5a').text()
        price_float = item.find('.priceFloat--XpixvyQ1').text()

        try:
            # 尝试转换为浮点数
            if price_int and price_float:
                price = float(f"{price_int}{price_float}")
            else:
                price = 0.0

        except ValueError:
            # 如果转换失败，将价格设为 0.0
            price = 0.0

        # 定位交易量
        deal = item.find('.realSales--XZJiepmt').text()
        # 定位所在地信息
        location = item.find('.procity--wlcT2xH9 span').text()
        # 定位店名
        shop = item.find('.shopNameText--DmtlsDKm').text()
        # 定位包邮的位置
        postText = item.find('.subIconWrapper--Vl8zAdQn ').text()
        postText = "包邮" if "包邮" in postText else "/"
        # 定位商品url
        # t_url = item.find('.Card--doubleCardWrapper--L2XFE73')
        # t_url = t_url.attr('href')
        t_url = item.attr('href')
        link="https:"+t_url
        # print(t_url)
        # 定位店名url
        shop_url = item.find('.TextAndPic--grkZAtsC a')
        shop_url = shop_url.attr('href')
        # print(shop_url)
        # 定位商品图片url
        img = item.find('.mainPicWrapper--qRLTAeii img')
        img_url = img.attr('src')
        # print(img_url)

        # 构建商品信息字典
        product = {
            'title': title,
            'price': price,
            'deal': deal,
            'shop': shop,
            'link': link,
            'img': img_url
        }
        print(product)

        # 将商品信息写入CSV文件
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=product.keys())
            writer.writerow(product)


if __name__ == '__main__':

    # 启动ChromeDriver服务
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)

    # 反爬机制
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
    driver.get('https://www.taobao.com')
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # 手动扫码登录
    input("请在浏览器中扫码登录，完成后按回车继续...")

    # 关键词列表
    # keywordbox = [ '电脑', '办公', '文具','家电', '数码', '家具', '手机', '家装', '女装','配饰',
    #                '女鞋','男装', '运动', '珠宝', '箱包', '食品', '生鲜', '母婴', '童装',
    #               '潮玩', '美妆', '洗护','宠物', '图书', '鲜花']
    # '玩偶','礼物','零食','耳机','电吹风','娱乐','烘焙工具', '户外装备', '露营', '帐篷', '汽车配件',
    # '充电器', '座垫', '美容', '美甲','剃须刀', '按摩器', '摆件',
    # '墙贴',  '游戏机', '音响设备',  '智能手环', '保健品', '智能家居', '节日装饰',
    # '维生素', '办公设备', '打印机', '扫描仪', '投影仪', '跑步机', '瑜伽垫',
    #
    #         '彩灯', '宠物用品', '宠物玩具', '宠物粮食', '行用品',  '健身器材', '哑铃',
    #         '旅行箱', '床上用品', '衣架',  '水杯', '记事本','厨房用品',


    keywordbox = [
        '帽子'
    ]

    # 设置CSV文件名称
    csv_filename = 'tb.csv'

    # 初始化CSV文件，准备写入表头
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=['title', 'price', 'deal', 'shop', 'link', 'img'])
        if file.tell() == 0:
            csv_writer.writeheader()

    # 遍历每个关键词进行爬取
    for KEYWORD in keywordbox:
        print(f"开始爬取关键词: {KEYWORD}")
        search_goods(KEYWORD, 1,2)
        print(f"关键词 {KEYWORD} 的数据已保存到 {csv_filename}")
        driver.get('https://www.taobao.com') # 回到淘宝网首页开始搜索

    # 关闭浏览器
    driver.quit()
    print(f"所有关键词数据已爬取并存储成功：{csv_filename}")
