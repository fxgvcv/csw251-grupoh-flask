from flask import Flask
from src.repositories.building_repository import BuildingRepository
from src.repositories.room_repository import RoomRepository
from src.services.building_service import BuildingService
from src.services.room_service import RoomService
from src.controllers.building_controller import BuildingController
from src.controllers.room_controller import RoomController
from src.models.building_model import Building
from src.models.room_model import Room
from src.utils.shared.db.base import Base, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./local.db'
db.init_app(app)

with app.app_context():
    # Create tables if they don't exist
    db.create_all()
    # Inject repositories using the current db.session
    app.building_repository = BuildingRepository(db.session)
    app.room_repository = RoomRepository(db.session)
    # Inject services using the repositories
    app.building_service = BuildingService(app.building_repository)
    app.room_service = RoomService(app.room_repository)
    # Inject controllers using the services
    app.building_controller = BuildingController(app.building_service)
    app.room_controller = RoomController(app.room_service)

# Register routes for building and room controllers
app.register_blueprint(app.building_controller.blueprint)
app.register_blueprint(app.room_controller.blueprint)

@app.route('/')
def health_check():
    return {'message': 'Alive!'}, 200