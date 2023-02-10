import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
data = pd.read_csv('Hyderabad.csv')
model = pickle.load(open('model-2.pkl','rb'))
le = LabelEncoder()
x = le.fit_transform(data['Location'])

@app.route('/') 
def index():

    locations = sorted(data['Location'].unique())
    return render_template('html.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    area = request.form.get('area')
    bhk = request.form.get('bhk')
    ne = request.form.get('toggle')
    sc = request.form.get('sec')
    ind = request.form.get('ind')
    ca = request.form.get('car')
    lt = request.form.get('lift')
    n=0
    for i in range(414):
         if data['Location'][i] == location:
            n = i
            break
    if sc == 'on':
        sec = 1
    else:
        sec = 0
    if lt == 'on':
        lift = 1
    else:
        lift = 0
    if ca == 'on':
        car = 1
    else:
        car = 0
    if ind == 'on':
        indd = 1
    else:
        indd = 0
    if ne == 'on':
        new = 1
    else:
        new = 0
    print(area,x[n],bhk,new,sec,car,indd,lift)
    input = pd.DataFrame([[area,x[n],bhk,new,sec,car,indd,lift]], columns=['Area','Location','No. of Bedrooms','Resale','24X7Security','PowerBackup','CarParking','LiftAvailable'])
    pred = model.predict(input)[0]*1e6
    return str(pred)


if __name__ == "__main__":
    app.run(debug = True, port=5000)