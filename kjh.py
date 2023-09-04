import requests
credentials = {
        "login" : "1",
        "password": "9764"
    }
resp = requests.get(url="http://localhost:5003/login", params=credentials)

data = resp

print(data)