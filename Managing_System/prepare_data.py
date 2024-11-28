# prepare_data.py

import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_data(csv_file):
    try:
        data = pd.read_csv(csv_file, parse_dates=['Timestamp'])
        logging.info("Data loaded successfully.")
        return data
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

def preprocess_data(data):
    try:
        # Drop rows with missing critical values
        data = data.dropna(subset=['CPU Usage (%)', 'Memory Usage (%)', 'Weather Temp (°C)', 'Humidity (%)', 'Weather Description', 'ReqPerSec', 'Average Latency (ms)'])
        
        # Handle 'N/A' in 'CPU Temp (°C)'
        data['CPU Temp (°C)'] = pd.to_numeric(data['CPU Temp (°C)'], errors='coerce').fillna(0)
        
        # One-hot encode 'Weather Description'
        weather_desc = data[['Weather Description']]
        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        weather_encoded = encoder.fit_transform(weather_desc)
        weather_encoded_df = pd.DataFrame(weather_encoded, columns=encoder.get_feature_names_out(['Weather Description']))
        data = pd.concat([data.drop('Weather Description', axis=1), weather_encoded_df], axis=1)
        
        # Features and scaling
        features = data.drop(['Timestamp'], axis=1)
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        logging.info("Data preprocessing completed.")
        return scaled_features, scaler, encoder
    except Exception as e:
        logging.error(f"Error in preprocessing data: {e}")
        return None, None, None

def save_preprocessed_data(scaled_features, scaler, encoder, feature_file='features.pkl', encoder_file='encoder.pkl'):
    try:
        joblib.dump(scaled_features, feature_file)
        joblib.dump(scaler, 'scaler.pkl')
        joblib.dump(encoder, encoder_file)
        logging.info(f"Preprocessed data saved to {feature_file}, scaler saved to scaler.pkl, encoder saved to {encoder_file}.")
    except Exception as e:
        logging.error(f"Error saving preprocessed data: {e}")

def main():
    csv_file = '/mnt/c/Users/danie/Dropbox/bonjr/coding/VSProjects/Lets_SAS_RPI_Websites/Managing_System/combined.csv'
    data = load_data(csv_file)
    if data is None:
        logging.error("Data loading failed. Exiting.")
        return
    
    scaled_features, scaler, encoder = preprocess_data(data)
    if scaled_features is None:
        logging.error("Data preprocessing failed. Exiting.")
        return
    
    save_preprocessed_data(scaled_features, scaler, encoder)

if __name__ == "__main__":
    main()
