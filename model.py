import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression

data = pd.read_csv('data/train.csv')

data.Credit_History.fillna(data.Credit_History.mode()[0],inplace=True)
data.Gender.fillna(data.Gender.mode()[0],inplace=True)
data.Married.fillna(data.Married.mode()[0],inplace=True)
data.Dependents.fillna(data.Dependents.mode()[0],inplace=True) 
data.Self_Employed.fillna(data.Self_Employed.mode()[0],inplace=True) 
data.Dependents = data.Dependents.replace('3+','3')
data = data.fillna(data.mean())

gender_mapper = {'Male':1, 'Female':0}
married_mapper = {'Yes':1, 'No':0}
educ_mapper = {'Graduate':1, 'Not Graduate':0}
self_emp_mapper = {'Yes':1, 'No':0}
prop_area_mapper = {'Semiurban':0, 'Urban':1, 'Rural':2}
loan_mapper = {'Y':1, 'N':0}
data.Gender = data.Gender.map(gender_mapper)
data.Married = data.Married.map(married_mapper)
data.Education = data.Education.map(educ_mapper)
data.Self_Employed = data.Self_Employed.map(self_emp_mapper)
data.Property_Area = data.Property_Area.map(prop_area_mapper)
data.Loan_Status = data.Loan_Status.map(loan_mapper)

data.Dependents = data.Dependents.astype(int)

data.drop('Loan_ID', axis=1, inplace=True)
#data = pd.get_dummies(data, drop_first=True)

target = data.Loan_Status
features = data.drop('Loan_Status',axis=1)

features = data[['Married', 'Dependents', 'Education', 'Self_Employed', 'Credit_History', 
                'Property_Area','ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
                'Loan_Amount_Term','Gender']]

lr = LogisticRegression(C= 2, solver = 'lbfgs', warm_start = True)
lr.fit(features, target)

pickle.dump(lr, open('model.pkl','wb'))
