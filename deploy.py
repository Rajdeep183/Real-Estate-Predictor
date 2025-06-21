from pyngrok import ngrok
import threading
import time
from server import app, util

def start_flask():
    """Start the Flask application"""
    print("Starting Flask server...")
    util.load_saved_artifacts()
    app.run(host='0.0.0.0', port=5001, debug=False)

def start_tunnel():
    """Start ngrok tunnel"""
    try:
        # Create tunnel
        public_url = ngrok.connect(5001)
        print(f"\n🚀 Your app is now live at: {public_url}")
        print(f"📱 Access your Real Estate Predictor from anywhere!")
        print(f"🔗 Public URL: {public_url}")
        print("\n⚠️  Keep this terminal running to maintain the tunnel")
        print("Press Ctrl+C to stop the tunnel and server")
        
        # Keep the tunnel alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping tunnel and server...")
            ngrok.disconnect(public_url)
            ngrok.kill()
            
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        print("💡 Alternative: Your Flask app is still running locally at http://localhost:5001")

if __name__ == "__main__":
    print("🏠 Real Estate Predictor - Local to Internet Deployment")
    print("=" * 50)
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(3)
    
    # Start tunnel
    start_tunnel()