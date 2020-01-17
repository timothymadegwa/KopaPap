import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression

data = pd.read_csv('data/train.csv')
data = data.fillna(data.mean())
data.Gender.fillna(data.Gender.mode()[0],inplace=True)
data.Married.fillna(data.Married.mode()[0],inplace=True)
data.Dependents.fillna(data.Dependents.mode()[0],inplace=True) 
data.Self_Employed.fillna(data.Self_Employed.mode()[0],inplace=True) 
data.Dependents = data.Dependents.replace('3+','3')

data.drop('Loan_ID', axis=1, inplace=True)
data = pd.get_dummies(data, drop_first=True)

target = data.Loan_Status_Y
features = data.drop('Loan_Status_Y',axis=1)

lr = LogisticRegression(C= 1, solver = 'lbfgs', warm_start = True)
lr.fit(features, target)
print(features.columns)


pickle.dump(lr, open('model.pkl','wb'))
