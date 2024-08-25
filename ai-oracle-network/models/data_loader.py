import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DataLoader:
    def __init__(self, config):
        self.config = config

    def load_data(self):
        data = pd.read_csv(self.config['data_path'])
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)

        if self.config['feature_engineering']:
            data = self._feature_engineering(data)

        return data

    def _feature_engineering(self, data):
        data['moving_average'] = data['target'].rolling(window=30).mean()
        data['exponential_smoothing'] = data['target'].ewm(span=30).mean()
        return data

    def split_data(self, data):
        train_size = int(0.8 * len(data))
        train_data, test_data = data[:train_size], data[train_size:]
        return train_data, test_data

    def scale_data(self, data):
        scaler = MinMaxScaler()
        data[['target']] = scaler.fit_transform(data[['target']])
        return data
