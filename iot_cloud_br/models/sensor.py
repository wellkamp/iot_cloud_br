class Sensor():
    def __init__(self, sensor_name, temperature, humidity, date_now, time_now, fk_user):
        self._sensor_name = sensor_name
        self._temperature = temperature
        self._humidity = humidity
        self._date_now = date_now
        self._time_now = time_now
        self._fk_user = fk_user

    @property
    def sensor_name(self):
        return self._sensor_name

    @sensor_name.setter
    def sensor_name(self, sensor_name):
        self._sensor_name = sensor_name

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temperature):
        self._temperature = temperature

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, humidity):
        self._humidity = humidity

    @property
    def date_now(self):
        return self._date_now

    @date_now.setter
    def date_now(self, date_now):
        self._date_now = date_now

    @property
    def time_now(self):
        return self._time_now

    @time_now.setter
    def time_now(self, time_now):
        self._time_now = time_now

    @property
    def fk_user(self):
        return self._fk_user

    @fk_user.setter
    def fk_user(self, user_fk):
        self._fk_user = user_fk

    def __str__(self):
        str = f'{self.sensor_name} + {self.temperature} + {self.humidity} + {self.date_now} + {self.time_now} + {self.fk_user}'
        return str