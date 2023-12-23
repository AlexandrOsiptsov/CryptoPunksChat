from dotenv import load_dotenv
from os import getenv 
from src import create_app
from src.extensions import socketio

load_dotenv()
SERVER_HOST = getenv("SERVER_HOST")
SERVER_PORT = int(getenv("SERVER_PORT"))

app = create_app()

socketio.run(app, host=SERVER_HOST, port=SERVER_PORT)
