import subprocess
import threading
import time
import webbrowser
from server import app, util

def start_flask():
    """Start the Flask application"""
    print("Starting Flask server...")
    util.load_saved_artifacts()
    app.run(host='0.0.0.0', port=5001, debug=False)

def start_simple_tunnel():
    """Start a simple tunnel using Python's built-in capabilities"""
    print("\n🌐 Setting up local deployment...")
    print(f"✅ Your Real Estate Predictor is running at:")
    print(f"   🏠 Local: http://localhost:5001")
    print(f"   🌍 Network: http://192.0.0.2:5001")
    print(f"   📱 Mobile (same WiFi): http://192.0.0.2:5001")
    
    print("\n📋 Deployment Options:")
    print("1. 🔗 Share on your local network - Use: http://192.0.0.2:5001")
    print("2. 🚀 For internet access, try these free options:")
    print("   • Render.com (free tier)")
    print("   • Railway.app (free tier)")
    print("   • PythonAnywhere (free tier)")
    print("   • Heroku (with credit card)")
    
    print("\n⚡ Quick Internet Access:")
    print("   Run: ssh -R 80:localhost:5001 serveo.net")
    print("   This will give you a public URL instantly!")
    
    try:
        # Open local app in browser
        webbrowser.open('http://localhost:5001')
        print("\n🌟 Opening your app in the browser...")
    except:
        pass
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")

if __name__ == "__main__":
    print("🏠 Real Estate Predictor - Simple Deployment")
    print("=" * 50)
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(2)
    
    # Start simple deployment info
    start_simple_tunnel()