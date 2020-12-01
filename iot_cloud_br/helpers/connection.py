import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="usuario_do_banco",
    port = 3306,
    password="senha_do_banco",
    auth_plugin='mysql_native_password',
    database='iot_cloud_br'
)


def get_connection():
    return db
