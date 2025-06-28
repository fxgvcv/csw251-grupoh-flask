from src.controllers.interfaces.room_controller import InterfaceRoomController

from flask import Blueprint, request, jsonify, abort
from src.services.interfaces.room_service import InterfaceRoomService

class RoomController(InterfaceRoomController):
    def __init__(self, service: InterfaceRoomService):
        self.service = service
        self.blueprint = Blueprint('room', __name__, url_prefix='/rooms')
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.get_all_rooms, methods=['GET'])
        self.blueprint.add_url_rule('/<string:room_id>', view_func=self.get_room_by_id, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create_room, methods=['POST'])
        self.blueprint.add_url_rule('/<string:room_id>', view_func=self.update_room, methods=['PUT'])
        self.blueprint.add_url_rule('/<string:room_id>', view_func=self.delete_room, methods=['DELETE'])

    def get_all_rooms(self):
        rooms = self.service.get_all_rooms()
        return jsonify([r.to_dict() for r in rooms]), 200

    def get_room_by_id(self, room_id):
        room = self.service.get_room_by_id(room_id)
        if not room:
            abort(404, description="Room not found")
        return jsonify(room.to_dict()), 200

    def create_room(self):
        data = request.get_json()
        room = self.service.create_room(data)
        return jsonify(room.to_dict()), 201

    def update_room(self, room_id):
        data = request.get_json()
        updated = self.service.update_room(room_id, data)
        if not updated:
            abort(404, description="Room not found")
        return jsonify(updated.to_dict()), 200

    def delete_room(self, room_id):
        deleted = self.service.delete_room(room_id)
        if not deleted:
            abort(404, description="Room not found")
        return jsonify(deleted.to_dict()), 200
