from flask import Flask

from .routes import main
from .events import socketio


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config["SECRET_KEY"] = "secret"

    app.register_blueprint(main)

    socketio.init_app(app)

    return app
