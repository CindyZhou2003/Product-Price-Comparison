import random
import time
import csv
from DrissionPage import ChromiumPage
import os
import requests
import csv
from DrissionPage.errors import ElementNotFoundError

def catch(k,start,end):
    with open('../data/image_urls.csv', mode='a', encoding='utf-8', newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=['id', 'url'])
        # Only write the header if the file is empty
        if f.tell() == 0:
            csv_writer.writeheader()

        # Initialize the browser
        driver = ChromiumPage()

        time.sleep(random.uniform(1, 2))
        print("正在爬取中...")
        # Loop through 10 pages
        for i in range(start, end):  # 循环从 1 到 10（range(1, 11) 包含 1, 但不包括 11）
            driver.get(f'https://www.vcg.com/creative-image/zhengmianrenlian/?page={i}')
            time.sleep(random.uniform(2, 5))
            # Scroll down gradually
            for scroll_pos in range(1000, 12000, 1000):
                driver.scroll.to_location(0, scroll_pos)
                time.sleep(random.uniform(1, 2))

            # driver.scroll.to_bottom()  # Scroll to bottom to load all products
            time.sleep(random.uniform(2, 3))

            # Select all product elements
            pics = driver.eles('css:.galleryItem')

            print("Page"+str(i))

            # Extract data from each product
            for p in pics:
                """提取商品信息"""
                img = p.ele('css:.imgWaper img').attr('src')
                url = img

                # Create dictionary with extracted data
                dit = {
                    'id': k,
                    'url': url,
                }
                # Write the data to CSV
                csv_writer.writerow(dit)
                print(dit)
                k=k+1
            # Click the next page button
            # driver.ele('css:.paginationClickBox').click()

        driver.quit()

# 定义下载图片的函数
def download_image(url, output_folder, image_name):
    try:
        # 发送HTTP GET请求
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        # 保存图片
        with open(os.path.join(output_folder, image_name), "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"成功下载: {image_name}")
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {image_name}, 错误: {e}")

# 主逻辑
def download_images_from_csv(csv_file, output_folder, url_column):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 读取CSV文件
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            # 获取URL并生成文件名
            url = row[url_column]
            if url.strip():  # 确保URL非空
                image_name = f"image_{i+1}.jpg"  # 根据需要调整文件名规则
                download_image(url, output_folder, image_name)

if __name__ == "__main__":
    # 配置参数
    csv_file = "../data/image_urls.csv"  # 替换为你的CSV文件路径
    output_folder = "downloaded_images"  # 替换为你的目标文件夹路径
    url_column = "url"  # 替换为CSV文件中存放URL的列名
    # catch(1914,15,23)
    download_images_from_csv(csv_file, output_folder, url_column)
