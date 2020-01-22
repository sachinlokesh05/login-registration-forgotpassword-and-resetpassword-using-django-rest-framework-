import json
import requests
ENDPOINT = 'http://127.0.0.1:8788/login/'

# headers = {
#     'Content-Type': 'application/json'
# }
headerss = {
    'Content-Type': 'application/json',
    # 'Accept': 'application/json'
    #    'Authorization':'Token d070b44498fd12728d1e1cfbc9aa5f195600d21e'
}

data = {
    "username": "sachin",
    "password": "123"
}

response = requests.post(ENDPOINT, data=json.dumps(data), headers=headerss)
print(response)
# response.json()
