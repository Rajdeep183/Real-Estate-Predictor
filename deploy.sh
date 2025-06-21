#!/bin/bash
# Deployment script for Real Estate Predictor

echo "🚀 Deploying Real Estate Predictor to Vercel..."

# Check if Vercel CLI is available
if ! command -v vercel &> /dev/null && ! command -v npx &> /dev/null; then
    echo "❌ Vercel CLI not found. Please install with: npm install -g vercel"
    exit 1
fi

# Deploy to Vercel
echo "📤 Deploying to production..."
if command -v vercel &> /dev/null; then
    vercel --prod
else
    npx vercel --prod
fi

echo "✅ Deployment complete!"
echo "🌐 Your app should be live at the URL provided by Vercel"
echo ""
echo "📋 Next steps:"
echo "1. Note down your deployment URL"
echo "2. Test the API endpoints:"
echo "   - GET /get_location_names"
echo "   - POST /predict_home_price"
echo "3. Your frontend will automatically use the same domain for API calls"