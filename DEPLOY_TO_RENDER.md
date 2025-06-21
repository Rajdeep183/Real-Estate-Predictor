# Render Deployment Guide for Your ML API

## Quick Deploy to Render (Free Tier)

1. Create account at render.com
2. Connect your GitHub repo
3. Create new Web Service with these settings:

**Build Command:** 
```
pip install -r ml_requirements.txt
```

**Start Command:** 
```
gunicorn ml_api_server:app
```

**Environment Variables:**
- FLASK_ENV=production
- PORT=10000

Your ML API will be live at: https://your-app-name.onrender.com

## Test Commands:
```bash
# Health check
curl https://your-app-name.onrender.com/

# Test prediction
curl -X POST https://your-app-name.onrender.com/predict_home_price \
  -H "Content-Type: application/json" \
  -d '{"total_sqft": 1500, "location": "Koramangala", "bhk": 3, "bath": 2, "balcony": 1}'
```