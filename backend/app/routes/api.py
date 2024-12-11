from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..services.security_service import SecurityService
from ..models import User  # Assuming you have a User model defined in your models

# Create a Blueprint for the API
api_bp = Blueprint('api', __name__)

# Initialize the SecurityService
security_service = SecurityService()

@api_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    try:
        user = security_service.create_user(username, password)
        return jsonify({"msg": "User  created", "user_id": user.id}), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@api_bp.route('/login', methods=['POST'])
def login():
    """Login a user and return an access token."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    token = security_service.authenticate_user(username, password)
    if token:
        return jsonify({"access_token": token}), 200
    return jsonify({"msg": "Bad username or password"}), 401

@api_bp.route('/current_user', methods=['GET'])
@jwt_required()
def current_user():
    """Get the current authenticated user."""
    user = security_service.get_current_user()
    return jsonify({"username": user.username}), 200

@api_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout the user (invalidate the token)."""
    return security_service.logout_user()

# Register the Blueprint in the main application
def register_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')
