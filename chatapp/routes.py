# -*- coding: cp1251 -*-
from flask import Flask, Blueprint, request, jsonify, session, render_template, url_for
from .AesKey import preSet
from .credential import *
import uuid

main = Blueprint("main", __name__)

modulus,exponent, s_key=preSet() #инициализация констант необходимых rsa

clear_file() #подготовка файла all_credits.txt

@main.route("/")
def index():
    global exponent
    global modulus
    client_id = session.get('client_id')
    if  not client_id or not exponent or not modulus:
        client_id = str(uuid.uuid4())
        #ниже приведен возможный вариант идентификации пользователя
        #session['client_id'] = client_id
        #client_ip = request.remote_addr
        #client_port = request.environ['REMOTE_PORT']
        #client_ip_port = f"{client_ip}:{client_port}"
        #session['client_ip_port'] = client_ip_port 
        
        
    return render_template('index.html', client_id=client_id,
                          exponent=exponent, modulus=modulus) #передача необходимых параметров для выполнения процедуры формирования ключа


#выполняестя для получения client_id и привязки к нему ключа
@main.route('/get_client_id', methods=['GET'])
def get_client_id():
    client_id = session.get('client_id')
    return jsonify({'client_id': client_id})

@main.route('/process_data', methods=['POST'])
def process_data():
    session['client_id'] = request.json.get('client_id')
    session['e_msg'] = request.json.get('e_msg') #запрс на ключ AES, зашифрованный RSA

    client_id = session.get('client_id')
    e_msg = session.get('e_msg')

    #client_ip = request.remote_addr
    #client_port = request.environ['REMOTE_PORT']
    #client_ip_port = f"{client_ip}:{client_port}"

    
    d_msg=pow(int(e_msg), s_key, modulus) #расшифровка ключа AES

    add_aes_key(client_id, d_msg) #добавление ключа в файл all_credentials.txt

    response_data = {'message': 'Data is processed', 'd_msg': get_aes_key(client_id),
                    'client_id': client_id} #сообщение отладки
    return jsonify(response_data)



@main.route('/chat')
def chat():
    return render_template('chat.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/forgot_psw')
def forgot_psw():
    return render_template('forgot_psw.html')