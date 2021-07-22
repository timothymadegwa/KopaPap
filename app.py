import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
kes_to_usd = 100
DEBUG = False

@app.route('/')
def home():
    return render_template("index.html")


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
