from src.controllers.interfaces.building_controller import InterfaceBuildingController

from flask import Blueprint, request, jsonify, abort
from src.services.interfaces.building_service import InterfaceBuildingService

class BuildingController(InterfaceBuildingController):
    def __init__(self, service: InterfaceBuildingService):
        self.service = service
        self.blueprint = Blueprint('building', __name__, url_prefix='/buildings')
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.get_all_buildings, methods=['GET'])
        self.blueprint.add_url_rule('/<string:building_id>', view_func=self.get_building_by_id, methods=['GET'])
        self.blueprint.add_url_rule('/', view_func=self.create_building, methods=['POST'])
        self.blueprint.add_url_rule('/<string:building_id>', view_func=self.update_building, methods=['PUT'])
        self.blueprint.add_url_rule('/<string:building_id>', view_func=self.delete_building, methods=['DELETE'])

    def get_all_buildings(self):
        buildings = self.service.get_all_buildings()
        return jsonify([b.to_dict() for b in buildings]), 200

    def get_building_by_id(self, building_id):
        building = self.service.get_building_by_id(building_id)
        if not building:
            abort(404, description="Building not found")
        return jsonify(building.to_dict()), 200

    def create_building(self):
        data = request.get_json()
        building = self.service.create_building(data)
        return jsonify(building.to_dict()), 201

    def update_building(self, building_id):
        data = request.get_json()
        updated = self.service.update_building(building_id, data)
        if not updated:
            abort(404, description="Building not found")
        return jsonify(updated.to_dict()), 200

    def delete_building(self, building_id):
        deleted = self.service.delete_building(building_id)
        if not deleted:
            abort(404, description="Building not found")
        return jsonify(deleted.to_dict()), 200