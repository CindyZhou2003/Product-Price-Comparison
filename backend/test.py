import requests

# Define the URL and the payload
url = "http://127.0.0.1:8000/backend/login"
payload = {
    # "email": "12345@163.com",
    # "username":"ACD",
    # "password": "sf12343"
    "username":"zhouxinyi5277",
    "password": "zxy123"
}

# Send a POST request to the server
response = requests.post(url, json=payload)

# Print the response from the server
print("Status Code:", response.status_code)
print("Response Body:", response.json())
