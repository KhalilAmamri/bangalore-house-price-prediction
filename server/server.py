from flask import Flask, jsonify, request
import sys
import os

# Add server directory to path so util can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import util

app = Flask(__name__)
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_price', methods=['POST'])
def predict_price():
    sqft = float(request.form['sqft'])
    bath = int(request.form['bath'])
    bhk = int(request.form['bhk'])
    location = request.form['location']
    
    estimated_price = util.get_estimated_price(location, sqft, bath, bhk)
    
    response = jsonify({
        'estimated_price': estimated_price
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server for Home Price Prediction...")
    util.load_saved_artifacts()
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)