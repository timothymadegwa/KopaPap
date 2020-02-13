import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from custdetails import authenticate, Querycust_api
from searchcust import AuthenticateSearch, QuerySearchApi

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
    data = [*request.form.values()]
    print(data)
    first, last, tel, email, id_num, dob = data

    a = AuthenticateSearch('config.csv')
    token = a.get_token()
    data ="{\n  \"firstName\": \"EMANUEL\",\n  \"lastName\" : \"SHOWN\",\n  \"phoneNumber\": \"0044 01753 573244\",\n  \"emailAddress\": \"OfficeAdmin@OfficeAddress.com\",\n  \"identificationNumber\": \"WWW12\",\n  \"dateOfBirth\": \"1979-05-01\"\n}"
    tcm = QuerySearchApi(token,data)
    results = tcm.connect_endpoint()
    results = results['items'][0]
    print(results['customerId'])
    return render_template('search.html', text = 'The customer id is {} '.format(results['customerId']))

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    
    features = [*request.form.values()]
    customer_id = features[0]
    print(customer_id)
    features = features[1:]
    features = [*map(float,features)]
    print(features)
    

    a = authenticate('config.csv')
    response,token = a.get_token()
    print(response.status_code)
    method = 'GET'
    endpoint = 'personal-customers'
    endpoint2 = '/'+customer_id
    payload = ''
    additional_headers = {}
    params = {}
    config_file = 'config.csv'
    tcm = Querycust_api(config_file, token, method, endpoint,endpoint2, payload, additional_headers, params)
    response2 = tcm.connect_endpoint()
    response2 = response2.json()
    title = response2['title']
    f_name = response2['firstName']
    l_name = response2['lastName']
    gender = response2['gender']
    if gender == 'MALE':
        features.append(1)
    else:
        features.append(0)
    

    features = np.array([features])
    print(features)

    prediction = model.predict_proba(features)
    

    output = round((prediction[0][1])*100,2)

    return render_template('report.html', text='Client {} : Probability of repayment for {} {} {} is: {} %'.format(customer_id, title, f_name, l_name,output))

if __name__ == "__main__":
    app.run(debug=True)
