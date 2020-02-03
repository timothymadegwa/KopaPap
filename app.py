import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from custdetails import authenticate, Querycust_api

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    
    features = pd.DataFrame([*request.form.values()])
    customer_id = features[0:1].values[0,0]
    print(customer_id)
    features = features.T
    features = features.values[:,1:].astype(float)

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

    prediction = model.predict_proba(features)
    

    output = round((prediction[0][1])*100,2)

    return render_template('report.html', prediction_text='Client {} : Probability of repayment for {} {} {} is: {} %'.format(customer_id, title, f_name, l_name,output))

if __name__ == "__main__":
    app.run(debug=True)
