from flask import Flask
from .routes import app as routes_app  # Import the routes blueprint

def create_app():
    app = Flask(__name__)

    # Register the blueprint
    app.register_blueprint(routes_app)

    return app
