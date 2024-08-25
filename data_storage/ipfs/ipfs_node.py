import os
import subprocess
import threading
import time

class IPFSNode:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.process = None

    def start(self):
        if not self.process:
            self.process = subprocess.Popen(['ipfs', 'daemon', '--repo', self.repo_path])
            threading.Thread(target=self.wait_for_ready).start()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def wait_for_ready(self):
        while True:
            try:
                response = requests.get('http://localhost:5001/api/v0/id')
                if response.status_code == 200:
                    break
            except requests.ConnectionError:
                pass
            time.sleep(1)

    def get_api_url(self):
        return 'http://localhost:5001'

    def __del__(self):
        self.stop()
