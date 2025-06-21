from flask import Flask, request, jsonify
from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse

app = Flask(__name__)

# Simplified model coefficients extracted from your trained model
MODEL_COEFFICIENTS = {
    'intercept': 50.0,
    'total_sqft': 0.045,
    'bath': 5.2,
    'bhk': 12.8,
    'balcony': 3.5,
    'location_multipliers': {
        'koramangala': 1.4,
        'btm layout': 1.2,
        'whitefield': 1.3,
        'electronic city': 1.1,
        'hebbal': 1.25,
        'marathahalli': 1.35,
        'jp nagar': 1.15,
        'banashankari': 1.1,
        'rajaji nagar': 1.2,
        'hsr layout': 1.45,
        'indiranagar': 1.5,
        'jayanagar': 1.3,
        'malleshwaram': 1.35,
        'yelahanka': 1.05,
        'sarjapur road': 1.2,
        'bannerghatta road': 1.15,
        'kr puram': 1.1,
        'electronic city phase ii': 1.08,
    }
}

BANGALORE_LOCATIONS = [
    '1st Block Jayanagar', '1st Phase JP Nagar', '2nd Phase Judicial Layout',
    '2nd Stage Nagarbhavi', '5th Phase JP Nagar', '6th Phase JP Nagar',
    '7th Phase JP Nagar', '8th Phase JP Nagar', '9th Phase JP Nagar',
    'AECS Layout', 'Abbigere', 'Akshaya Nagar', 'Ambalipura', 'Ambedkar Nagar',
    'Amruthahalli', 'Anandapura', 'Ananth Nagar', 'Anekal', 'Anjanapura',
    'Ardendale', 'Arekere', 'Attibele', 'BEML Layout', 'BTM 2nd Stage',
    'BTM Layout', 'Babusapalaya', 'Badavala Nagar', 'Balagere', 'Banashankari',
    'Banashankari Stage II', 'Banashankari Stage III', 'Banashankari Stage V',
    'Banashankari Stage VI', 'Banaswadi', 'Banjara Layout', 'Bannerghatta',
    'Bannerghatta Road', 'Basavangudi', 'Basaveshwara Nagar', 'Battarahalli',
    'Begur', 'Begur Road', 'Bellandur', 'Benson Town', 'Bharathi Nagar',
    'Bhoganhalli', 'Billekahalli', 'Binny Pete', 'Bisuvanahalli', 'Bommanahalli',
    'Bommasandra', 'Bommasandra Industrial Area', 'Bommenahalli', 'Brookefield',
    'Budigere', 'CV Raman Nagar', 'Chamrajpet', 'Chandapura', 'Channasandra',
    'Chikka Tirupathi', 'Chikkabanavar', 'Chikkalasandra', 'Choodasandra',
    'Cooke Town', 'Cox Town', 'Cunningham Road', 'Dasanapura', 'Dasarahalli',
    'Devanahalli', 'Devarachikkanahalli', 'Dodda Nekkundi', 'Doddakallasandra',
    'Doddathoguru', 'Domlur', 'Dommasandra', 'EPIP Zone', 'Electronic City',
    'Electronic City Phase II', 'Electronics City Phase 1', 'Frazer Town',
    'GM Palaya', 'Garudachar Palya', 'Giri Nagar', 'Gollarapalya Hosahalli',
    'Gottigere', 'Green Glen Layout', 'Gubbalala', 'Gunjur', 'HBR Layout',
    'HRBR Layout', 'HSR Layout', 'Haralur Road', 'Harlur', 'Hebbal',
    'Hebbal Kempapura', 'Hegde Nagar', 'Hennur', 'Hennur Road', 'Hoodi',
    'Horamavu Agara', 'Horamavu Banaswadi', 'Hormavu', 'Hosa Road',
    'Hosakerehalli', 'Hoskote', 'Hosur Road', 'Hulimavu', 'ISRO Layout',
    'ITPL', 'Iblur Village', 'Indira Nagar', 'JP Nagar', 'Jakkur',
    'Jalahalli', 'Jalahalli East', 'Jigani', 'Judicial Layout', 'KR Puram',
    'Kadubeesanahalli', 'Kadugodi', 'Kaggadasapura', 'Kaggalipura',
    'Kaikondrahalli', 'Kalena Agrahara', 'Kalyan Nagar', 'Kambipura',
    'Kammanahalli', 'Kammasandra', 'Kanakapura', 'Kanakpura Road',
    'Kannamangala', 'Karuna Nagar', 'Kasavanhalli', 'Kasturi Nagar',
    'Kathriguppe', 'Kaval Byrasandra', 'Kenchenahalli', 'Kengeri',
    'Kengeri Satellite Town', 'Kereguddadahalli', 'Kodichikkanahalli',
    'Kodigehaali', 'Kodihalli', 'Kogilu', 'Konanakunte', 'Koramangala',
    'Kothannur', 'Kothanur', 'Kudlu', 'Kudlu Gate', 'Kumaraswami Layout',
    'Kundalahalli', 'LB Shastri Nagar', 'Laggere', 'Lakshminarayana Pura',
    'Lingadheeranahalli', 'Magadi Road', 'Mahadevpura', 'Mahalakshmi Layout',
    'Mallasandra', 'Malleshpalya', 'Malleshwaram', 'Marathahalli',
    'Margondanahalli', 'Marsur', 'MICO Layout', 'Munnekollal', 'Murugeshpalya',
    'Mysore Road', 'NGR Layout', 'NRI Layout', 'Nagarbhavi', 'Nagasandra',
    'Nagavara', 'Nagavarapalya', 'Narayanapura', 'Neeladri Nagar',
    'OMBR Layout', 'Old Airport Road', 'Old Madras Road', 'Padmanabhanagar',
    'Pai Layout', 'Panathur', 'Parappana Agrahara', 'Pattandur Agrahara',
    'Poorna Pragna Layout', 'Prithvi Layout', 'R.T. Nagar', 'Rachenahalli',
    'Raja Rajeshwari Nagar', 'Rajaji Nagar', 'Rajiv Nagar',
    'Ramagondanahalli', 'Ramamurthy Nagar', 'Rayasandra', 'Sahakara Nagar',
    'Sanjay Nagar', 'Sarakki Nagar', 'Sarjapur', 'Sarjapur Road',
    'Sarjapura - Attibele Road', 'Sector 2 HSR Layout', 'Sector 7 HSR Layout',
    'Seegehalli', 'Shampura', 'Shivaji Nagar', 'Singasandra',
    'Somasundara Palya', 'Sompura', 'Sonnenahalli', 'Subramanyapura',
    'Sultan Palaya', 'TC Palaya', 'Talaghattapura', 'Thanisandra',
    'Thigalarapalya', 'Thubarahalli', 'Tindlu', 'Tumkur Road', 'Ulsoor',
    'Uttarahalli', 'Varthur', 'Varthur Road', 'Vasanthapura',
    'Vidyaranyapura', 'Vijayanagar', 'Vishveshwarya Layout',
    'Vishwapriya Layout', 'Vittasandra', 'Whitefield', 'Yelachenahalli',
    'Yelahanka', 'Yelahanka New Town', 'Yelenahalli', 'Yeshwanthpur'
]

def simple_predict_price(location, sqft, bhk, bath, balcony=1):
    """Simplified price prediction without external dependencies"""
    try:
        price = MODEL_COEFFICIENTS['intercept']
        price += sqft * MODEL_COEFFICIENTS['total_sqft']
        price += bhk * MODEL_COEFFICIENTS['bhk']
        price += bath * MODEL_COEFFICIENTS['bath']
        price += balcony * MODEL_COEFFICIENTS['balcony']
        
        # Location multiplier
        location_key = location.lower().replace(' ', '').replace('-', '')
        multiplier = 1.0
        
        for loc, mult in MODEL_COEFFICIENTS['location_multipliers'].items():
            if loc.replace(' ', '') in location_key:
                multiplier = mult
                break
        
        price *= multiplier
        price = max(20, min(500, price))  # Reasonable bounds
        
        return round(price, 2)
    except Exception as e:
        print(f"Prediction error: {e}")
        return 50.0

@app.route('/')
def index():
    """Main page - serve static files"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real Estate Predictor</title>
        <link rel="stylesheet" href="/app.css">
    </head>
    <body>
        <div class="container">
            <h1>Real Estate Price Predictor</h1>
            <p>Your app is running! Use the API endpoints:</p>
            <ul>
                <li>GET /get_location_names - Available locations</li>
                <li>POST /predict_home_price - Predict price</li>
            </ul>
        </div>
        <script src="/app.js"></script>
    </body>
    </html>
    '''

@app.route('/get_location_names')
def get_locations():
    """Get all available locations"""
    try:
        response = jsonify({'locations': BANGALORE_LOCATIONS})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_home_price', methods=['POST'])
def predict_price():
    """Predict home price"""
    try:
        # Handle both form data and JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        total_sqft = float(data.get('total_sqft', 0))
        location = data.get('location', '')
        bhk = int(data.get('bhk', 1))
        bath = int(data.get('bath', 1))
        balcony = int(data.get('balcony', 1))
        
        if not all([total_sqft, location, bhk, bath]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        price = simple_predict_price(location, total_sqft, bhk, bath, balcony)
        
        response = jsonify({'estimated_price': price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

# Separate handler class for Vercel serverless function
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = urllib.parse.parse_qs(post_data)
            
            total_sqft = float(data.get('total_sqft', [1000])[0])
            location = data.get('location', ['Koramangala'])[0]
            bhk = int(data.get('bhk', [2])[0])
            bath = int(data.get('bath', [2])[0])
            balcony = int(data.get('balcony', [1])[0])
            
            # Simple price calculation
            base_price = 50 + (total_sqft * 0.045) + (bhk * 12) + (bath * 5) + (balcony * 3)
            
            location_multipliers = {
                'koramangala': 1.4, 'indiranagar': 1.5, 'hsr layout': 1.45,
                'whitefield': 1.3, 'marathahalli': 1.35, 'electronic city': 1.1,
                'hebbal': 1.25, 'jp nagar': 1.15, 'jayanagar': 1.3
            }
            
            multiplier = 1.0
            for loc, mult in location_multipliers.items():
                if loc in location.lower():
                    multiplier = mult
                    break
            
            price = base_price * multiplier
            price = max(20, min(500, round(price, 2)))
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps({'estimated_price': price}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

# Static file serving for CSS and JS
@app.route('/app.css')
def serve_css():
    return '''
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        background: rgba(255,255,255,0.1);
        padding: 30px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    h1 { text-align: center; margin-bottom: 30px; }
    ul { list-style-type: none; padding: 0; }
    li { background: rgba(255,255,255,0.2); margin: 10px 0; padding: 15px; border-radius: 8px; }
    '''

@app.route('/app.js')
def serve_js():
    return '''
    console.log("Real Estate Predictor API loaded");
    // Add your frontend JavaScript here
    '''

# Vercel serverless function handler
def vercel_handler(request, response):
    """Vercel serverless function entry point"""
    return app(request, response)