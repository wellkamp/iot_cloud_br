SQL_INSERT_SENSOR = 'INSERT into user_sensors (sensor_name, temperature, humidity, date_column, hour_column, fk_users) ' \
                    'values (%s, %s, %s, %s, %s, %s)'


class SensoresDao():
    def __init__(self, db):
        self.db = db

    def select_temperatura(self, fk_user, sensor_name):
        cursor = self.db.cursor()
        cursor.execute('SELECT temperature FROM user_sensors WHERE fk_users = '+str(fk_user)+' and sensor_name = "'+sensor_name+'" ORDER BY id DESC limit 1')
        resultado = cursor.fetchall()
        for resultados in resultado:
            return resultados[0]

    def select_umidade(self, fk_user, sensor_name):
        cursor = self.db.cursor()
        cursor.execute('SELECT humidity FROM user_sensors WHERE fk_users = '+str(fk_user)+' and sensor_name = "'+sensor_name+'" ORDER BY id DESC limit 1')
        resultado = cursor.fetchall()
        for resultados in resultado:
            return resultados[0]

    def select_date(self, fk_user, sensor_name):
        cursor = self.db.cursor()
        cursor.execute('SELECT date_column FROM user_sensors WHERE fk_users = '+str(fk_user)+' and sensor_name = "'+sensor_name+'" ORDER BY id DESC limit 1')
        resultado = cursor.fetchall()
        for resultados in resultado:
            return resultados[0]

    def select_hour(self, fk_user, sensor_name):
        cursor = self.db.cursor()
        cursor.execute('SELECT hour_column FROM user_sensors WHERE fk_users = '+str(fk_user)+' and sensor_name = "'+sensor_name+'" ORDER BY id DESC limit 1')
        resultado = cursor.fetchall()
        for resultados in resultado:
            return resultados[0]

    def insert_user_sensor(self, sensor_name, temperature, humidity, date_column, hour_column, fk_user):
        cursor = self.db.cursor()
        cursor.execute(SQL_INSERT_SENSOR, (sensor_name, temperature, humidity, date_column, hour_column, fk_user))
        self.db.commit()