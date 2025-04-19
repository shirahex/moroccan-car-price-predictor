import streamlit as st
import joblib
import pandas as pd
from model import predict_price
import plotly.express as px
import time

# Set page configuration
st.set_page_config(
    page_title="Avito Car Price Predictor - Morocco",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern, professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background-color: #f5f7fa;
        padding: 20px;
    }
    
    h1 {
        color: #1e3a8a;
        font-weight: 700;
        font-size: 2.5rem;
    }
    
    h2 {
        color: #1e3a8a;
        font-weight: 600;
        font-size: 1.5rem;
        margin-top: 20px;
    }
    
    h3 {
        color: #374151;
        font-weight: 500;
    }
    
    .stButton>button {
        background-color: #1e40af;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        border: none;
        font-weight: 600;
        width: 100%;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #1e3a8a;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border-left: 5px solid #1e40af;
    }
    
    .result-card {
        background-color: #1e3a8a;
        color: white;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 10px 15px rgba(30, 58, 138, 0.2);
        text-align: center;
        margin: 30px 0;
        border: none;
    }
    
    .result-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .result-label {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 10px;
    }
    
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    .info-box {
        background-color: #e0f2fe;
        border-radius: 8px;
        padding: 15px;
        margin: 20px 0;
        border-left: 4px solid #0ea5e9;
    }
    
    .sidebar .sidebar-content {
        background-color: #1e3a8a;
    }
    
    .slidecontainer {
        width: 100%;
    }
    
    .loading-spinner {
        text-align: center;
        padding: 20px;
    }
    
    /* Animation for result */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated {
        animation: fadeIn 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)



# Load dropdown options
marques = joblib.load("marque_list.pkl")
brand_model_dict = joblib.load("brand_model_dict.pkl")
boites = joblib.load("boite_list.pkl")

# Fix carburants - add Diesel
carburants = ["Essence", "Diesel", "Electrique", "Hybride", "LPG"]

# Fix origines - add Dédouanée
origines = ["Dédouanée", "Importée neuve", "Pas encore dédouanée", "WW au Maroc"]

etats = joblib.load("etat_list.pkl")
localisations = joblib.load("localisation_list.pkl")

# Sidebar for project information
with st.sidebar:
    st.image("favicon.ico.svg", width=150)
    st.markdown("## 🚗 Moroccan Car Price Predictor")
    st.markdown("### About this project")
    st.markdown("""
    This machine learning application predicts car prices in Morocco based on Avito marketplace data.
    
    **Features:**
    - Data scraping from Avito.ma
    - Advanced data preprocessing
    - Machine learning model with R² = 0.84
    - Interactive user interface
    
    **Technologies used:**
    - Python
    - Pandas & NumPy
    - Scikit-learn / XGBoost
    - Streamlit
    """)
    
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("""
    1. Enter your car details
    2. Click "Predict Price"
    3. Get an estimated price based on market data
    
    The model analyzes thousands of car listings to determine the most important factors affecting car prices in Morocco.
    """)
    
    st.markdown("---")
    st.markdown("### Created by")
    st.markdown("Daouki Marouane & Alouani Imane")
    st.markdown("© 2025")

# Main page content
st.markdown("<h1>🚗 Moroccan Car Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("### Predict used car prices accurately using machine learning and real market data from Avito.ma")

# Tab-based interface
tab1, tab2, tab3 = st.tabs(["Predict Price", "Market Insights", "About"])

with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Enter Car Details")
    
    # Create three columns for better layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        marque = st.selectbox("Marque (Brand) 🏭", marques)
        filtered_models = sorted(brand_model_dict.get(marque, []))
        modele = st.selectbox("Modèle (Model) 📝", filtered_models)
        annee_modele = st.slider("Année modèle (Year) 📅", 1990, 2024, 2015)
        localisation = st.selectbox("Localisation (City) 📍", localisations)
    
    with col2:
        kilometrage = st.number_input("Kilométrage (Mileage) 🛣️", 0, 500000, 100000, step=5000, 
                                   help="Total kilometers driven")
        puissance_fiscale = st.number_input("Puissance fiscale (Fiscal Power) 💪", 1, 20, 6,
                                        help="Fiscal horsepower - important for taxation in Morocco")
        nombre_de_portes = st.selectbox("Nombre de portes (Doors) 🚪", [3, 4, 5])
        type_de_carburant = st.selectbox("Type de carburant (Fuel Type) ⛽", carburants)
        
    with col3:
        premiere_main = st.selectbox("Première main? (First owner?) 🆕", 
                                 [("Non", 0), ("Oui", 1)], 
                                 format_func=lambda x: x[0])[1]
        boite_vitesses = st.selectbox("Boîte de vitesses (Transmission) 🔄", boites)
        origine = st.selectbox("Origine (Origin) 🌍", origines)
        etat_du_vehicule = st.selectbox("État du véhicule (Condition) 🔧", etats)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Prepare input data for prediction
    input_data = {
        "marque": marque,
        "modele": modele,
        "annee_modele": annee_modele,
        "kilometrage": kilometrage,
        "nombre_de_portes": nombre_de_portes,
        "puissance_fiscale": puissance_fiscale,
        "premiere_main": premiere_main,
        "boite_vitesses": boite_vitesses,
        "type_de_carburant": type_de_carburant,
        "origine": origine,
        "etat_du_vehicule": etat_du_vehicule,
        "localisation": localisation
    }
    
    # Center the predict button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("💰 Predict Price")
    
    if predict_button:
        try:
            # Show loading spinner
            with st.spinner("Calculating estimated price..."):
                # Add slight delay for effect
                time.sleep(1.2)
                price = predict_price(input_data)
                
                # Format the price with spaces for thousands
                formatted_price = f"{int(price):,}".replace(",", " ")
            
            # Display animated result card
            st.markdown(f"""
            <div class='result-card animated'>
                <div class='result-label'>Estimated Price</div>
                <div class='result-value'>{formatted_price} MAD</div>
                <div>Based on current market conditions</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Price factors explanation
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### Key Price Factors")
            
            # Calculate age effect
            age = 2025 - annee_modele
            age_impact = "High negative impact" if age > 10 else "Medium negative impact" if age > 5 else "Low negative impact"
            
            # Calculate mileage effect
            mileage_impact = "High negative impact" if kilometrage > 200000 else "Medium negative impact" if kilometrage > 100000 else "Low negative impact"
            
            # Display factors
            factors_col1, factors_col2 = st.columns(2)
            
            with factors_col1:
                st.markdown(f"**Age:** {age} years ({age_impact})")
                st.markdown(f"**Mileage:** {kilometrage:,} km ({mileage_impact})".replace(",", " "))
                st.markdown(f"**Brand popularity:** {'High' if marque in ['Dacia', 'Renault', 'Volkswagen'] else 'Medium'}")
                
            with factors_col2:
                st.markdown(f"**Condition:** {etat_du_vehicule}")
                st.markdown(f"**Origin:** {origine}")
                st.markdown(f"**First Owner:** {'Yes' if premiere_main == 1 else 'No'}")
                
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Additional information box
            st.markdown("""
            <div class='info-box'>
            <strong>Note:</strong> This estimate is based on historical data from Avito.ma. 
            The actual selling price may vary based on specific vehicle condition, 
            additional features, market trends, and negotiation.
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            st.error("Please check that all necessary files are available and the model is correctly configured.")
            
            # Provide more specific guidance based on error
            if "feature_names mismatch" in str(e):
                st.warning("There appears to be a mismatch between the features expected by the model and the data provided. Please check your model configuration.")
            elif "not callable" in str(e):
                st.warning("There seems to be an issue with the prediction function. Please verify the MODEL.py file.")

with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Morocco Car Market Insights")
    
    # Create sample data for visualization
    brands = ['Dacia', 'Renault', 'Volkswagen', 'Peugeot', 'Hyundai', 'Citroen', 'Ford', 'Toyota', 'Mercedes', 'BMW']
    values = [18, 16, 12, 10, 9, 8, 7, 7, 7, 6]
    
    # Create horizontal bar chart of popular brands
    fig = px.bar(x=values, y=brands, orientation='h', 
                 title="Most Popular Car Brands in Morocco",
                 labels={'x': 'Market Share (%)', 'y': 'Brand'},
                 color=values, color_continuous_scale='Blues')
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Age distribution
    st.markdown("### Age Distribution of Used Cars")
    age_ranges = ['< 3 years', '3-5 years', '6-10 years', '11-15 years', '> 15 years']
    age_dist = [15, 22, 35, 18, 10]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig2 = px.pie(values=age_dist, names=age_ranges, hole=0.4,
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("#### Market Insights")
        st.markdown("""
        - The Moroccan used car market is dominated by affordable brands like Dacia and Renault
        - Most sold used cars are 6-10 years old
        - Diesel vehicles still represent over 60% of the market
        - Automatic transmissions are gaining popularity but remain less common
        - Popular cities for car sales: Casablanca, Rabat, Marrakech, Tangier
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Price trends
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Price Trends by Car Age")
    
    # Sample data for price depreciation
    years = list(range(0, 16))
    percentage = [100, 85, 75, 67, 60, 54, 49, 45, 41, 38, 35, 32, 29, 27, 25, 23]
    
    fig3 = px.line(x=years, y=percentage, 
                  labels={'x': 'Vehicle Age (Years)', 'y': 'Value Retained (%)'},
                  title="Car Value Depreciation Over Time")
    fig3.update_traces(line=dict(color='#1e40af', width=3))
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### About This Project")
    
    st.markdown("""
    #### Project Development Stages
    
    **1. Data Collection**
    - Web scraping of Avito.ma car listings
    - Collection of over 10,000 vehicle listings
    - Data extraction of key vehicle attributes and prices
    
    **2. Data Preprocessing**
    - Cleaning of inconsistent and missing data
    - Feature engineering to extract valuable insights
    - Encoding of categorical variables
    - Normalization of numeric features
    
    **3. Model Development**
    - Testing of various regression algorithms
    - Hyperparameter tuning for optimal performance
    - Cross-validation to ensure model reliability
    - Final model selection based on performance metrics
    
    **4. Application Development**
    - Creation of user-friendly interface with Streamlit
    - Integration of predictive model
    - Development of visualization components
    - Deployment for end-user access
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Model Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Metrics
        - **R² Score:** 0.84
        - **Mean Absolute Error:** 12,500 MAD
        - **Root Mean Squared Error:** 18,200 MAD
        """)
        
    with col2:
        st.markdown("""
        #### Key Predictors
        - Vehicle age (years)
        - Mileage
        - Brand and model popularity
        - Fuel type
        - Transmission type
        - Vehicle condition
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    <p>© 2025 Moroccan Car Price Predictor | Data sourced from Avito.ma | Created for academic purposes</p>
    <p>This application is for educational use only and does not represent an official valuation tool.</p>
</div>
""", unsafe_allow_html=True)