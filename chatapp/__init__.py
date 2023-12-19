from flask import Flask
import os
from dotenv import load_dotenv
from .routes import main
from .events import socketio

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def create_app():
    app = Flask(__name__, static_folder="static")
    app.config["SECRET_KEY"] = SECRET_KEY

    app.register_blueprint(main)

    socketio.init_app(app)

    return app
