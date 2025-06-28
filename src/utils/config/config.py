import os

class DevConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL", "sqlite:///local.db")
    DEBUG = True
    # Add other dev settings

class ProdConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL")
    DEBUG = False