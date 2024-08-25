import os
import sys
import json
import hashlib
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from blockchain.blockchain import Blockchain
from blockchain.block import Block
from blockchain.transaction import Transaction
from blockchain.miner import Miner
from blockchain.wallet import Wallet

app = Flask(__name__)
CORS(app)

# Initialize the blockchain
blockchain = Blockchain()

# Initialize the miner
miner = Miner(blockchain)

# Initialize the wallet
wallet = Wallet()

@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    transaction = Transaction(data['sender'], data['receiver'], data['amount'])
    blockchain.add_transaction(transaction)
    miner.mine()
    return jsonify({'block': blockchain.get_latest_block().to_dict()})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = blockchain.get_transactions()
    return jsonify([t.to_dict() for t in transactions])

@app.route('/blocks', methods=['GET'])
def get_blocks():
    blocks = blockchain.get_blocks()
    return jsonify([b.to_dict() for b in blocks])

@app.route('/balance', methods=['GET'])
def get_balance():
    address = request.args.get('address')
    balance = blockchain.get_balance(address)
    return jsonify({'balance': balance})

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    transaction = Transaction(data['sender'], data['receiver'], data['amount'])
    blockchain.add_transaction(transaction)
    return jsonify({'transaction': transaction.to_dict()})

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'Blockchain node is healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
