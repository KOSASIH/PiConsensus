import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

class IntrusionDetector:
    def __init__(self, data):
        self.data = data
        self.encoder = LabelEncoder()
        self.model = RandomForestClassifier(n_estimators=100)

    def train(self):
        X = self.data.drop('label', axis=1)
        y = self.encoder.fit_transform(self.data['label'])
        self.model.fit(X, y)

    def predict(self, new_data):
        X_new = new_data.drop('label', axis=1)
        predictions = self.model.predict(X_new)
        return self.encoder.inverse_transform(predictions)

    def evaluate(self, labels):
        accuracy = self.model.score(self.data.drop('label', axis=1), labels)
        return accuracy

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def main():
    file_path = 'data/intrusion_detection_data.csv'
    data = load_data(file_path)
    detector = IntrusionDetector(data)
    detector.train()
    new_data = pd.DataFrame({'feature1': [10, 20, 30], 'feature2': [40, 50, 60], 'label': ['normal', 'anomaly', 'normal']})
    predictions = detector.predict(new_data)
    print(predictions)

if __name__ == '__main__':
    main()
