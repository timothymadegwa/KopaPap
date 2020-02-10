import requests
import json

#performs authentication
class authenticate: 

    def __init__(self,): 
        self.client_id = 'bb473ed6-c10f-4765-a97b-735b659dea59'
        self.client_secret = '4ad025f3-5ff2-4919-8286-8bb4f80cec0e'
        self.token_endpoint = 'https://api.fusionfabric.cloud/login/v1/sandbox/oidc/token'
        
    def get_token(self): 
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        data = {
            'grant_type'     : 'client_credentials',
            'client_id'      : self.client_id,
            'client_secret'  : self.client_secret
        }
        r = requests.post(self.token_endpoint, data=data, headers=headers)
        response =  r.json()
        print(r.status_code)
        if (r.status_code is 200):         
            token = response['access_token']
        return  token

class Query_api:
    def __init__(self, token,payload): 
        self.base_url = 'https://api.fusionfabric.cloud/retail-banking/customers/v1/personal-customers/search?limit=1&offset=1'
        self.token = token 
        self.payload = payload

    def connect_endpoint(self):
        self.url = self.base_url
        headers = {
            'Authorization': 'Bearer ' + self.token,  
            'Content-Type' : 'application/json',
            'Accept' : 'application/json',
            }  
        response = requests.post(self.url,data=self.payload,headers=headers)
        print(response.status_code)
        print(response.json())
        cc = response.json()
        return cc

if __name__ == "__main__":
    a = authenticate()
    token = a.get_token()
    data ="{\n  \"firstName\": \"EMANUEL\",\n  \"lastName\" : \"SHOWN\",\n  \"phoneNumber\": \"0044 01753 573244\",\n  \"emailAddress\": \"OfficeAdmin@OfficeAddress.com\",\n  \"identificationNumber\": \"WWW12\",\n  \"dateOfBirth\": \"1979-05-01\"\n}"
    tcm = Query_api(token,data)
    print(tcm.connect_endpoint())
