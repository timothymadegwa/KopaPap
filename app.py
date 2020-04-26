import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import json
import pickle
from custdetails import authenticate, Querycust_api
from searchcust import AuthenticateSearch, QuerySearchApi

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
kes_to_usd = 100
active = 1

@app.route('/')
def predict_home():
    return render_template('index.html')

@app.route('/search',methods=['POST','GET'])
def search():
    try:
        data = []
        data = [*request.form.values()]
        print(data)
        first, last, tel, email, id_num, dob = data
        first = first.upper()
        last = last.upper()
        a = AuthenticateSearch('config.csv')
        token = a.get_token()
        data ={"firstName": first,"lastName" : last,"phoneNumber": tel,"emailAddress": email,"identificationNumber":id_num,"dateOfBirth": dob}
        data  = json.dumps(data)
        tcm = QuerySearchApi(token,data)
        results = tcm.connect_endpoint()
        try:
            results = results['items'][0]
            cust_id = results['customerId']
            return render_template('searchreport.html', text = 'The customer id is {} '.format(cust_id))
        except (TypeError,KeyError):
            return render_template('search.html', warning_text = 'Invalid customer credentials', error=1)
    except ValueError:
        return render_template('search.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    features = [*request.form.values()]
    customer_id = features[0]
    print(customer_id)
    amt = features[9]
    features = features[1:]
    try:
        features = [*map(float,features)]
    except ValueError:
        return render_template('index.html', error=1, warning_text ="kindly enter a integer values in the relevant fields")
    features.append((features[6]*12)/features[8])
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
    try:
        title = response2['title']
        f_name = response2['firstName']
        l_name = response2['lastName']
        gender = response2['gender']
    except KeyError:
        return render_template('index.html', warning_text = 'Client {} does not exist'.format(customer_id), error=1)
    if gender == 'MALE':
        features.append(1)
    else:
        features.append(0)
        

    features = np.array([features])
    features[0][6] = (features[0][6]*12)/kes_to_usd
    features[0][7] = (features[0][7]*12)/kes_to_usd
    features[0][8] = features[0][8]/kes_to_usd
    print(features)

    prediction = model.predict_proba(features)
        

    output = round((prediction[0][1])*100,2)

    return render_template('report.html', text='Client {} : Probability of repayment for {} {} {} on a loan of KES {} is: {} %'.format(customer_id, title, f_name, l_name, amt, output))
    

if __name__ == "__main__":
    app.run(debug=False)
