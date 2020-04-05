import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, session, logging, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt

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

class Register(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(300))

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
    


model = pickle.load(open('model.pkl', 'rb'))




@app.route('/', methods=['POST','GET'])
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
                return render_template('register.html', text = 'success')
               
            return render_template('register.html', text = 'The email is already associated with another account')
            
        else:
            return render_template('register.html', text = 'The passwords do not match')


if __name__ == "__main__":
    app.run()