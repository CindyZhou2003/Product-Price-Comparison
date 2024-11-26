import requests
import os
import django
from django.utils.timezone import localtime

# Define the URL and the payload
# url = "http://127.0.0.1:8000/backend/login"
# payload = {
#     # "email": "12345@163.com",
#     # "username":"ACD",
#     # "password": "sf12343"
#     "username":"zhouxinyi5277",
#     "password": "zxy123"
# }
# url = "http://127.0.0.1:8000/backend/update_and_show_price"
# url = "http://127.0.0.1:8000/backend/update_and_show_price"
# url = "http://127.0.0.1:8000/backend/send_user_email"
url = "http://127.0.0.1:8000/backend/search_platform_products"
# params = {
#     "search":"https://detail.tmall.com/item.htm?priceTId=2147820017308929924073442e0193&utparam=%7B%22aplus_abtest%22%3A%22147faa88590dd67ced21724be9d95a99%22%7D&id=737835268170&ns=1&abbucket=11&xxc=taobaoSearch&skuId=5361326104000",
# }
payload = {
    # "user_id":"2"
    "search":"围巾",
    "platform":"淘宝"
}
# Send a POST request to the server
response = requests.post(url, json=payload)
# response = requests.get(url, params=params)
# Print the response from the server
print("Status Code:", response.status_code)
print("Response Body:", response.json())


# # Define the URL and the payload
# url = "http://127.0.0.1:8000/backend/search_products"
# params = {
#     "search": "洗发水",
# }
#
# # Send a GET request with URL parameters
#
#
# # 检查请求是否成功
# if response.status_code == 200:
#     response_data = response.json()  # 将响应内容转换为 JSON 格式
#     # 检查返回的状态是否成功
#     if response_data.get("status") == "ok":
#         products = response_data.get("products", [])  # 提取 products 列表
#         print(f"Found {len(products)} products matching the search criteria.")
#         # 打印每个产品的详细信息
#         for product in products:
#             print(f"ID: {product['id']}, Title: {product['title']}, Price: {product['price']}, "
#                   f"Comments: {product['comments']}, Shop: {product['shop']}, Platform: {product['platform']}")
#     else:
#         print(f"Error: {response_data.get('message')}")
# else:
#     print(f"Failed to get response. Status Code: {response.status_code}")



# url = "http://127.0.0.1:8000/backend/like"

# url ="http://127.0.0.1:8000/backend/get_favorites"
# params = {
#     "user_id":1,
# }
# payload = {
#     "user_id":1,
#     "id":1,
# }
# # Send a POST request to the server
# # response = requests.post(url, json=payload)
# response = requests.get(url, params=params)
# # Print the response from the server
# print("Status Code:", response.status_code)
# print("Response Body:", response.json())
