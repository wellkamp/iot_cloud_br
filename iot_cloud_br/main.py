import paho.mqtt.client as mqtt
import json
from telepot.loop import MessageLoop
from dao.sensores_dao import SensorsDao
from dao.usuarios_dao import UsuarioDao
from models.sensor import Sensor
from models.bot_telegram import TelegramBot
from helpers import connection
import time


def main():
    sensor_dao = SensorsDao(connection.db)
    user_dao = UsuarioDao(connection.db)

    def on_connect(client, userdata, flags, rc):
        # print("Connected with result code {0}".format(str(rc)))
        # topico_novo = novo_bot.topico
        # print(topico_novo)
        client.subscribe('iot_cloud_br/8650110')

    def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
        data_in = json.loads(msg.payload.decode('utf-8'))
        try:
            user_fk = user_dao.search_id_user(data_in['usuario'])
            novo_sensor = Sensor(data_in['nome_sensor'], data_in['temperatura'], data_in['umidade'],
                                 time.strftime('%Y-%m-%d'),
                                 time.strftime('%H:%M:%S'), user_fk)
            sensor_dao.insert_user_sensor(novo_sensor.sensor_name, novo_sensor.temperature, novo_sensor.humidity,
                                          novo_sensor.date_now, novo_sensor.time_now, novo_sensor.fk_user)
            novo_bot.send_response('Valor inserido!')
        except Exception as e:
            print(e)

    # BOT
    novo_bot = TelegramBot('1310318843:AAF8BnH-YqmHhNxlsg4Afy-_egm-DMyNMK8')
    MessageLoop(novo_bot.bot, novo_bot.handle).run_as_thread()

    # MQTT
    print('Rodando...')
    client = mqtt.Client("trabalho_se")
    # client.loop_start()
    client.connect('test.mosquitto.org', 1883)
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message
    client.loop_forever(1.0)  # Start networking daemon


if __name__ == '__main__':
    main()
