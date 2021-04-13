import requests
import json
import time


local_url = "http://127.0.0.1:7000/api/model_deployment"
azure_url = "YOUR_AZURE_URL_PLUS_CODE"

data = [
    {
        'TransactionId': 'TransactionId_47357',
        'FraudResult': '0'
        
    }
]

r = requests.post(local_url, json=json.dumps(data))
print(r)
print(r.text)

r = requests.post(azure_url, json=json.dumps(data))
print(r)
print(r.text)
