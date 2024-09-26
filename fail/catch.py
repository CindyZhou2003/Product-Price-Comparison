import pickle
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# 在浏览器中登录淘宝后，复制浏览器中的Cookie信息
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Cookie': 'cookie2=1a45b6c69ee7d43ff81962178a2906ed; t=f8e1102480b2dfc709e781b791b265ec; _tb_token_=ea575407ebe85; mtop_partitioned_detect=1; _m_h5_tk=68ac39a2817b8261b23e9ab948d500c3_1726998602578; _m_h5_tk_enc=529e7fa2e57e38c9981c7eb5900d5d0d; cna=6q52H9kVVx8CASeukTk/ql4H; thw=cn; xlly_s=1; _samesite_flag_=true; 3PcFlag=1726988533955; sgcookie=E100ObM8Osr2xLRpvc8SZEEi%2Fe3gG0ZV0x8T4NFow9rY0GCVivyKmAsV%2BXr8eh0qOGghMChqL2SAEfiB7dKES8CsdVwh8qJ137dV0cKbWKD2QdE%3D; wk_cookie2=1c693b012f5aae456d54df68627afa6f; wk_unb=UNaGsUSAqLrWag%3D%3D; unb=3619577491; uc1=cookie14=UoYcBber2N0xNw%3D%3D&existShop=false&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=UIHiLt3xThH8t7YQoFNq&pas=0&cookie15=V32FPkk%2Fw0dUvg%3D%3D; uc3=nk2=F6k3HS2jVzFJXL4KLHTfQJNqVp8%3D&id2=UNaGsUSAqLrWag%3D%3D&vt3=F8dD3iVGa5SEm5JkCiQ%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; csg=bbaa7a2a; lgc=t_1515297060224_0443; cancelledSubSites=empty; cookie17=UNaGsUSAqLrWag%3D%3D; dnk=t_1515297060224_0443; skt=917d5dfe10f49cfe; existShop=MTcyNjk4ODU2Mg%3D%3D; uc4=nk4=0%40FbMocxjedSYWx0uc0fq%2F9dSiKTx8aozjBu1LOWbKAg%3D%3D&id4=0%40UgGP9Tm3BsVbAFvtdrtDYGLGUYIT; tracknick=t_1515297060224_0443; _cc_=VFC%2FuZ9ajQ%3D%3D; _l_g_=Ug%3D%3D; sg=31f; _nk_=t_1515297060224_0443; cookie1=BxuUBHqY%2FYcLWKJK6ve1JZ5BwMo55RliSCLEKUgXNyc%3D; tfstk=f6ESnH4uFQA77mQP5pBq5H_hUpmC_WsZypMLIJKyp0nRdWNTN2uKTaVIRWPmJuozUSZQ_S63z2oRdWNTN25oUJ-K9RPIY2EETk9uc5te4_bupHiEv15NbGylEDmd_YieY0hoK-hpK9n5w8mnvs5NbGyuE5OcH36IvtixLAD-v4hdhmHiM3Hp2vdAhjDKvH3p2KdxLAR-eHFLHtMnMXh8rGkDxj25nUUUR3OiV8hXA8qje4Tuejtpvoa-PfIIGHKLcYwDqTLkfwlTSbuZsSI2VDwxdSgaP1t7OJegJqZBwTPTp7qjqc_FEVaYuPu7l_KIgukIWD3XpHebejP_VcI9Gx4YUyEuNptKEurZRf0fpH0EDluTW79hI-n-pW0gY1xowJegjPo1VCD7kRif42tZ13vpRKgMAxGNhtTH-jvPV7-7agkIyxD4Gt6X7xg-nxGNhtTH-4Hm3cWfhFkf.; isg=BLS05Yb7bggLtfrEPu9Fr2_JhXImjdh3LXTY904VQD_CuVQDdp2oB2p_OfFhRBDP'
# }
# 初始化浏览器
driver = webdriver.Chrome()

# 打开淘宝页面
driver.get('https://www.taobao.com')

# 等待用户手动登录
print("请手动登录淘宝...")
time.sleep(1)  # 给用户足够的时间进行手动登录

# 保存cookie
# cookies = driver.get_cookies()
# with open('taobao_cookies.pkl', 'wb') as file:
#     pickle.dump(cookies, file)

# 加载已保存的Cookies
with open('../catch/taobao_cookies.pkl', 'rb') as file:
    cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

# 刷新页面，验证是否已登录
driver.refresh()
time.sleep(1)

# 淘宝商品页面的URL
url = 'https://s.taobao.com/search?commend=all&ie=utf8&initiative_id=tbindexz_20170306&localImgKey=&page=1&q=%E5%A5%B3%E8%A3%85&search_type=item&sourceId=tb.index&spm=a21bo.jianhua%2Fa.201856.d13&ssid=s5-e&tab=all'
# 打开你想要抓取的商品搜索页面
driver.get(url)

# 发起请求
# response = requests.get(url, headers=headers)

time.sleep(5)
# 滚动页面，加载更多商品
for i in range(5):  # 可根据需要滚动多次加载更多商品
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(2)  # 每次滚动等待加载

# 检查请求是否成功
# if response.status_code == 200:
# print("请求成功，正在解析页面...")
# print(response.text)

# 获取页面的HTML内容
page_source = driver.page_source

# 解析HTML内容
soup = BeautifulSoup(page_source, 'html.parser')

# 查找商品信息
items = soup.find_all('div', class_='item J_MouserOnverReq')

for item in items:
    # 获取商品名称
    title = item.find('a', class_='J_ClickStat').get_text(strip=True)

    # 获取商品价格
    price = item.find('strong').get_text(strip=True)

    # 获取商品图片
    img = item.find('img')['data-src']

    # 获取店铺名称
    shop = item.find('a', class_='shopname').get_text(strip=True)

    # 打印获取到的信息
    print(f"商品名称: {title}")
    print(f"价格: {price}")
    print(f"图片链接: {img}")
    print(f"店铺: {shop}")
    print("-" * 40)
# else:
#     print(f"请求失败，状态码: {response.status_code}")
