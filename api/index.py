from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import pickle
import numpy as np

# Global variables for model artifacts
__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    """Load the trained model and data columns"""
    global __data_columns, __locations, __model
    
    try:
        # Load columns from current directory
        with open('columns.json', 'r') as f:
            data = json.load(f)
            __data_columns = data['data_columns']
            __locations = __data_columns[4:]  # Skip first 4 features
        
        # Load trained model from current directory
        with open('banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)
            
        return True
    except Exception as e:
        print(f"Failed to load ML model: {e}")
        return False

def get_estimated_price_ml(location, sqft, bhk, bath, balcony=1):
    """Use your original ML algorithm for price prediction"""
    try:
        # Find location index
        loc_index = -1
        try:
            loc_index = __data_columns.index(location.lower())
        except:
            pass
        
        # Create feature vector
        x = np.zeros(len(__data_columns))
        x[0] = sqft
        x[1] = bath  
        x[2] = bhk
        x[3] = balcony
        
        # Set location feature
        if loc_index >= 0:
            x[loc_index] = 1
        
        # Use trained model for prediction
        prediction = __model.predict([x])[0]
        return round(prediction, 2)
        
    except Exception as e:
        # Fallback to simple calculation if ML fails
        return get_estimated_price_simple(location, sqft, bhk, bath, balcony)

def get_estimated_price_simple(location, sqft, bhk, bath, balcony=1):
    """Fallback simple calculation"""
    price = 50.0 + (sqft * 0.045) + (bhk * 12.8) + (bath * 5.2) + (balcony * 3.5)
    
    # Location multipliers
    location_multipliers = {
        'koramangala': 1.4, 'indiranagar': 1.5, 'hsr layout': 1.45,
        'whitefield': 1.3, 'marathahalli': 1.35, 'electronic city': 1.1,
        'hebbal': 1.25, 'jp nagar': 1.15, 'jayanagar': 1.3
    }
    
    location_key = location.lower().replace(' ', '')
    multiplier = 1.0
    for loc, mult in location_multipliers.items():
        if loc.replace(' ', '') in location_key:
            multiplier = mult
            break
    
    return round(price * multiplier, 2)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check if this is the get_location_names endpoint
        if '/get_location_names' in self.path or self.path.endswith('/'):
            self.handle_get_locations()
        else:
            self.send_404()
    
    def do_POST(self):
        # Check if this is the predict_home_price endpoint
        if '/predict_home_price' in self.path:
            self.handle_predict_price()
        else:
            self.send_404()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def handle_get_locations(self):
        # Load your actual location list
        locations = [
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
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {'locations': locations}
        self.wfile.write(json.dumps(response).encode())
    
    def handle_predict_price(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length).decode('utf-8')
                try:
                    data = json.loads(post_data)
                except:
                    data = dict(urllib.parse.parse_qsl(post_data))
            else:
                self.send_error_response(400, 'No data provided')
                return
            
            # Extract parameters
            total_sqft = float(data.get('total_sqft', 1000))
            location = str(data.get('location', 'Koramangala'))
            bhk = int(data.get('bhk', 2))
            bath = int(data.get('bath', 2))
            balcony = int(data.get('balcony', 1))
            
            # Try to use ML model first, fallback to simple calculation
            if load_saved_artifacts():
                price = get_estimated_price_ml(location, total_sqft, bhk, bath, balcony)
            else:
                price = get_estimated_price_simple(location, total_sqft, bhk, bath, balcony)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {'estimated_price': price}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error_response(500, f'Prediction failed: {str(e)}')
    
    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'error': message}).encode())
    
    def send_404(self):
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Not found'}).encode())