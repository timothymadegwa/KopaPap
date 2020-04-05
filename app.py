import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, session, logging, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from db import Register,db

import json
import pickle
from custdetails import authenticate, Querycust_api
from searchcust import AuthenticateSearch, QuerySearchApi

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://timothy:Kibukamusoke1!@localhost/Kopapap'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lmane')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmed = request.form.get('confirm')
        if password == confirmed:
            secure_password = sha256_crypt(str(password))
            if db.session.query(Register).filter(Register.email == email).count() == 0:
                data = Register(fname,lname,email,secure_password)
                db.session.add(data)
                db.session.commit()
                return render_template('login.html')
               
            return render_template('register.html', text = 'The email is already associated with another account')
            
        else:
            return render_template('register.html', text = 'The passwords do not match')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #email_data = db.execute("SELECT email FROM users WHERE email=:email",{'email':email}).fetchone()
        #password_data = db.execute("SELECT password FROM users WHERE email:=email", {'email': email}).fetchone()

        #if email_data is None:
         #   return render_template('login.html', text = 'No account associated with {}, Kindly register'.format(email))
        #else:
         #   if sha256_crypt.verify(password,password_data):
          #      session['log'] = True
           #     return render_template('index.html')
            #else:
             #   return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('login.html')


@app.route('/search',methods=['POST','GET'])
def search():
    try:
        data = []
        data = [*request.form.values()]
        print(data)
        first, last, tel, email, id_num, dob = data

        a = AuthenticateSearch('config.csv')
        token = a.get_token()
        data ={"firstName": first,"lastName" : last,"phoneNumber": tel,"emailAddress": email,"identificationNumber":id_num,"dateOfBirth": dob}
        data  = json.dumps(data)
        tcm = QuerySearchApi(token,data)
        results = tcm.connect_endpoint()
        try:
            results = results['items'][0]
            cust_id = results['customerId']
            return render_template('search.html', text = 'The customer id is {} '.format(cust_id))
        except TypeError:
            return render_template('search.html', text = 'Invalid customer credentials')
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
