import numpy as np
#import pandas as pd
from flask import Flask, request, jsonify, render_template
#import json
#import os
import pickle
#from custdetails import authenticate, Querycust_api
#from searchcust import AuthenticateSearch, QuerySearchApi

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
kes_to_usd = 100
DEBUG = False

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search',methods=['POST','GET'])
def search():
    try:
        data = []
        data = [*request.form.values()]
        first, last, tel, email, id_num, dob = data
        first = first.upper()
        last = last.upper()
        if DEBUG:
            a = AuthenticateSearch('config.csv')
        else:
            a = AuthenticateSearch()
        token = a.get_token()
        data ={"firstName": first,"lastName" : last,"phoneNumber": tel,"emailAddress": email,"identificationNumber":id_num,"dateOfBirth": dob}
        data  = json.dumps(data)
        tcm = QuerySearchApi(token,data)
        results = tcm.connect_endpoint()
        try:
            results = results['items'][0]
            cust_id = results['customerId']
            return render_template('searchreport.html', client_id = cust_id)
        except (TypeError,KeyError):
            return render_template('search.html', warning_text = 'Invalid customer credentials', error=1)
    except ValueError:
        return render_template('search.html')


@app.route('/predict',methods=['POST', 'GET'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    features = [*request.form.values()]
    
    amt = features[8]
    
    try:
        features = [*map(float,features)]
    except ValueError:
        return render_template('index.html', error=1, warning_text ="kindly enter a integer values in the relevant fields")
    features.append((features[6]*12)/features[8])
    
    features = np.array([features])
    features[0][6] = (features[0][6]*12)/kes_to_usd
    features[0][7] = (features[0][7]*12)/kes_to_usd
    features[0][8] = features[0][8]/kes_to_usd

    prediction = model.predict_proba(features)
        

    output = round((prediction[0][1])*100,2)

    return render_template('report.html', text='The probability of repayment for on a loan of KES {} by the Client is: {} %'.format(amt, output))
    

if __name__ == "__main__":
    app.run(debug=True)
