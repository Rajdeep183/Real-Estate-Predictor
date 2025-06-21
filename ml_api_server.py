#!/usr/bin/env python3
"""
Dedicated ML API Server for Real Estate Price Prediction
Uses your actual trained scikit-learn model
Optimized for cloud deployment
"""

from flask import Flask, request, jsonify
import json
import pickle
import numpy as np
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for model artifacts
__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    """Load the trained model and data columns"""
    global __data_columns, __locations, __model
    
    try:
        print("🔄 Loading model artifacts...")
        
        # Load columns
        with open('columns.json', 'r') as f:
            data = json.load(f)
            __data_columns = data['data_columns']
            __locations = __data_columns[4:]  # Skip first 4 features: total_sqft, bath, bhk, balcony
        
        # Load trained model
        with open('banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)
            
        print(f"✅ Model loaded successfully!")
        print(f"📊 Features: {len(__data_columns)}")
        print(f"📍 Locations: {len(__locations)}")
        print(f"🤖 Model type: {type(__model).__name__}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to load ML model: {e}")
        return False

def get_estimated_price(location, sqft, bhk, bath, balcony=1):
    """Use your original ML algorithm for price prediction"""
    try:
        # Find location index in data columns (exact match from your util.py)
        loc_index = -1
        try:
            loc_index = __data_columns.index(location.lower())
        except:
            # Try fuzzy matching for location names
            clean_location = location.lower().replace(' ', '').replace('-', '').replace('.', '')
            for i, col in enumerate(__data_columns):
                clean_col = col.replace(' ', '').replace('-', '').replace('.', '')
                if clean_location == clean_col or clean_location in clean_col:
                    loc_index = i
                    break
        
        # Create feature vector exactly like your util.py
        x = np.zeros(len(__data_columns))
        x[0] = sqft      # total_sqft
        x[1] = bath      # bath
        x[2] = bhk       # bhk  
        x[3] = balcony   # balcony
        
        # Set location feature if found
        if loc_index >= 0:
            x[loc_index] = 1
        
        # Use your trained model for prediction
        prediction = __model.predict([x])[0]
        return round(prediction, 2)
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return None

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Real Estate ML API - Your Trained Model',
        'model_loaded': __model is not None,
        'locations_count': len(__locations) if __locations else 0,
        'model_type': str(type(__model).__name__) if __model else None,
        'version': '2.0'
    })

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    """Get all available location names from your trained model"""
    try:
        if not __locations:
            if not load_saved_artifacts():
                return jsonify({'error': 'Model not loaded'}), 500
        
        # Convert to proper case for frontend display
        formatted_locations = []
        for loc in __locations:
            # Convert from lowercase to title case
            formatted = ' '.join(word.capitalize() for word in loc.split())
            formatted_locations.append(formatted)
        
        return jsonify({
            'locations': sorted(formatted_locations),
            'count': len(formatted_locations),
            'source': 'trained_model'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get locations: {str(e)}'}), 500

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    """Predict home price using your actual trained ML model"""
    try:
        # Ensure model is loaded
        if not __model:
            if not load_saved_artifacts():
                return jsonify({'error': 'ML model not available'}), 500
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract parameters
        total_sqft = float(data.get('total_sqft', 1000))
        location = str(data.get('location', 'Koramangala'))
        bhk = int(data.get('bhk', 2))
        bath = int(data.get('bath', 2))
        balcony = int(data.get('balcony', 1))
        
        # Validate inputs
        if total_sqft <= 0 or bhk <= 0 or bath <= 0:
            return jsonify({'error': 'Invalid input values'}), 400
        
        # Get prediction using your actual ML model
        price = get_estimated_price(location, total_sqft, bhk, bath, balcony)
        
        if price is None:
            return jsonify({'error': 'Prediction failed'}), 500
        
        return jsonify({
            'estimated_price': price,
            'input': {
                'location': location,
                'total_sqft': total_sqft,
                'bhk': bhk,
                'bath': bath,
                'balcony': balcony
            },
            'model': 'scikit-learn',
            'algorithm': 'YOUR_ACTUAL_TRAINED_MODEL',
            'confidence': 'high',
            'source': 'ml_model'
        })
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/model_info', methods=['GET'])
def model_info():
    """Get detailed information about your loaded model"""
    try:
        if not __model:
            if not load_saved_artifacts():
                return jsonify({'error': 'Model not loaded'}), 500
        
        return jsonify({
            'model_type': str(type(__model).__name__),
            'features_count': len(__data_columns) if __data_columns else 0,
            'locations_count': len(__locations) if __locations else 0,
            'sample_locations': __locations[:10] if __locations else [],
            'model_loaded': __model is not None,
            'model_file': 'banglore_home_prices_model.pickle',
            'columns_file': 'columns.json',
            'algorithm': 'Your Trained Scikit-Learn Model'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get model info: {str(e)}'}), 500

if __name__ == '__main__':
    print("🏠 Starting Real Estate ML API Server...")
    print("🎯 Using YOUR actual trained scikit-learn model")
    
    # Load model on startup
    if load_saved_artifacts():
        print("✅ ML model loaded successfully!")
        print("🚀 Server ready to make predictions!")
    else:
        print("⚠️  Warning: ML model failed to load")
    
    # Run server
    port = int(os.environ.get('PORT', 8080))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)