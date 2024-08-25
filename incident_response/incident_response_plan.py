import os
import json
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from incident_response.incident import Incident
from incident_response.team import Team
from incident_response.playbook import Playbook

app = Flask(__name__)
CORS(app)

# Load incident response plan from JSON file
with open('incident_response_plan.json') as f:
    incident_response_plan = json.load(f)

# Initialize incident response team
team = Team(incident_response_plan['team'])

# Initialize playbooks
playbooks = {}
for playbook_name, playbook_config in incident_response_plan['playbooks'].items():
    playbooks[playbook_name] = Playbook(playbook_config)

@app.route('/incident', methods=['POST'])
def create_incident():
    data = request.get_json()
    incident = Incident(data['title'], data['description'], data['severity'])
    team.assign_to_incident(incident)
    return jsonify({'incident_id': incident.id})

@app.route('/incident/<incident_id>', methods=['GET'])
def get_incident(incident_id):
    incident = team.get_incident(incident_id)
    if incident:
        return jsonify(incident.to_dict())
    else:
        return jsonify({'error': 'Incident not found'}), 404

@app.route('/incident/<incident_id>/playbook', methods=['POST'])
def run_playbook(incident_id):
    data = request.get_json()
    playbook_name = data['playbook_name']
    playbook = playbooks[playbook_name]
    playbook.run(incident_id)
    return jsonify({'message': 'Playbook executed successfully'})

@app.route('/incident/<incident_id>/status', methods=['GET'])
def get_incident_status(incident_id):
    incident = team.get_incident(incident_id)
    if incident:
        return jsonify({'status': incident.status})
    else:
        return jsonify({'error': 'Incident not found'}), 404

@app.route('/incident/<incident_id>/update', methods=['PATCH'])
def update_incident(incident_id):
    data = request.get_json()
    incident = team.get_incident(incident_id)
    if incident:
        incident.update(data)
        return jsonify({'message': 'Incident updated successfully'})
    else:
        return jsonify({'error': 'Incident not found'}), 404

@app.route('/incident/<incident_id>/close', methods=['POST'])
def close_incident(incident_id):
    incident = team.get_incident(incident_id)
    if incident:
        incident.close()
        return jsonify({'message': 'Incident closed successfully'})
    else:
        return jsonify({'error': 'Incident not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
