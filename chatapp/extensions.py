from flask_socketio import SocketIO 
import pymysql

socketio = SocketIO()

con = pymysql.connect(host='localhost',user='root',
                      password='3621',database='pythonlogin')
cursor = con.cursor()