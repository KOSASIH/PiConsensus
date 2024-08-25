import os
import sys
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from models.oracle_model import OracleModel
from data.data_loader import DataLoader

app = Flask(__name__)
CORS(app)

# Load the configuration file
with open('config.json') as f:
    config = json.load(f)

# Initialize the data loader
data_loader = DataLoader(config)

# Initialize the oracle model
oracle_model = OracleModel(config)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    X = data_loader.load_data(data)
    prediction = oracle_model.predict(X)
    return jsonify({'prediction': prediction})

@app.route('/train', methods=['POST'])
def train():
    data = request.get_json()
    X, y = data_loader.load_data(data)
    oracle_model.train(X, y)
    return jsonify({'status': 'Model trained successfully'})

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'Oracle node is healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
