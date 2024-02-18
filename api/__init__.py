"""Module providing API functionality"""
from flask import Flask
from config import Config
from api.handlers import handlers_bp

def init_app() -> Flask:
    """
    Init Flask API based on environment type
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(handlers_bp)

    return app
