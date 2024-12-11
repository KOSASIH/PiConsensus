import json
import requests
from datetime import datetime

class IoTIntegrationService:
    def __init__(self, device_url):
        self.device_url = device_url

    def get_device_status(self):
        """Fetch the current status of the IoT device."""
        try:
            response = requests.get(f"{self.device_url}/status")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching device status: {e}")
            return None

    def send_command(self, command):
        """Send a command to the IoT device."""
        try:
            payload = json.dumps({"command": command})
            response = requests.post(f"{self.device_url}/command", data=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending command to device: {e}")
            return None

    def log_device_data(self, data):
        """Log data received from the IoT device."""
        # Here you would typically save the data to a database
        # For demonstration, we'll just print it
        print(f"[{datetime.now()}] Device Data: {data}")

    def receive_data(self):
        """Simulate receiving data from the IoT device."""
        # In a real application, this might involve a WebSocket or MQTT subscription
        # For demonstration, we'll simulate it with a simple GET request
        try:
            response = requests.get(f"{self.device_url}/data")
            response.raise_for_status()
            data = response.json()
            self.log_device_data(data)
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error receiving data from device: {e}")
            return None

# Example usage
if __name__ == "__main__":
    device_url = "http://example-iot-device.local"  # Replace with your IoT device URL
    iot_service = IoTIntegrationService(device_url)

    # Get device status
    status = iot_service.get_device_status()
    print("Device Status:", status)

    # Send a command to the device
    command_response = iot_service.send_command("turn_on")
    print("Command Response:", command_response)

    # Receive data from the device
    data = iot_service.receive_data()
    print("Received Data:", data)
