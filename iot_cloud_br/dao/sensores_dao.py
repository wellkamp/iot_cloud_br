SQL_INSERT_SENSOR = 'INSERT into user_sensors ' \
                    '(sensor_name, temperature, humidity, date_column, hour_column, fk_users) ' \
                    'values (%s, %s, %s, %s, %s, %s)'


class SensorsDao():
    def __init__(self, db):
        self.db = db

    def select_temperature(self, fk_user, sensor_name):
        cursor = self.db.cursor()
        cursor.execute('SELECT temperature FROM user_sensors WHERE fk_users = '
                       ''+str(fk_user)+' and sensor_name = "'+sensor_name+'" ORDER BY id DESC limit 1')
        result = cursor.fetchall()
        for results in result:
            return results[0]

    def select_humidity(self, fk_user, sensor_name):
        cursor = self.db.cursor()
        cursor.execute('SELECT humidity FROM user_sensors WHERE fk_users = '
                       ''+str(fk_user)+' and sensor_name = "'+sensor_name+'" ORDER BY id DESC limit 1')
        result = cursor.fetchall()
        for results in result:
            return results[0]

    def select_date(self, fk_user, sensor_name):
        cursor = self.db.cursor()
        cursor.execute('SELECT date_column FROM user_sensors WHERE fk_users = '
                       ''+str(fk_user)+' and sensor_name = "'+sensor_name+'" ORDER BY id DESC limit 1')
        result = cursor.fetchall()
        for results in result:
            return results[0]

    def select_hour(self, fk_user, sensor_name):
        cursor = self.db.cursor()
        cursor.execute('SELECT hour_column FROM user_sensors WHERE fk_users = '
                       ''+str(fk_user)+' and sensor_name = "'+sensor_name+'" ORDER BY id DESC limit 1')
        result = cursor.fetchall()
        for results in result:
            return results[0]

    def insert_user_sensor(self, sensor_name, temperature, humidity, date_column, hour_column, fk_user):
        cursor = self.db.cursor()
        cursor.execute(SQL_INSERT_SENSOR, (sensor_name, temperature, humidity, date_column, hour_column, fk_user))
        self.db.commit()

    def select_temperature_eight_rows(self, fk_user, sensor_name):
        temperature = []
        cursor = self.db.cursor()
        cursor.execute('SELECT temperature FROM user_sensors WHERE fk_users = ' + str(
            fk_user) + ' and sensor_name = "' + sensor_name + '" ORDER BY id DESC LIMIT 8')
        result = cursor.fetchall()
        for results in result:
            temperature.append(int(results[0]))
        return temperature[::-1]

    def select_hour_eight_rows(self, fk_user, sensor_name):
        hour = []
        cursor = self.db.cursor()
        cursor.execute('SELECT hour_column FROM user_sensors WHERE fk_users = ' + str(
            fk_user) + ' and sensor_name = "' + sensor_name + '" ORDER BY id DESC LIMIT 8')
        result = cursor.fetchall()
        for results in result:
            hour.append(results[0])
        return hour[::-1]

    def select_humidity_eight_rows(self, fk_user, sensor_name):
        humidity = []
        cursor = self.db.cursor()
        cursor.execute('SELECT humidity FROM user_sensors WHERE fk_users = ' + str(
            fk_user) + ' and sensor_name = "' + sensor_name + '" ORDER BY id DESC LIMIT 8')
        result = cursor.fetchall()
        for results in result:
            humidity.append(int(results[0]))
        return humidity[::-1]

    def delete_sensor(self, sensor_name, fk_user):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM user_sensors WHERE sensor_name = '
                       '"' + sensor_name + '" and fk_users = '+str(fk_user)+'')
        self.db.commit()

    def select_humidity_average(self, fk_user, sensor_name):
        humidity = []
        cursor = self.db.cursor()
        cursor.execute('SELECT humidity FROM user_sensors WHERE fk_users = ' + str(
            fk_user) + ' and sensor_name = "' + sensor_name + '" ORDER BY date_column, hour_column DESC LIMIT 24')
        result = cursor.fetchall()
        for results in result:
            humidity.append(int(results[0]))
        return f'{(sum(humidity) / 24):.2f} %'

    def select_temperature_average(self, fk_user, sensor_name):
        temperature = []
        cursor = self.db.cursor()
        cursor.execute('SELECT temperature FROM user_sensors WHERE fk_users = ' + str(
            fk_user) + ' and sensor_name = "' + sensor_name + '" ORDER BY date_column, hour_column DESC LIMIT 24')
        result = cursor.fetchall()
        for results in result:
            temperature.append(int(results[0]))
        return f'{(sum(temperature) / 24):.1f} ºC'