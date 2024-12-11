import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import requests
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketAnalysisService:
    def __init__(self, data_source_url):
        self.data_source_url = data_source_url
        self.model = None
        self.data = None

    def fetch_data(self):
        """Fetch market data from a specified URL."""
        try:
            logger.info("Fetching data from %s", self.data_source_url)
            response = requests.get(self.data_source_url)
            response.raise_for_status()
            self.data = pd.DataFrame(response.json())
            logger.info("Data fetched successfully.")
        except Exception as e:
            logger.error("Error fetching data: %s", e)
            raise

    def preprocess_data(self):
        """Preprocess the data for training."""
        logger.info("Preprocessing data...")
        # Example preprocessing steps
        self.data.dropna(inplace=True)  # Remove missing values
        self.data['date'] = pd.to_datetime(self.data['date'])  # Convert date column
        self.data.set_index('date', inplace=True)  # Set date as index
        self.data['price_change'] = self.data['price'].pct_change()  # Calculate price change
        self.data.dropna(inplace=True)  # Drop NaN values after calculation
        logger.info("Data preprocessing completed.")

    def train_model(self):
        """Train the Random Forest model on the market data."""
        logger.info("Training model...")
        X = self.data.drop(columns=['price', 'price_change'])
        y = self.data['price']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        logger.info("Model training completed with MSE: %.2f", mse)

    def predict(self, input_data):
        """Make predictions using the trained model."""
        if self.model is None:
            logger.error("Model is not trained yet. Call train_model() first.")
            raise Exception("Model not trained")

        logger.info("Making predictions...")
        input_df = pd.DataFrame(input_data)
        predictions = self.model.predict(input_df)
        return predictions

    def save_model(self, file_path):
        """Save the trained model to a file."""
        joblib.dump(self.model, file_path)
        logger.info("Model saved to %s", file_path)

    def load_model(self, file_path):
        """Load a trained model from a file."""
        self.model = joblib.load(file_path)
        logger.info("Model loaded from %s", file_path)

# Example usage
if __name__ == "__main__":
    data_source = "https://api.example.com/market_data"  # Replace with actual data source
    service = MarketAnalysisService(data_source)

    service.fetch_data()
    service.preprocess_data()
    service.train_model()

    # Example input for prediction
    input_data = {
        'feature1': [0.5],
        'feature2': [1.2],
        # Add other features as necessary
    }
    predictions = service.predict(input_data)
    print("Predictions:", predictions)

    # Save the model
    service.save_model("market_analysis_model.pkl")
