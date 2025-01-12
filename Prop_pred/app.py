from flask import Flask, request, jsonify, render_template,url_for
import pickle
import numpy as np

app = Flask(__name__)

with open('pred.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    area = float(request.form['area'])
    rooms = int(request.form['rooms'])

    features = np.array([[area, rooms]])

    prediction = model.predict(features)

    return render_template('index.html', 
                           prediction_text=f'price: ${prediction[0]:,.2f}')

if __name__ =="__main__":
    app.run(debug=True)