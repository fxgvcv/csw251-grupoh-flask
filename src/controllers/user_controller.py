from src.controllers.interfaces.user_controller import InterfaceUserController

from flask import Blueprint, request, jsonify, abort
from src.services.interfaces.user_service import InterfaceUserService

class UserController(InterfaceUserController):
    def __init__(self, service: InterfaceUserService):
        self.service = service
        self.blueprint = Blueprint('user', __name__, url_prefix='/users')
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.get_all_users, methods=['GET'])
        self.blueprint.add_url_rule('/<string:user_id>', view_func=self.get_user_by_id, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create_user, methods=['POST'])
        self.blueprint.add_url_rule('/<string:user_id>', view_func=self.update_user, methods=['PUT'])
        self.blueprint.add_url_rule('/<string:user_id>', view_func=self.delete_user, methods=['DELETE'])
        self.blueprint.add_url_rule('/username/<string:username>', view_func=self.get_user_by_username, methods=['GET'])
        self.blueprint.add_url_rule('/authenticate', view_func=self.authenticate_user, methods=['POST'])

    def get_all_users(self):
        users = self.service.get_all_users()
        # Don't return password in the response
        return jsonify([{k: v for k, v in user.to_dict().items() if k != 'password'} for user in users]), 200

    def get_user_by_id(self, user_id):
        user = self.service.get_user(user_id)
        if not user:
            abort(404, description="User not found")
        # Don't return password in the response
        user_dict = user.to_dict()
        user_dict.pop('password', None)
        return jsonify(user_dict), 200

    def create_user(self):
        data = request.get_json()
        
        # Validate required fields
        if not data or 'username' not in data or 'email' not in data or 'password' not in data:
            abort(400, description="Missing required fields: username, email, password")
        
        user = self.service.create_user(data)
        # Don't return password in the response
        user_dict = user.to_dict()
        user_dict.pop('password', None)
        return jsonify(user_dict), 201

    def update_user(self, user_id):
        data = request.get_json()
        updated = self.service.update_user(user_id, data)
        if not updated:
            abort(404, description="User not found")
        # Don't return password in the response
        user_dict = updated.to_dict()
        user_dict.pop('password', None)
        return jsonify(user_dict), 200

    def delete_user(self, user_id):
        deleted = self.service.delete_user(user_id)
        if not deleted:
            abort(404, description="User not found")
        # Don't return password in the response
        user_dict = deleted.to_dict()
        user_dict.pop('password', None)
        return jsonify(user_dict), 200

    def get_user_by_username(self, username):
        user = self.service.get_user_by_username(username)
        if not user:
            abort(404, description="User not found")
        # Don't return password in the response
        user_dict = user.to_dict()
        user_dict.pop('password', None)
        return jsonify(user_dict), 200

    def authenticate_user(self):
        data = request.get_json()
        
        # Validate required fields
        if not data or 'username' not in data or 'password' not in data:
            abort(400, description="Missing required fields: username, password")
        
        user = self.service.authenticate(data['username'], data['password'])
        if not user:
            abort(401, description="Invalid credentials")
        
        # Don't return password in the response
        user_dict = user.to_dict()
        user_dict.pop('password', None)
        return jsonify({
            'message': 'Authentication successful',
            'user': user_dict
        }), 200
