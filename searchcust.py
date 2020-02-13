import requests
import json
import pandas as pd

#performs authentication
class AuthenticateSearch: 

    def __init__(self,config_file):
        self.df = pd.read_csv(config_file)
        self.client_id = self.df['application_id'].values[0]
        self.client_secret = self.df['access_key'].values[0]
        self.token_endpoint = self.df['token_endpoint'].values[0]
        
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

class QuerySearchApi:
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
        cc = response.json()
        return cc

if __name__ == "__main__":
    a = AuthenticateSearch('config.csv')
    token = a.get_token()
    data ="{\n  \"firstName\": \"EMANUEL\",\n  \"lastName\" : \"SHOWN\",\n  \"phoneNumber\": \"0044 01753 573244\",\n  \"emailAddress\": \"OfficeAdmin@OfficeAddress.com\",\n  \"identificationNumber\": \"WWW12\",\n  \"dateOfBirth\": \"1979-05-01\"\n}"
    tcm = QuerySearchApi(token,data)
    results = tcm.connect_endpoint()
