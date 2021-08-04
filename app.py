# importing relevant libraries
import numpy as np
from flask import Flask, request, render_template
import pickle

# create an instance of a flask app
app = Flask(__name__)

# load our pre-trained model
model = pickle.load(open('model.pkl', 'rb'))

# hypothetical currency conversion
kes_to_usd = 100

# Creating a route for the home page
@app.route('/')
def home():
    return render_template("index.html")

# creating a route for the predict page
@app.route('/predict',methods=['POST', 'GET'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # extraction of the form values
    features = [*request.form.values()]

    # extract the amount 
    amt = features[8]
    
    try:
        # converting all values in the list to floats
        features = [*map(float,features)]
    except ValueError:
        # incase of a value error, it redirects to the home page
        return render_template('index.html', error=1, warning_text ="kindly enter a integer values in the relevant fields")
    
    # calculating the loan to income ratio
    features.append((features[6]*12)/features[8])
    
    # converting the list to a numpy array
    features = np.array([features])

    # Converting values to kes
    features[0][6] = (features[0][6]*12)/kes_to_usd
    features[0][7] = (features[0][7]*12)/kes_to_usd
    features[0][8] = features[0][8]/kes_to_usd

    # using the pre-trained model to make predictions
    prediction = model.predict_proba(features)
        
    # converting to a % age and rounding off to 2 dp
    output = round((prediction[0][1])*100,2)

    return render_template('report.html', text='The probability of repayment for on a loan of KES {} by the Client is: {} %'.format(amt, output))
    

if __name__ == "__main__":
    app.run(debug=True)
