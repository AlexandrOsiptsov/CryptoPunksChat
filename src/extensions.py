from os import getenv
from dotenv import load_dotenv
from flask_socketio import SocketIO 
import pymysql

socketio = SocketIO()

load_dotenv()
DB_HOST = getenv("DB_HOST")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_NAME = getenv("DB_NAME")

con = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

cursor = con.cursor()
