import json

import requests

store_hash = 'rmz2xgu42d'
url = f'https://api.bigcommerce.com/stores/{store_hash}/v2/customers'

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Auth-Token": "hjmi4b9dsesuj1ybgeiampqofwgvvp1"
}

resp = requests.get(url, headers=headers)
print(resp)

new_user = requests.post(url, headers=headers, data=json.dumps({
    "email": "test1@test1.com",
    'first_name': "test1",
    "last_name": "test1"
}))

print(new_user)