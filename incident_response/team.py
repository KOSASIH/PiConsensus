class Team:
    def __init__(self, team_config):
        self.members = team_config['members']
        self.incidents = {}

    def assign_to_incident(self, incident):
        self.incidents[incident.id] = incident

    def get_incident(self, incident_id):
        return self.incidents.get(incident_id)
