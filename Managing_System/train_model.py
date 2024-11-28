import joblib
import logging
from sklearn.ensemble import IsolationForest
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_preprocessed_data(feature_file='features.pkl'):
    try:
        scaled_features = joblib.load(feature_file)
        logging.info("Preprocessed data loaded successfully.")
        return scaled_features
    except Exception as e:
        logging.error(f"Error loading preprocessed data: {e}")
        return None

def load_scaler(scaler_file='scaler.pkl'):
    try:
        scaler = joblib.load(scaler_file)
        logging.info("Scaler loaded successfully.")
        return scaler
    except Exception as e:
        logging.error(f"Error loading scaler: {e}")
        return None

def load_encoder(encoder_file='encoder.pkl'):
    try:
        encoder = joblib.load(encoder_file)
        logging.info("OneHotEncoder loaded successfully.")
        return encoder
    except Exception as e:
        logging.error(f"Error loading OneHotEncoder: {e}")
        return None

def train_isolation_forest(scaled_features):
    try:
        model = IsolationForest(
            n_estimators=100,
            contamination=0.07,
            random_state=42
        )
        model.fit(scaled_features)
        logging.info("Isolation Forest model trained successfully.")
        return model
    except Exception as e:
        logging.error(f"Error training Isolation Forest model: {e}")
        return None

def save_model(model, model_path='isolation_forest_model.pkl'):
    try:
        joblib.dump(model, model_path)
        logging.info(f"Isolation Forest model saved to {model_path}.")
    except Exception as e:
        logging.error(f"Error saving model: {e}")

def main():
    feature_file = 'features.pkl'
    scaler_file = 'scaler.pkl'
    encoder_file = 'encoder.pkl'
    
    scaled_features = load_preprocessed_data(feature_file)
    if scaled_features is None:
        logging.error("Loading preprocessed data failed. Exiting.")
        return
    
    scaler = load_scaler(scaler_file)
    if scaler is None:
        logging.error("Loading scaler failed. Exiting.")
        return
    
    encoder = load_encoder(encoder_file)
    if encoder is None:
        logging.error("Loading OneHotEncoder failed. Exiting.")
        return
    
    model = train_isolation_forest(scaled_features)
    if model is None:
        logging.error("Model training failed. Exiting.")
        return
    
    save_model(model)

if __name__ == "__main__":
    main()
