from chatapp import create_app
from chatapp.extensions import socketio

app = create_app()

socketio.run(app, host="0.0.0.0", port=8080)