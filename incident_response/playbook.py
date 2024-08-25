class Playbook:
    def __init__(self, playbook_config):
        self.steps = playbook_config['steps']

    def run(self, incident_id):
        for step in self.steps:
            if step['type'] == 'notification':
                self.send_notification(incident_id, step['message'])
            elif step['type'] == 'task':
                self.create_task(incident_id, step['title'], step['description'])
            # Add more step types as needed

    def send_notification(self, incident_id, message):
        # Implement notification logic here
        print(f"Sending notification for incident {incident_id}: {message}")

    def create_task(self, incident_id, title, description):
        # Implement task creation logic here
        print(f"Creating task for incident {incident_id}: {title} - {description}")
