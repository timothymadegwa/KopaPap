# importing relevant libraries
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression

# reading/loading in the training data
data = pd.read_csv('data/train.csv')

# replacing missing data with the modal value
data.Credit_History.fillna(data.Credit_History.mode()[0],inplace=True)
data.Gender.fillna(data.Gender.mode()[0],inplace=True)
data.Married.fillna(data.Married.mode()[0],inplace=True)
data.Dependents.fillna(data.Dependents.mode()[0],inplace=True) 
data.Self_Employed.fillna(data.Self_Employed.mode()[0],inplace=True) 

# changing the format for '3+' dependants
data.Dependents = data.Dependents.replace('3+','3')

# filling other missing data with the mean
data = data.fillna(data.mean())

# creating mappers for the different columns
gender_mapper = {'Male':1, 'Female':0}
married_mapper = {'Yes':1, 'No':0}
educ_mapper = {'Graduate':1, 'Not Graduate':0}
self_emp_mapper = {'Yes':1, 'No':0}
prop_area_mapper = {'Semiurban':0, 'Urban':1, 'Rural':2}
loan_mapper = {'Y':1, 'N':0}

# mapping the data to categorical values
data.Gender = data.Gender.map(gender_mapper)
data.Married = data.Married.map(married_mapper)
data.Education = data.Education.map(educ_mapper)
data.Self_Employed = data.Self_Employed.map(self_emp_mapper)
data.Property_Area = data.Property_Area.map(prop_area_mapper)
data.Loan_Status = data.Loan_Status.map(loan_mapper)

# converting dependants to interger values
data.Dependents = data.Dependents.astype(int)

# creating an income to loan ratio
data['income_to_loan'] = data['ApplicantIncome'] / data['LoanAmount']

# dropping the loan ID column
data.drop('Loan_ID', axis=1, inplace=True)

# isolating the loan status (target) values
target = data.Loan_Status

# dropping the loan status from original dataset
features = data.drop('Loan_Status',axis=1)

# creating the features to be used for training
features = data[['Married', 'Dependents', 'Education', 'Self_Employed', 'Credit_History', 
                'Property_Area','ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
                'Loan_Amount_Term', 'income_to_loan', 'Gender']]

# Creating an instance of logistic regression
lr = LogisticRegression(C= 0.1, solver = 'liblinear', warm_start = True)

# training the model using logistic regression
lr.fit(features, target)

# saving the model as a pickle file
pickle.dump(lr, open('model.pkl','wb'))
