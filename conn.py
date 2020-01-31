import requests

r=requests.get(url = 'https://api.fusionfabric.cloud/retail-banking/accounts/v1/accounts/accounts?customerId=” FFDC01”')
print(r.json())
