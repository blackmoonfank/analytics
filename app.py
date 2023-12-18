

from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

fuel = pd.read_excel('./data_set_fuel_cons.xlsx')

app = Flask(__name__)

#load the saved model
model = joblib.load('./model_fuel.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        #get input data from html
        hm_vhms = float(request.form['hm_vhms'])
        lf_egt_max = float(request.form['lf_egt_max'])
        lr_egt_max = float(request.form['lr_egt_max'])
        rf_egt_max = float(request.form['rf_egt_max'])
        rr_egt_max = float(request.form['rr_egt_max'])
        boost_press_max = float(request.form['boost_press_max'])
        eng_speed_ave = float(request.form['eng_speed_ave'])
        eng_oil_press_lo_min = float(request.form['eng_oil_press_lo_min'])
        eng_oil_press_hi_min = float(request.form['eng_oil_press_hi_min'])
        cool_temp_max = float(request.form['cool_temp_max'])
        eng_on_count = float(request.form['eng_on_count'])

        #make prediction
        prediction = model.predict([[hm_vhms, lf_egt_max, lr_egt_max, rf_egt_max, rr_egt_max, boost_press_max, 
                                     eng_speed_ave, eng_oil_press_lo_min, eng_oil_press_hi_min, cool_temp_max, eng_on_count]])

        #return the predicted class
        return render_template('index.html', result = f'Predicted Fuel Rate (l/h): {prediction[0]}', 
                               hm_vhms = hm_vhms, lf_egt_max = lf_egt_max, lr_egt_max = lr_egt_max, rf_egt_max = rf_egt_max,
                               rr_egt_max = rr_egt_max, boost_press_max = boost_press_max, eng_speed_ave = eng_speed_ave,
                               eng_oil_press_lo_min = eng_oil_press_lo_min, eng_oil_press_hi_min = eng_oil_press_hi_min,
                               cool_temp_max = cool_temp_max, eng_on_count = eng_on_count)
    
    except Exception as e:
        return render_template('index.html', result = f'Error: {e}')
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)