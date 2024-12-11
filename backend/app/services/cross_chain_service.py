import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrossChainService:
    def __init__(self, blockchain_configs):
        """
        Initialize the CrossChainService with configurations for different blockchains.
        
        :param blockchain_configs: A dictionary containing blockchain configurations.
        """
        self.blockchain_configs = blockchain_configs

    def get_blockchain_data(self, blockchain_name, endpoint, params=None):
        """
        Fetch data from a specified blockchain.

        :param blockchain_name: The name of the blockchain to query.
        :param endpoint: The API endpoint to call.
        :param params: Optional parameters for the API call.
        :return: The response data from the blockchain.
        """
        if blockchain_name not in self.blockchain_configs:
            logger.error("Blockchain configuration for '%s' not found.", blockchain_name)
            raise ValueError("Invalid blockchain name")

        url = f"{self.blockchain_configs[blockchain_name]['base_url']}/{endpoint}"
        try:
            logger.info("Fetching data from %s: %s", blockchain_name, url)
            response = requests.get(url, params=params)
            response.raise_for_status()
            logger.info("Data fetched successfully from %s", blockchain_name)
            return response.json()
        except Exception as e:
            logger.error("Error fetching data from %s: %s", blockchain_name, e)
            raise

    def transfer_assets(self, from_chain, to_chain, asset_data):
        """
        Transfer assets from one blockchain to another.

        :param from_chain: The name of the source blockchain.
        :param to_chain: The name of the destination blockchain.
        :param asset_data: A dictionary containing asset transfer details.
        :return: The transaction result.
        """
        if from_chain not in self.blockchain_configs or to_chain not in self.blockchain_configs:
            logger.error("Invalid blockchain names: %s, %s", from_chain, to_chain)
            raise ValueError("Invalid blockchain names")

        # Example of transferring assets (this will vary based on the blockchain)
        from_url = self.blockchain_configs[from_chain]['base_url'] + '/transfer'
        to_url = self.blockchain_configs[to_chain]['base_url'] + '/receive'

        try:
            logger.info("Initiating asset transfer from %s to %s", from_chain, to_chain)
            # Step 1: Transfer from the source blockchain
            transfer_response = requests.post(from_url, json=asset_data)
            transfer_response.raise_for_status()
            transfer_result = transfer_response.json()

            # Step 2: Receive on the destination blockchain
            receive_response = requests.post(to_url, json=transfer_result)
            receive_response.raise_for_status()
            logger.info("Asset transfer completed successfully.")
            return receive_response.json()
        except Exception as e:
            logger.error("Error during asset transfer: %s", e)
            raise

    def get_transaction_status(self, blockchain_name, tx_id):
        """
        Get the status of a transaction on a specified blockchain.

        :param blockchain_name: The name of the blockchain to query.
        :param tx_id: The transaction ID to check.
        :return: The transaction status.
        """
        endpoint = f"transaction/{tx_id}/status"
        return self.get_blockchain_data(blockchain_name, endpoint)

# Example usage
if __name__ == "__main__":
    # Example blockchain configurations
    blockchain_configs = {
        "Ethereum": {
            "base_url": "https://api.etherscan.io/api"
        },
        "BinanceSmartChain": {
            "base_url": "https://api.bscscan.com/api"
        }
    }

    service = CrossChainService(blockchain_configs)

    # Fetching data from Ethereum
    try:
        eth_data = service.get_blockchain_data("Ethereum", "stats")
        print("Ethereum Data:", eth_data)
    except Exception as e:
        print("Error fetching Ethereum data:", e)

    # Example asset transfer
    asset_data = {
        "from": "0xYourEthereumAddress",
        "to": "0xYourBSCAddress",
        "amount": 1.0,
        "token": "ETH"
    }
    try:
        transfer_result = service.transfer_assets("Ethereum", "BinanceSmartChain", asset_data)
        print("Transfer Result:", transfer_result)
    except Exception as e:
        print("Error during asset transfer:", e)

    # Checking transaction status
    try:
        tx_status = service.get_transaction_status(" Ethereum", "0xYourTransactionID")
        print("Transaction Status:", tx_status)
    except Exception as e:
        print("Error fetching transaction status:", e) ```python
    # Example of checking transaction status
    try:
        tx_status = service.get_transaction_status("Ethereum", "0xYourTransactionID")
        print("Transaction Status:", tx_status)
    except Exception as e:
        print("Error fetching transaction status:", e)
