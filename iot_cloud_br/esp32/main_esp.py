from umqtt.simple import MQTTClient
import time
import ujson as json
import dht
from machine import Pin
from time import sleep
import conexao as cn


def main():
    def valores_dht11():
        sensor.measure()
        valor_temperatura = sensor.temperature()
        valor_umidade = sensor.humidity()
        valores = {
            "temperatura": valor_temperatura,
            "umidade": valor_umidade,
            "nome_sensor": "nome_do_sensor",
            "usuario": "usuario_fornecido_pelo_bot"
        }
        file_json = json.dumps(valores)
        return file_json

    cn.connect('ssid', 'senha')
    sensor = dht.DHT11(Pin(12))
    c_mqtt = MQTTClient('nome_do_cliente', 'BROKER', port=1883)
    c_mqtt.connect()

    while True:
        try:
            c_mqtt.publish(topic='nome_do_topico', msg=valores_dht11())
            print("mensagem enviada com sucesso")
        except Exception as e:
            print(e)
        time.sleep(1800)


if __name__ == '__main__':
    main()



