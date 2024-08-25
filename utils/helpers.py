import requests
import json
from typing import List, Dict
from .constants import API_ENDPOINT_IPFS, API_ENDPOINT_ETHEREUM, PINATA_PINNING_SERVICE

def get_ipfs_client() -> requests.Session:
    # Create an IPFS client session
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})
    return session

def get_ethereum_client() -> requests.Session:
    # Create an Ethereum client session
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})
    return session

def pin_file_to_ipfs(file_path: str) -> str:
    # Pin a file to IPFS using Pinata
    with open(file_path, 'rb') as f:
        file_data = f.read()
    response = requests.post(PINATA_PINNING_SERVICE, files={'file': file_data})
    return response.json()['IpfsHash']

def get_ipfs_hash(file_path: str) -> str:
    # Get the IPFS hash of a file
    with open(file_path, 'rb') as f:
        file_data = f.read()
    response = requests.post(API_ENDPOINT_IPFS + '/api/v0/add', files={'file': file_data})
    return response.json()['Hash']

def get_ethereum_block_number() -> int:
    # Get the current Ethereum block number
    response = requests.get(API_ENDPOINT_ETHEREUM + '/blockNumber')
    return int(response.json()['result'], 16)

def get_ethereum_transaction_receipt(tx_hash: str) -> Dict:
    # Get the transaction receipt of an Ethereum transaction
    response = requests.get(API_ENDPOINT_ETHEREUM + '/getTransactionReceipt', params={'tx_hash': tx_hash})
    return response.json()['result']

def wait_for_ethereum_transaction(tx_hash: str, max_retries: int = 5) -> Dict:
    # Wait for an Ethereum transaction to be mined
    for i in range(max_retries):
        response = requests.get(API_ENDPOINT_ETHEREUM + '/getTransactionReceipt', params={'tx_hash': tx_hash})
        if response.json()['result']['status'] == '0x1':
            return response.json()['result']
        time.sleep(1)
    raise Exception('Transaction not mined after {} retries'.format(max_retries))
