import os
from src.utils.config.config import DevConfig, ProdConfig
from flask import Flask
from flask_cors import CORS
from src.repositories.building_repository import BuildingRepository
from src.repositories.room_repository import RoomRepository
from src.repositories.user_repository import UserRepository
from src.services.building_service import BuildingService
from src.services.room_service import RoomService
from src.services.user_service import UserService
from src.controllers.building_controller import BuildingController
from src.controllers.room_controller import RoomController
from src.controllers.user_controller import UserController
from src.models.building_model import Building
from src.models.room_model import Room
from src.models.user_model import User
from src.utils.shared.db.base import Base, db

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

if os.getenv("FLASK_ENV") == "development":
    app.config.from_object(DevConfig)
else:
    app.config.from_object(ProdConfig)
    
db.init_app(app)

with app.app_context():
    # Create tables if they don't exist
    db.create_all()
    # Inject repositories using the current db.session
    app.building_repository = BuildingRepository(db.session)
    app.room_repository = RoomRepository(db.session)
    app.user_repository = UserRepository(db.session)
    # Inject services using the repositories
    app.building_service = BuildingService(app.building_repository)
    app.room_service = RoomService(app.room_repository)
    app.user_service = UserService(app.user_repository)
    # Inject controllers using the services
    app.building_controller = BuildingController(app.building_service)
    app.room_controller = RoomController(app.room_service)
    app.user_controller = UserController(app.user_service)

# Register routes for building, room, and user controllers
app.register_blueprint(app.building_controller.blueprint)
app.register_blueprint(app.room_controller.blueprint)
app.register_blueprint(app.user_controller.blueprint)

@app.route('/')
def health_check():
    return {'message': 'Alive!'}, 200