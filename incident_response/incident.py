class Incident:
    def __init__(self, title, description, severity):
        self.id = uuid.uuid4()
        self.title = title
        self.description = description
        self.severity = severity
        self.status = 'open'
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update(self, data):
        self.title = data.get('title', self.title)
        self.description = data.get('description', self.description)
        self.severity = data.get('severity', self.severity)
        self.status = data.get('status', self.status)
        self.updated_at = datetime.datetime.now()

    def close(self):
        self.status = 'closed'
        self.updated_at = datetime.datetime.now()
