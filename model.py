import joblib
import pandas as pd
import numpy as np

# Load the model
model = joblib.load("best_car_price_model.pkl")

def predict_price(input_data):
    """
    Transform raw input data from the UI into the format expected by the model,
    then predict the car price.
    
    Args:
        input_data (dict): User input from the Streamlit interface
        
    Returns:
        float: Predicted price in MAD
    """
    # Create a DataFrame with a single row for the input data
    df = pd.DataFrame([input_data])
    
    # Extract the necessary features for prediction
    numeric_features = [
        "annee_modele", 
        "kilometrage", 
        "nombre_de_portes", 
        "puissance_fiscale", 
        "premiere_main"
    ]
    
    # Start building the feature set for prediction
    X = pd.DataFrame()
    
    # Add numeric features
    for feature in numeric_features:
        X[feature] = df[feature]
    
    # Calculate frequency-based features (if needed)
    # Load frequency mappings
    marque_freq = joblib.load("marque_freq.pkl")
    modele_freq = joblib.load("modele_freq.pkl")
    
    X["marque_freq"] = df["marque"].map(marque_freq).fillna(0)
    X["modele_freq"] = df["modele"].map(modele_freq).fillna(0)
    
    # Boite vitesses - USING ONLY MANUAL FLAG PER ERROR MESSAGE
    X["boite_vitesses_Manuelle"] = df["boite_vitesses"].iloc[0] == "Manuelle"
    
    # Type de carburant - Handle all types including Diesel
    # Map Diesel to either default or nearest appropriate value since model doesn't support it
    carburant = df["type_de_carburant"].iloc[0]
    
    # Initialize all to False
    X["type_carburant_Electrique"] = False
    X["type_carburant_Essence"] = False
    X["type_carburant_Hybride"] = False
    X["type_carburant_LPG"] = False
    
    # Set the appropriate one to True
    if carburant == "Diesel":  
        # Map Diesel to Essence as a fallback since model doesn't have Diesel
        X["type_carburant_Essence"] = True
    elif carburant == "Electrique":
        X["type_carburant_Electrique"] = True
    elif carburant == "Essence":
        X["type_carburant_Essence"] = True
    elif carburant == "Hybride":
        X["type_carburant_Hybride"] = True
    elif carburant == "LPG":
        X["type_carburant_LPG"] = True
    
    # Origine - Handle all types including Dédouanée
    origine = df["origine"].iloc[0]
    
    # Initialize all to False
    X["origine_Importée neuve"] = False
    X["origine_Pas encore dédouanée"] = False
    X["origine_WW au Maroc"] = False
    
    # Set the appropriate one to True
    if origine == "Importée neuve":
        X["origine_Importée neuve"] = True
    elif origine == "Pas encore dédouanée":
        X["origine_Pas encore dédouanée"] = True
    elif origine == "WW au Maroc":
        X["origine_WW au Maroc"] = True
    elif origine == "Dédouanée":
        # Map Dédouanée to WW au Maroc as closest equivalent
        X["origine_WW au Maroc"] = True
    
    # Etat du vehicule
    etat_cols = [
        "etat_Correct",
        "etat_Endommagé",
        "etat_Excellent",
        "etat_Neuf",
        "etat_Pour Pièces",
        "etat_Très bon"
    ]
    
    # Initialize all to False
    for col in etat_cols:
        X[col] = False
        
    # Set the appropriate one to True
    etat = df["etat_du_vehicule"].iloc[0]
    etat_mapped = f"etat_{etat}"
    if etat_mapped in etat_cols:
        X[etat_mapped] = True
    else:
        # Default to "Correct" if not found
        X["etat_Correct"] = True
    
    # Handle localisation as integer
    try:
        X["localisation"] = pd.to_numeric(df["localisation"])
    except:
        try:
            loc_mapping = joblib.load("localisation_mapping.pkl")
            X["localisation"] = df["localisation"].map(loc_mapping).astype(int)
        except:
            localisation_list = joblib.load("localisation_list.pkl")
            loc_mapping = {loc: i for i, loc in enumerate(localisation_list)}
            X["localisation"] = df["localisation"].map(loc_mapping).astype(int)
    
    # Get the exact columns needed by the model from the error message
    expected_columns = [
        'annee_modele', 'kilometrage', 'nombre_de_portes', 'premiere_main', 
        'puissance_fiscale', 'localisation', 'modele_freq', 'marque_freq',
        'boite_vitesses_Manuelle', 'type_carburant_Electrique', 
        'type_carburant_Essence', 'type_carburant_Hybride', 'type_carburant_LPG',
        'origine_Importée neuve', 'origine_Pas encore dédouanée', 'origine_WW au Maroc',
        'etat_Correct', 'etat_Endommagé', 'etat_Excellent', 'etat_Neuf', 
        'etat_Pour Pièces', 'etat_Très bon'
    ]
    
    # Create a DataFrame with all expected columns initialized to 0
    final_X = pd.DataFrame(0, index=[0], columns=expected_columns)
    
    # Fill in the values we have
    for col in X.columns:
        if col in expected_columns:
            final_X[col] = X[col]
    
    # Make sure all columns are of numeric type
    for col in final_X.columns:
        if final_X[col].dtype == 'object':
            final_X[col] = pd.to_numeric(final_X[col], errors='coerce').fillna(0)
        elif final_X[col].dtype == 'bool':
            final_X[col] = final_X[col].astype(int)
    
    # Make prediction
    predicted_price = model.predict(final_X)[0]
    
    return predicted_price