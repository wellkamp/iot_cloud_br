import mysql.connector
import matplotlib.pyplot as plt

SQL_INSERT_SENSOR = 'INSERT into user_sensors (sensor_name, temperature, humidity, date_column, hour_column, fk_users) ' \
                    'values (%s, %s, %s, %s, %s, %s)'

db = mysql.connector.connect(
    host="localhost",
    user="wellkamp",
    port = 3306,
    password="wellk4mp",
    auth_plugin='mysql_native_password',
    database='iot_cloud_br'
)


SQL = 'SELECT login, senha FROM USUARIOS'
SQL_INSERT= 'INSERT into usuarios(login, senha) values(%s, %s)'


def insert_usuario(valor1, valor2):
    cursor = db.cursor()
    cursor.execute(SQL_INSERT, (valor1, valor2))
    db.commit()


def select_usuarios():
    cursor = db.cursor()
    cursor.execute(SQL)
    resultado = cursor.fetchall()
    return dict(resultado)


def select_usuarios_teste():
    cursor = db.cursor()
    cursor.execute(SQL)
    resultado = cursor.fetchall()
    dict(resultado)
    for chave, valor in select_usuarios().items():
        print(chave + ' == ' + valor)
        if chave == 'alsdasdo' and valor == 'alo':
            return True
    return False


def select_sensors(tabela):
    cursor = db.cursor()
    cursor.execute('SELECT temperatura, umidade FROM ' + tabela + ' ORDER BY id DESC limit 1')
    resultado = cursor.fetchall()
    for resultados in resultado:
        str = 'Temperatura: ' + resultados[0]
        return str


def busca_id_usuario(usuario):
    cursor = db.cursor()
    cursor.execute("SELECT id_users FROM usuarios WHERE login = '"+usuario+"'")
    resultado = cursor.fetchall()
    for resultados in resultado:
        return resultados[0]

def select_temperatura(tabela):
    cursor = db.cursor()
    cursor.execute('SELECT temperatura FROM ' + tabela + ' ORDER BY id DESC limit 1')
    resultado = cursor.fetchall()
    for resultados in resultado:
        str = 'Temperatura: ' + resultados[0] + ' º'
        return str


def select_umidade(tabela):
    cursor = db.cursor()
    cursor.execute('SELECT umidade FROM ' + tabela + ' ORDER BY id DESC limit 1')
    resultado = cursor.fetchall()
    for resultados in resultado:
        return resultados[0]


def insert_sensor_table(nome, field_1, field_2, data, hora, fk_user):
    cursor = db.cursor()
    cursor.execute(SQL_INSERT_SENSOR, (nome, field_1, field_2, data, hora, fk_user))
    db.commit()


def select_temperatura_teste(fk_user, sensor_name):
    lista = []
    cursor = db.cursor()
    cursor.execute('SELECT temperature FROM user_sensors WHERE fk_users = ' + str(
        fk_user) + ' and sensor_name = "' + sensor_name + '"')
    resultado = cursor.fetchall()
    for resultados in resultado:
        if resultado.count(1):
            return print(resultados)


def select_temperature_ten_rows(fk_user, sensor_name):
    temperature = []
    cursor = db.cursor()
    cursor.execute('SELECT temperature FROM user_sensors WHERE fk_users = ' + str(
        fk_user) + ' and sensor_name = "' + sensor_name + '" ORDER BY date_column, hour_column DESC LIMIT 10')
    result = cursor.fetchall()
    for results in result:
        temperature.append(results[0])
    return temperature


def select_hour_ten_rows(fk_user, sensor_name):
    hour = []
    cursor = db.cursor()
    cursor.execute('SELECT hour_column FROM user_sensors WHERE fk_users = ' + str(
        fk_user) + ' and sensor_name = "' + sensor_name + '" ORDER BY date_column, hour_column DESC LIMIT 7')
    result = cursor.fetchall()
    for results in result:
        hour.append(results[0])
    return hour


def select_humidity_ten_rows(fk_user, sensor_name):
    humidity = []
    cursor = db.cursor()
    cursor.execute('SELECT humidity FROM user_sensors WHERE fk_users = ' + str(
        fk_user) + ' and sensor_name = "' + sensor_name + '" ORDER BY date_column, hour_column DESC LIMIT 7')
    result = cursor.fetchall()
    for results in result:
        humidity.append(int(results[0]))
    return humidity


def select_humidity_average(fk_user, sensor_name):
    humidity = []
    cursor = db.cursor()
    cursor.execute('SELECT humidity FROM user_sensors WHERE fk_users = ' + str(
        fk_user) + ' and sensor_name = "' + sensor_name + '" ORDER BY date_column, hour_column DESC LIMIT 24')
    result = cursor.fetchall()
    for results in result:
        humidity.append(int(results[0]))
    return f'{(sum(humidity) / 24):.2f} %'


def select_temperature_average(fk_user, sensor_name):
    temperature = []
    cursor = db.cursor()
    cursor.execute('SELECT temperature FROM user_sensors WHERE fk_users = ' + str(
        fk_user) + ' and sensor_name = "' + sensor_name + '" ORDER BY date_column, hour_column DESC LIMIT 24')
    result = cursor.fetchall()
    for results in result:
        temperature.append(int(results[0]))
    return f'{(sum(temperature) / 24):.1f} ºC'


'''
data_atual = dt.datetime.utcnow()
# str = data_atual.strftime('%Y-%m-%d %H:%M:%S')
print(str)
data = time.strftime('%Y-%m-%d')
hora = time.strftime('%H:%M:%S')
print(data)
print(hora)
insert_sensor_table('teste', 'teste', 'teste', data, hora, 5)
print(select_temperatura_teste(5, 'teste'))
'''
#SELECT id_users FROM usuarios WHERE login = 'wellkamp';
#print(select_usuarios_teste())
#print(select_sensors('dht11'))
#print(select_temperatura('dht11'))
#print(select_umidade('dht11'))
# print(busca_id_usuario('wellington_1118650110'))
# umidade = select_humidity_average(5, 'dht11')
# temperature = select_temperature_average(5, 'dht11')



