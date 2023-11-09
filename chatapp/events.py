from flask import request
from flask_socketio import emit
from .extensions import socketio
import datetime
from time import sleep


class Client:
    def __init__(self, ip, sid, username):
        self.ip = ip
        self.sid = sid
        self.username = username
        self.last_connect_time = None
        self.last_disconnect_time = None

    def set_last_connect_time(self, time):
        self.last_connect_time = time

    def set_last_disconnect_time(self, time):
        self.last_disconnect_time = time

    def set_sid(self, sid):
        self.sid = sid

    def set_username(self, username):
        self.username = username

    def connect(self):
        self.set_last_connect_time(datetime.datetime.now())
        print("==================== CLIENT CONNECTED ====================")
        print(f"Client IP:  {self.ip}")
        print(f"Client SID: {self.sid}")

    def disconnect(self):
        self.set_last_disconnect_time(datetime.datetime.now())
        print("------------------ CLIENT DISCONNECTED ------------------")
        print(f"Client IP:  {self.ip}")
        print(f"Client SID: {self.sid}")
        print(f"Time:       {self.last_disconnect_time}")

    def is_connected(self):
        if self.last_disconnect_time != None:
            return self.last_connect_time > self.last_disconnect_time
        return True

    def get_disconnect_time_diff(self):
        if self.last_disconnect_time is None:
            return (datetime.datetime.now() - datetime.datetime.min).total_seconds()
        return (datetime.datetime.now() - self.last_disconnect_time).total_seconds()

    def print_self(self):
        print(f"IP:       {self.ip}")
        print(f"Username: {self.username}")
        print(f"Connect time: {self.last_connect_time}")
        print(f"Discnct time: {self.last_disconnect_time}")
        print(f"Is connected: {self.is_connected()}")


clients: dict[str, Client] = {}


@socketio.on("connect")
def handle_connect():
    ip_addr = request.remote_addr
    sid = request.sid
    if not ip_addr in clients:
        clients[ip_addr] = Client(ip_addr, sid, None)
    clients[ip_addr].connect()


@socketio.on("user_chat_join")
def handle_username_send(username):
    ip_addr = request.remote_addr
    clients[ip_addr].set_username(username)

    if (
        clients[ip_addr].get_disconnect_time_diff() > 10
        and not clients[ip_addr].is_connected()
    ):
        response = {"username": "Server", "message": f"{username} connected"}
        emit("chat_message_response", response, broadcast=True)


@socketio.on("disconnect")
def handle_disconnect():
    ip_addr = request.remote_addr
    username = clients[ip_addr].username
    clients[ip_addr].disconnect()

    sleep(10)

    if ip_addr in clients and not clients[ip_addr].is_connected():
        response = {
            "username": "Server",
            "message": f"{username} disconnected",
        }
        emit("chat_message_response", response, broadcast=True)
        clients.pop(ip_addr)


@socketio.on("navigate")
def handle_navigate(url):
    emit("navigate", url)


@socketio.on("chat_message_request")
def handle_chat_message_request(data):
    username = data["username"]
    message = data["message"]

    print(f"Message request: {username} : {message}")

    response = {"username": username, "message": message}
    emit("chat_message_response", response, broadcast=True)

    print("Response sent")
