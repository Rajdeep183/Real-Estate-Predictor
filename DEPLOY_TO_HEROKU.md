# Heroku Deployment Guide for Your ML API

## Deploy to Heroku (Alternative Option)

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login and create app:

```bash
heroku login
heroku create your-real-estate-ml-api
```

3. Set environment variables:
```bash
heroku config:set FLASK_ENV=production
```

4. Deploy:
```bash
git add .
git commit -m "Deploy ML API with trained model"
git push heroku main
```

Your ML API will be live at: https://your-real-estate-ml-api.herokuapp.com

## Required Files (already created):
- `ml_api_server.py` - Your Flask app
- `Procfile` - Contains: `web: gunicorn ml_api_server:app`
- `ml_requirements.txt` - Python dependencies
- `banglore_home_prices_model.pickle` - Your trained model
- `columns.json` - Feature columns data