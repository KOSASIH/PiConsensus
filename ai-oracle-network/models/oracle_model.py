import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

class OracleModel:
    def __init__(self, config):
        self.config = config
        self.model = self._build_model()

    def _build_model(self):
        if self.config['model_type'] == 'random_forest':
            return RandomForestRegressor(n_estimators=100, random_state=42)
        elif self.config['model_type'] == 'lstm':
            model = Sequential()
            model.add(LSTM(units=50, return_sequences=True, input_shape=(self.config['sequence_length'], 1)))
            model.add(LSTM(units=50))
            model.add(Dense(1))
            model.compile(loss='mean_squared_error', optimizer='adam')
            return model
        else:
            raise ValueError("Invalid model type")

    def train(self, data):
        X, y = data.drop(['target'], axis=1), data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if self.config['model_type'] == 'random_forest':
            self.model.fit(X_train, y_train)
        elif self.config['model_type'] == 'lstm':
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train.values.reshape(-1, 1))
            X_test_scaled = scaler.transform(X_test.values.reshape(-1, 1))
            self.model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_scaled, y_test))

        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Model trained with MSE: {mse:.2f}")

    def predict(self, data):
        if self.config['model_type'] == 'random_forest':
            return self.model.predict(data)
        elif self.config['model_type'] == 'lstm':
            scaler = StandardScaler()
            data_scaled = scaler.transform(data.values.reshape(-1, 1))
            return self.model.predict(data_scaled)
