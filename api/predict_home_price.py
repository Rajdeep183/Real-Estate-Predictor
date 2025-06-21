from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Model coefficients
        model_coefficients = {
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
        
        try:
            # Read POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse form data
            data = urllib.parse.parse_qs(post_data)
            
            # Extract parameters
            total_sqft = float(data.get('total_sqft', [0])[0])
            location = data.get('location', [''])[0]
            bhk = int(data.get('bhk', [1])[0])
            bath = int(data.get('bath', [1])[0])
            balcony = int(data.get('balcony', [1])[0])
            
            if not all([total_sqft, location, bhk, bath]):
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Missing required parameters'}).encode())
                return
            
            # Calculate price
            price = model_coefficients['intercept']
            price += total_sqft * model_coefficients['total_sqft']
            price += bhk * model_coefficients['bhk']
            price += bath * model_coefficients['bath']
            price += balcony * model_coefficients['balcony']
            
            # Location multiplier
            location_key = location.lower().replace(' ', '').replace('-', '')
            multiplier = 1.0
            
            for loc, mult in model_coefficients['location_multipliers'].items():
                if loc.replace(' ', '') in location_key:
                    multiplier = mult
                    break
            
            price *= multiplier
            price = max(20, min(500, price))
            price = round(price, 2)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {'estimated_price': price}
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': f'Prediction failed: {str(e)}'}).encode())