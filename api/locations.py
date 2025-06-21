from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        locations = [
            '1st Block Jayanagar', '1st Phase JP Nagar', 'BTM Layout', 'Banashankari',
            'Bannerghatta Road', 'Basavangudi', 'Bellandur', 'Bommanahalli', 
            'Brookefield', 'CV Raman Nagar', 'Electronic City', 'Hebbal',
            'HSR Layout', 'Indiranagar', 'JP Nagar', 'Jayanagar', 'Koramangala',
            'Malleshwaram', 'Marathahalli', 'Rajaji Nagar', 'Sarjapur Road', 
            'Whitefield', 'Yelahanka', 'Kormangala', 'BTM 2nd Stage',
            'Electronic City Phase II', 'Kadugodi', 'Kannur', 'Thanisandra'
        ]
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps({'locations': locations}).encode())