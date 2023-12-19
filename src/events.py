from flask import request, session
from flask_socketio import emit
from .extensions import socketio, cursor, con
from os import getenv
from dotenv import load_dotenv
import random
import string
from hashlib import sha256

def generate_client_id() -> str:
    return str(random.choice(string.digits[1:])) + "".join(random.choices(string.digits, k=8))

def hash_sha256(str_to_hash: str) -> str:
    return sha256(str_to_hash.encode('utf-8')).hexdigest()


load_dotenv()
CLIENTS_TABLE_NAME = getenv("CLIENTS_TABLE_NAME")


@socketio.on("connect")
def handle_connect():
    ip_addr = request.remote_addr
    sid = request.sid
    print()
    print("=========== CLIENT CONNECTED ==============")
    print(f"IP:  {ip_addr}")
    print(f"SID: {sid}")
    print()


@socketio.on("login")
def user_login(data):
    username = data["username"]
    psw = data["password"]
    psw_hash = hash_sha256(psw)

    cursor.execute(
        f"SELECT * FROM {CLIENTS_TABLE_NAME} WHERE clientname = '{username}' AND passwordhash = X'{psw_hash}'"
    )
    user = cursor.fetchone()

    if user:
        emit("login_response", {"success": True})
    else:
        emit("login_response", {"success": False})


@socketio.on("reg")
def user_reg(data):
    email = data["email"]
    username = data["username"]
    psw = data["password"]
    psw_hash = hash_sha256(psw)

    cursor.execute(
        f"SELECT * FROM {CLIENTS_TABLE_NAME} WHERE clientname = '{username}'"
    )

    existing_user = cursor.fetchone()

    if existing_user:
        emit("existing_user", {"error": True})
    else:
        client_id = generate_client_id()
        cursor.execute(
            f"INSERT INTO {CLIENTS_TABLE_NAME} (id, clientname, passwordhash, email) VALUES ({client_id}, '{username}', X'{psw_hash}', '{email}')",
        )
        con.commit()
        emit("reg_response", {"success": True})


@socketio.on("forgot_psw")
def change_psw(data):
    username = data["username"]
    newpassword = data["newpassword"]
    psw_hash = hash_sha256(newpassword)

    cursor.execute(
        f"SELECT * FROM {CLIENTS_TABLE_NAME} WHERE clientname = '{username}'"
    )
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.execute(
            f"UPDATE ACCOUNTS SET passwordhash = X'{psw_hash}' WHERE clientname = '{username}'"
        )
        con.commit()
        emit("change_psw", {"success": True})
    else:
        emit("existing_user", {"error": True})


@socketio.on("user_chat_join")
def handle_username_send(username):
    ip_addr = request.remote_addr
    response = {"username": "Server", "message": f"{username} connected"}
    emit("chat_message_response", response, broadcast=True)


@socketio.on("disconnect")
def handle_disconnect():
    ip_addr = request.remote_addr
    response = {
        "username": "Server",
        "message": "disconnected",
    }
    emit("chat_message_response", response, broadcast=True)


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
