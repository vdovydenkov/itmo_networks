from flask import Flask
from app.config import Settings
from app.routes import main, api

def create_app():
    app = Flask(__name__)
    app.secret_key = Settings.SECRET_KEY

    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)

    return app
