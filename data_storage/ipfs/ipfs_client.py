import requests
import json

class IPFSClient:
    def __init__(self, node_url):
        self.node_url = node_url

    def add_file(self, file_path):
        with open(file_path, 'rb') as f:
            file_data = f.read()
        response = requests.post(f'{self.node_url}/api/v0/add', files={'file': file_data})
        return response.json()['Hash']

    def get_file(self, hash):
        response = requests.get(f'{self.node_url}/api/v0/cat?arg={hash}')
        return response.content

    def list_files(self):
        response = requests.post(f'{self.node_url}/api/v0/ls')
        return response.json()

    def pin_file(self, hash):
        response = requests.post(f'{self.node_url}/api/v0/pin/add?arg={hash}')
        return response.json()

    def unpin_file(self, hash):
        response = requests.post(f'{self.node_url}/api/v0/pin/rm?arg={hash}')
        return response.json()
