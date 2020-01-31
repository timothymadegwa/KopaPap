import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

#to be defined!
def features_prep(array):
    return array

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    features = np.array([float(x) for x in request.form.values()])
    features = [features]
    final_features = features_prep(features)
    prediction = model.predict_proba(final_features)
    

    output = round((prediction[0][1])*100,2)

    return render_template('index.html', prediction_text='Probability of repayment is: {} %'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
