from flask import request
from flask_socketio import emit
from .extensions import socketio, cursor, con
import os
from os import getenv
from dotenv import load_dotenv
import random
import smtplib
from email.mime.text import MIMEText
import string
from hashlib import sha256
import threading
import subprocess


load_dotenv()
CLIENTS_TABLE_NAME = getenv("CLIENTS_TABLE_NAME")
SMTP_SERVER_ADDRESS = getenv("SMTP_SERVER_ADDRESS")
SMTP_SERVER_PORT = getenv("SMTP_SERVER_PORT")
AUTH_CODE_SENDER_EMAIL = getenv("AUTH_CODE_SENDER_EMAIL")
AUTH_CODE_SENDER_PASSWORD = getenv("AUTH_CODE_SENDER_PASSWORD")

email_authcodes_dict: dict[str, str] = {}
email_authcodes_dict_mutex = threading.Lock()


def generate_client_id() -> str:
    return str(random.choice(string.digits[1:])) + "".join(
        random.choices(string.digits, k=8)
    )

def generate_auth_code() -> str:
    return "".join(random.choices(string.digits, k=6))

def generate_client_color():
    while True:
        # Генерируем случайные значения для красного, зеленого и синего цветовых компонентов
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        # Вычисляем яркость цвета по формуле YIQ
        brightness = (r * 299 + g * 587 + b * 114) / 1000

        # Если яркость больше половины максимального значения (255/2 = 127.5),
        # цвет будет достаточно темным, поэтому продолжаем генерацию
        if brightness > 127.5:
            continue

        # Форматируем значения цветовых компонентов в HEX формате
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

        return hex_color

def execute_cpp_sha256(input_string):
    # Получение пути к текущему скрипту
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "SHA256/SHA256")

    # Выполнение исполняемого файла и передача входной строки в качестве аргумента
    process = subprocess.Popen([file_path, input_string], stdout=subprocess.PIPE)
    output, _ = process.communicate()

    # Декодирование вывода в строку
    result = output.decode().strip()

    return result


def hash_sha256(str_to_hash: str) -> str:
    # sha256(str_to_hash.encode("utf-8")).hexdigest() <-- реализация через python-библиотеку
    return execute_cpp_sha256(str_to_hash.encode('utf-8'))

def send_verification_code(recipient_email: str) -> str | None:
    sender_email = AUTH_CODE_SENDER_EMAIL
    sender_password = AUTH_CODE_SENDER_PASSWORD
    try:
        server = smtplib.SMTP(SMTP_SERVER_ADDRESS, SMTP_SERVER_PORT)
        server.starttls()
        server.login(sender_email, sender_password)

        auth_code = generate_auth_code()
        msg = MIMEText(auth_code)
        msg["Subject"] = "Код аутентификации"
        msg["To"] = recipient_email
        msg["From"] = sender_email
        server.sendmail(sender_email, recipient_email, msg.as_string())

    except Exception as e:
        print(f"Поймано исключение: {e}")
        return None

    return auth_code


def check_email_exists_db(email: str) -> bool:
    cursor.execute(f"SELECT * FROM {CLIENTS_TABLE_NAME} WHERE email = '{email}'")
    return cursor.fetchone()

def get_clientname_from_email_db(email: str) -> str | None:
    cursor.execute(f"SELECT clientname FROM {CLIENTS_TABLE_NAME} WHERE email = '{email}'")
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None
    


@socketio.on("connect")
def handle_connect():
    ip_addr = request.remote_addr
    sid = request.sid
    print()
    print("=========== CLIENT CONNECTED ==============")
    print(f"IP:  {ip_addr}")
    print(f"SID: {sid}")
    print()


@socketio.on("login_request")
def user_login(data):
    email = data["email"]
    psw = data["password"]
    psw_hash = hash_sha256(psw)

    print(f"========= LOGIN REQUEST {email}, {psw} ==========")

    cursor.execute(
        f"SELECT clientname, hexcolor FROM {CLIENTS_TABLE_NAME} WHERE email = '{email}' AND passwordhash = X'{psw_hash}'"
    )
    result = cursor.fetchone()

    if result:
        clientname = result[0]
        clientcolor = result[1]
        emit("login_response", {"success": True, "clientname": clientname, "clientcolor": clientcolor})

        print(f"========= LOGIN RESPONSE EMITTED {clientname}, {clientcolor} ==========")
    else:
        emit("login_response", {"success": False})


# Клиент отправил почту (отправка кода верификации на почту клиента)
@socketio.on("email_code_request")
def email_code_request(data):
    recipient_email = data["email"]

    # Если такая почта уже есть в БД, сообщить на клиент
    if check_email_exists_db(recipient_email):
        emit("email_error", {"error_msg": "Пользователь с таким email уже существует"})
    else:
        auth_code = send_verification_code(recipient_email)

        # Запись пары (почта: код) в словарь с защитой от множественного использования (мьютекс)
        with email_authcodes_dict_mutex:
            email_authcodes_dict[recipient_email] = auth_code

        response = {"success": auth_code is not None, "email": recipient_email}
        emit("email_code_response", response)


# Клиент отправил код верификации (проверка кода верификации)
@socketio.on("auth_code_verification")
def email_code_verification(data):
    clientEmail = data["email"]
    clientAuthCode = data["authCode"]

    with email_authcodes_dict_mutex:
        serverAuthCode = email_authcodes_dict[clientEmail]

    if clientAuthCode == serverAuthCode:
        emit("auth_code_verification_success")
    else:
        emit("auth_code_verification_error", {"error_msg": "Код неверный!"})


@socketio.on("reg")
def user_reg(data):
    email = data["email"]
    username = data["username"]
    psw = data["password"]
    psw_hash = hash_sha256(psw)

    cursor.execute(
        f"SELECT * FROM {CLIENTS_TABLE_NAME} WHERE clientname = '{username}'"
    )
    if cursor.fetchone():
        emit("existing_user", {"error": True})
    else:
        client_id = generate_client_id()
        color = generate_client_color()
        cursor.execute(
            f"INSERT INTO {CLIENTS_TABLE_NAME} (id, clientname, passwordhash, email, hexcolor) VALUES ({client_id}, '{username}', X'{psw_hash}', '{email}', '{color}')",
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
            f"UPDATE {CLIENTS_TABLE_NAME} SET passwordhash = X'{psw_hash}' WHERE clientname = '{username}'"
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
    clientname = data["clientname"]
    clientcolor = data["clientcolor"]
    message = data["message"]

    print(f"Message request: {clientname} : {message}")

    response = { "clientname": clientname, "clientcolor": clientcolor, "message": message }
    emit("chat_message_response", response, broadcast=True)