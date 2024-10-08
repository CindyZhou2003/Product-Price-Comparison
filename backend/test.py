import requests

# Define the URL and the payload
# url = "http://127.0.0.1:8000/backend/login"
# payload = {
#     # "email": "12345@163.com",
#     # "username":"ACD",
#     # "password": "sf12343"
#     "username":"zhouxinyi5277",
#     "password": "zxy123"
# }
#
# # Send a POST request to the server
# response = requests.post(url, json=payload)
#
# # Print the response from the server
# print("Status Code:", response.status_code)
# print("Response Body:", response.json())


import requests

# Define the URL and the payload
url = "http://127.0.0.1:8000/backend/search_products"
params = {
    "search": "洗发水",
}

# Send a GET request with URL parameters
response = requests.get(url, params=params)

# 检查请求是否成功
if response.status_code == 200:
    response_data = response.json()  # 将响应内容转换为 JSON 格式
    # 检查返回的状态是否成功
    if response_data.get("status") == "ok":
        products = response_data.get("products", [])  # 提取 products 列表
        print(f"Found {len(products)} products matching the search criteria.")
        # 打印每个产品的详细信息
        for product in products:
            print(f"ID: {product['id']}, Title: {product['title']}, Price: {product['price']}, "
                  f"Comments: {product['comments']}, Shop: {product['shop']}, Platform: {product['platform']}")
    else:
        print(f"Error: {response_data.get('message')}")
else:
    print(f"Failed to get response. Status Code: {response.status_code}")
