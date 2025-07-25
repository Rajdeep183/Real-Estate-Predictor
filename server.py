from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import util

app = Flask(__name__)

# Initialize the model when the module is imported (for Vercel)
util.load_saved_artifacts()


@app.route('/')
def index():
    return send_from_directory('.', 'app.html')


@app.route('/app.js')
def serve_js():
    return send_from_directory('.', 'app.js')


@app.route('/app.css')
def serve_css():
    return send_from_directory('.', 'app.css')


@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])
    balcony = int(request.form.get('balcony', 1))  # Default to 1 if not provided

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath, balcony)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# For Vercel serverless deployment
if __name__ != "__main__":
    # This ensures the app is properly initialized for Vercel
    util.load_saved_artifacts()

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
