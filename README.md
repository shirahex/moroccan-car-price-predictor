# 🚗 Moroccan Car Price Predictor



## Overview

The Moroccan Car Price Predictor is a machine learning application that estimates the market value of used cars in Morocco based on data collected from Avito.ma marketplace. This tool helps buyers and sellers make informed decisions by providing accurate price predictions based on various vehicle attributes.

## ✨ Features

- **Accurate Price Predictions**: Utilizes machine learning to predict car prices with R² score of 0.84
- **Interactive UI**: User-friendly interface built with Streamlit for easy data input
- **Market Insights**: Visual representations of Moroccan car market trends
- **Comprehensive Data**: Model trained on thousands of vehicle listings from Avito.ma

## 🛠️ Technology Stack

- **Python**: Core programming language
- **Pandas & NumPy**: Data manipulation and analysis
- **Scikit-learn / XGBoost**: Machine learning models
- **Joblib**: Model serialization
- **Streamlit**: Interactive web application
- **Plotly**: Data visualization
- **CSS/HTML**: UI styling

## 📊 Project Structure

```
moroccan-car-price-predictor/
├── app.py                    # Main Streamlit application file
├── model.py                  # Prediction function and model logic
├── best_car_price_model.pkl  # Serialized machine learning model
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── favicon.ico.svg           # Project logo
└── data/                     # Data files used by the application
    ├── marque_list.pkl       # List of car brands
    ├── modele_list.pkl       # List of car models
    ├── boite_list.pkl        # List of transmission types
    ├── carburant_list.pkl    # List of fuel types
    ├── etat_list.pkl         # List of vehicle conditions
    ├── localisation_list.pkl # List of Moroccan cities
    ├── marque_freq.pkl       # Brand frequency data
    ├── modele_freq.pkl       # Model frequency data
    └── localisation_mapping.pkl # City mapping data
```

## 🚀 Installation & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/moroccan-car-price-predictor.git
   cd moroccan-car-price-predictor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**:
   The application will be available at `http://localhost:8501`

## 📱 How to Use

1. Fill in your car details including:
   - Brand and model
   - Year of manufacture
   - Mileage
   - Fiscal power
   - Number of doors
   - Fuel type
   - Transmission type
   - Origin (imported or local)
   - Vehicle condition
   - Location (city)

2. Click "Predict Price" to get an estimated market value in Moroccan Dirhams (MAD)

3. View additional insights about factors affecting the price

## 📈 Model Performance

- **R² Score**: 0.84
- **Mean Absolute Error**: 12,500 MAD
- **Root Mean Squared Error**: 18,200 MAD

## 🔍 Project Development Process

### Data Collection
- Web scraping of car listings from Avito.ma
- Collection of over 80,000 vehicle entries
- Extraction of key vehicle attributes and prices

### Data Preprocessing
- Cleaning of inconsistent and missing data
- Feature engineering to extract valuable insights
- Encoding of categorical variables
- Normalization of numeric features

### Model Development
- Testing of various regression algorithms
- Hyperparameter tuning for optimal performance
- Cross-validation to ensure model reliability
- Final model selection based on performance metrics

### Application Development
- Creation of user-friendly interface with Streamlit
- Integration of the predictive model
- Development of visualization components
- Deployment for end-user access

## 🔑 Key Findings

- Vehicle age and mileage are the strongest predictors of car value
- Affordable brands like Dacia and Renault dominate the Moroccan market
- Most sold used cars in Morocco are 6-10 years old
- Diesel vehicles represent over 60% of the market
- Automatic transmissions are gaining popularity but remain less common
- Casablanca, Rabat, Marrakech, and Tangier are the most active cities for car sales

## 👥 Contributors

- Daouki Marouane
- Alouani Imane

## ⚠️ Disclaimer

This application is for educational purposes only and does not represent an official valuation tool. The estimated prices should be used as reference points and not as definitive valuations.

## 📄 License

© 2025 Moroccan Car Price Predictor | Data sourced from Avito.ma | Created for academic purposes
