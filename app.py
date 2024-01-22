import pickle
from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd

app = Flask(__name__,static_url_path="/static")

model = pickle.load(open('UsedCarPricePredictor.pkl','rb'))

@app.route('/')

def home():
    return render_template('home.html')

@app.route('/predict_api',methods = ['POST'])
#@app.route('/predict_PostMan',methods = ['POST'])
def predict_api():
    # viaAPI = False
    # if request.json['data'] != None:
    #     data = request.json['data']
    #     viaAPI = True
    # else:
    #     data=[float(x) for x in request.form.values()]  

    Fuel_Type_Petrol = 0
    Fuel_Type_Diesel =0
    Transmission_Manual = 0 
    Transmission_Automatic = 0
    # Transmission_Automatic = request.form['optionsTransmisssion']
    # Transmission_Manual = not request.form['optionsTransmisssion']

    fuel_type = request.form.get('optionsFuel_Type')
    transmission = request.form.get('optionsTransmisssion')

    if request.form.get('optionsFuel_Type') == 'Petrol':
        Fuel_Type_Petrol = 1
    elif request.form.get('optionsFuel_Type') == 'Diesel':
        Fuel_Type_Diesel = 1
    if request.form.get('optionsTransmisssion') == 'Automatic':
        Transmission_Automatic = 1
    elif request.form.get('optionsTransmisssion') == 'Manual':
        Transmission_Manual = 1
    data = {
        "Kilometers_Driven": float(request.form['Kilometers_Driven']),
        "Mileage": float(request.form['Mileage']),
        "Engine": float(request.form['Engine']),
        "Power": float(request.form['Power']),
        "Seats": float(request.form['Seats']),
        "Age": float(request.form['Age']),
        "Fuel_Type_Diesel": Fuel_Type_Diesel,
        "Fuel_Type_Petrol":Fuel_Type_Petrol ,
        "Transmission_Automatic": Transmission_Automatic,
        "Transmission_Manual": Transmission_Manual,
        "Prev_Owners": int(request.form['Prev_Owners'])
            }
    print("test execution")
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    newdata = np.array(list(data.values())).reshape(1,-1)
    output =  model.predict(newdata)
    print(output[0])
    #return jsonify("Expected amount would be  "+str(output[0])+"  lakhs")
    return render_template("home.html",prediction_text = str(output[0])+" lakhs")
@app.route('/predict_PostMan',methods = ['POST'])
def predict_PostMan():
    data = request.json['data']
    print("test execution")
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    newdata = np.array(list(data.values())).reshape(1,-1)
    output =  model.predict(newdata)
    print(output[0])
    return jsonify("Expected amount would be  "+str(output[0])+"  lakhs")
if __name__=="__main__":
    app.run(debug=True)