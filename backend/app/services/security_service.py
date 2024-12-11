from flask import current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from .models import User  # Assuming you have a User model defined in your models

class SecurityService:
    def __init__(self, app):
        self.app = app
        self.jwt = JWTManager(app)

    def create_user(self, username, password):
        """Create a new user with a hashed password."""
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        # Save the new user to the database
        new_user.save()  # Assuming you have a save method in your User model
        return new_user

    def authenticate_user(self, username, password):
        """Authenticate a user and return an access token if successful."""
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            return access_token
        return None

    @jwt_required()
    def get_current_user(self):
        """Get the current authenticated user."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user

    @jwt_required()
    def logout_user(self):
        """Logout the user (invalidate the token)."""
        # In a real application, you might want to implement a token blacklist
        return {"msg": "User  logged out successfully"}, 200

# Example usage
if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
    security_service = SecurityService(app)

    @app.route('/register', methods=['POST'])
    def register():
        # Example registration endpoint
        username = "example_user"  # Replace with actual data from request
        password = "example_password"  # Replace with actual data from request
        user = security_service.create_user(username, password)
        return {"msg": "User  created", "user_id": user.id}, 201

    @app.route('/login', methods=['POST'])
    def login():
        # Example login endpoint
        username = "example_user"  # Replace with actual data from request
        password = "example_password"  # Replace with actual data from request
        token = security_service.authenticate_user(username, password)
        if token:
            return {"access_token": token}, 200
        return {"msg": "Bad username or password"}, 401

    @app.route('/current_user', methods=['GET'])
    @jwt_required()
    def current_user():
        user = security_service.get_current_user()
        return {"username": user.username}, 200

    @app.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        return security_service.logout_user()

    app.run(debug=True)
