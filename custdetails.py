#API Handling Libraries -- requests, re, json
import requests
import json
#pandas
import pandas as pd
#performs authentication
class authenticate: 
    '''
    config_file: A csv that stores the client id, client secret, reply url, token endpoint and base url
    '''
    def __init__(self,config_file): 
        self.df = pd.read_csv(config_file)
        self.client_id = self.df['application_id'].values[0]
        self.client_secret = self.df['access_key'].values[0]
        self.reply_url = self.df['reply_url'].values[0]
        self.token_endpoint = self.df['token_endpoint'].values[0]
        self.base_url = self.df['base_url'].values[0]
        
    def get_token(self): 
        headers = {
        }
        data = {
            'grant_type'     : 'client_credentials',
            'client_id'      : self.client_id,
            'client_secret'  : self.client_secret
        }
        response = requests.request('POST', self.token_endpoint, data=data, headers=headers)
        cleaned_response = response.text.replace(':null', ':"null"')
        response_dict = eval(cleaned_response)
        token = response_dict['access_token']
        return response, token

class Querycust_api: 
    def __init__(self, config_file, token, method, endpoint,endpoint2, payload, additional_headers={}, params = None): 
        self.df = pd.read_csv(config_file)
        self.base_url = self.df['base_url'].values[0]
        self.token = token 
        self.endpoint_type = method
        self.endpoint = endpoint 
        self.endpoint2 = endpoint2
        self.additional_headers = additional_headers
        self.params = params
    
    def connect_endpoint(self):
        self.url = self.base_url + self.endpoint + self.endpoint2
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type' : 'application/json',
            }
        for key in self.additional_headers.keys():
            headers[key] = self.additional_headers[key]
        stringified_payload = json.dumps(payload)
        response = requests.request(self.endpoint_type, self.url, params=self.params, data=stringified_payload,headers=headers)
        return response

if __name__ == "__main__":
    a = authenticate('config.csv')
    response,token = a.get_token()
    print(response.status_code)
    method = 'GET'
    endpoint = 'personal-customers'
    endpoint2 = '/FFDC01'
    payload = ''
    additional_headers = {}
    params = {}
    config_file = 'config.csv'
    tcm = Querycust_api(config_file, token, method, endpoint,endpoint2, payload, additional_headers, params)
    response2 = tcm.connect_endpoint()
    response2 = response2.json()
    print("Response: ",response2)
  



