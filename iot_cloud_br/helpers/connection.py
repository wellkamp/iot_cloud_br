import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="USUARIO",
    port = 3306,
    password="SENHA",
    auth_plugin='mysql_native_password',
    database='iot_cloud_br'
)


def get_connection():
    return db
