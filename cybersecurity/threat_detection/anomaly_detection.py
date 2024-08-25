import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    def __init__(self, data):
        self.data = data
        self.scaler = StandardScaler()
        self.model = IsolationForest(contamination=0.1)

    def train(self):
        self.scaler.fit(self.data)
        scaled_data = self.scaler.transform(self.data)
        self.model.fit(scaled_data)

    def predict(self, new_data):
        scaled_new_data = self.scaler.transform(new_data)
        predictions = self.model.predict(scaled_new_data)
        return predictions

    def evaluate(self, labels):
        accuracy = self.model.score(self.data, labels)
        return accuracy

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def main():
    file_path = 'data/anomaly_detection_data.csv'
    data = load_data(file_path)
    detector = AnomalyDetector(data)
    detector.train()
    new_data = pd.DataFrame({'feature1': [10, 20, 30], 'feature2': [40, 50, 60]})
    predictions = detector.predict(new_data)
    print(predictions)

if __name__ == '__main__':
    main()
