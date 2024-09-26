import json
import random
import selenium
import time
import requests
import openpyxl
from jsonpath import jsonpath
from selenium import webdriver
from selenium.webdriver.common.by import By


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Cookie':'cna=6q52H9kVVx8CASeukTk/ql4H; thw=cn; xlly_s=1; wk_cookie2=1c693b012f5aae456d54df68627afa6f; wk_unb=UNaGsUSAqLrWag%3D%3D; lgc=t_1515297060224_0443; dnk=t_1515297060224_0443; tracknick=t_1515297060224_0443; cookie2=2c66d904f17ba073c2a17624303acfc8; t=f95ed79d24d3d617be179fc80a516394; _tb_token_=e7deebb8f137b; mtop_partitioned_detect=1; _m_h5_tk=4c3bf0ab755b854661cbc94ce2d60067_1727192719604; _m_h5_tk_enc=5923bedcb86d0824c233916fb5769bad; _samesite_flag_=true; 3PcFlag=1727184184424; isg=BPb2G_72jLMB9nhKUKWnSblzRyz4FzpRu57a-WDe6Vlqo5c9yKKLYT8au3_PDDJp; unb=3619577491; cancelledSubSites=empty; cookie17=UNaGsUSAqLrWag%3D%3D; _l_g_=Ug%3D%3D; sg=31f; _nk_=t_1515297060224_0443; cookie1=BxuUBHqY%2FYcLWKJK6ve1JZ5BwMo55RliSCLEKUgXNyc%3D; sgcookie=E100JWdpH%2FPeVHqZfFUoxEVc83xNARmuVFV5jRXdFfZ8utRQSSsytpnbp4QeKTAPAcO3PnTCB1znmG6%2BLNeXxPAo9jEBiqY2ivhV1wlWWIefdBw%3D; havana_lgc2_0=eyJoaWQiOjM2MTk1Nzc0OTEsInNnIjoiMzUwZmZkNzk1NjUxZGU1YjgwNDczZWJmMjAzMTRiMDAiLCJzaXRlIjowLCJ0b2tlbiI6IjFFd0RVNHVXdWNYUWNDS19nemVSVFJRIn0; _hvn_lgc_=0; havana_lgc_exp=1758288212739; cookie3_bak=2c66d904f17ba073c2a17624303acfc8; cookie3_bak_exp=1727443412740; uc1=cookie14=UoYcBD%2BfZIY9vg%3D%3D&existShop=false&pas=0&cookie15=V32FPkk%2Fw0dUvg%3D%3D&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C; sn=; uc3=lg2=UtASsssmOIJ0bQ%3D%3D&nk2=F6k3HS2jVzFJXL4KLHTfQJNqVp8%3D&id2=UNaGsUSAqLrWag%3D%3D&vt3=F8dD3iVEayqTVDd0AMI%3D; csg=da412fee; env_bak=FM%2BgywHD48I1%2FH%2BP9E8qUEZcnZAsrJfZFpwMv%2BKxNwOq; skt=1851aa5166979508; existShop=MTcyNzE4NDIxMg%3D%3D; uc4=id4=0%40UgGP9Tm3BsVbAFvtdrtCS%2BW4SG9d&nk4=0%40FbMocxjedSYWx0uc0fq%2F9dSiKTx8aozjB%2FhuU3xzcg%3D%3D; _cc_=URm48syIZQ%3D%3D; tfstk=g6-iLwZIfF7sOL4CGvSso_rN7sgK6Rsf1IEAMiCq865CD1K9WEYHFIfthVs9-sAet17tCdQ0mKfCD1K9WEYHsCrAWIKDRovWhhH1DAs6CisqwbnJid91ceuKFPD8LMWJLRrq21Z9BbsqwbnpkmN27i8AeJr_xp5CntrN0IoFT66cgtRV_wPFETsVgIRqYJWAUPPV_lkHL66V0skOQx11WZxE19bWrdxIoHWGS_JN_dpMYmQ35pC30o-HWZCri6q40HXMdlMa5u0AaU1Oy_OEvljDLtAhyFcujIv2FE7Hm5k9aKR6xGsokA_k8eLRSecam6KOnaSV--r2Kd5pZhjr4WXB8dL2fC200Ot92Zf5-xrfkM-RzURghY9FbtRfPnh7f1J2F3TRqcV5IeJlxgrL8zRd4o6EHHzblNWCK_n9AgGBT27zQvD3zX7NdOyEKv4blNWCK_HnKzyf796aL',
    'Referer':'https://s.taobao.com/'
}
def search_data(search):
    # driver.find_element(By.XPATH, '//a[@class="sn-login"]').click()
    # driver.find_element(By.XPATH, '//i[@class="iconfont icon-qrcode"]').click()

    time.sleep(10)

    driver.find_element(By.XPATH, '//input').send_keys(search)
    driver.find_element(By.XPATH, '//div[@class="rax-view-v2 SearchInput--searchButton"]').click()

    driver.implicitly_wait(3)
    url='https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0'
    response = requests.get(url,headers=headers)

    data = response.text.replace('mtopjsonp\d+\((.*)\)','')[:-1]
    json_data = json.loads(data)

    goodlist = jsonpath(json_data,'$.data.itemsArray')[0]
    print(goodlist)
    # for item in goodlist:
    #     print(item)



if __name__ == '__main__':
    search='手机'

    driver=webdriver.Chrome()
    driver.get('https://www.tmall.com/')
    time.sleep(random.uniform(2, 5))
    driver.maximize_window()
    search_data(search)
