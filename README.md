# Real Estate Predictor

A machine learning-powered web application that predicts real estate prices in Bangalore based on location, size, bathrooms, and other property features.

## 📋 Project Overview

This project uses a machine learning model trained on Bangalore housing data to predict property prices. The application consists of a Python Flask backend for serving predictions and a simple HTML/CSS/JavaScript frontend for user interaction.

## 🏗️ Project Structure

```
Real-Estate-Predictor/
├── app.css                              # Frontend styling
├── app.html                             # Main HTML interface
├── app.js                               # Frontend JavaScript logic
├── banglore_home_prices_model.pickle    # Trained ML model
├── columns.json                         # Feature columns metadata
├── columns.py                           # Column processing utilities
├── housing.csv                          # Training dataset
├── model1.ipynb                         # Jupyter notebook for model training
├── package.json                         # Project configuration
├── server.py                            # Flask backend server
└── util.py                              # Utility functions for predictions
```

## 🚀 Features

- **Property Price Prediction**: Estimate property prices based on:
  - Location (various areas in Bangalore)
  - Number of bedrooms (BHK)
  - Number of bathrooms
  - Total square footage
  - Number of balconies

- **Interactive Web Interface**: User-friendly form with real-time validation
- **Loading States**: Visual feedback during price calculation
- **Error Handling**: Proper error messages for invalid inputs

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.x
- Required Python packages (Flask, scikit-learn, pandas, numpy, etc.)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rajdeep183/Real-Estate-Predictor.git
   cd Real-Estate-Predictor
   ```

2. **Install dependencies**
   ```bash
   pip install flask pandas numpy scikit-learn pickle
   ```

3. **Run the application**
   ```bash
   npm run dev
   # or
   python server.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📊 Model Information

The machine learning model was trained using data from [housing.csv](housing.csv) and includes:

- **Features**: Location (one-hot encoded), total square footage, number of bathrooms, BHK, balconies
- **Target**: Property price in lakhs
- **Algorithm**: Linear Regression (as implemented in [model1.ipynb](model1.ipynb))
- **Preprocessing**: Data cleaning, outlier removal, feature engineering

## 🎯 Usage

1. Open the web application in your browser
2. Select the desired location from the dropdown
3. Choose the number of BHK (bedrooms)
4. Select the number of bathrooms
5. Enter the total square footage
6. Enter the number of balconies
7. Click "Calculate Price" to get the predicted price

The [`getBHKValue()`](app.js) and [`getBathValue()`](app.js) functions in [app.js](app.js) handle user input validation, while the prediction is processed by the Flask server in [server.py](server.py).

## 📝 API Endpoints

- `GET /`: Serves the main HTML page
- `POST /predict_home_price`: Returns predicted price based on input parameters
- `GET /get_location_names`: Returns list of available locations

## 🧪 Available Scripts

From [package.json](package.json):

- `npm run dev`: Start the development server
- `npm run start`: Start the production server
- `npm run serve`: Serve static files on port 8000

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the ISC License.

## 🔗 Links

- **Repository**: [GitHub](https://github.com/Rajdeep183/Real-Estate-Predictor)
- **Issues**: [Report Issues](https://github.com/Rajdeep183/Real-Estate-Predictor/issues)

## 📧 Contact

For any questions or suggestions, please open an issue on GitHub.
