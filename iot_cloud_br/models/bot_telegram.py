import telepot
from dao.usuarios_dao import UsuarioDao
from models.usuario import User
from dao.sensores_dao import SensorsDao
from helpers import connection
from telepot.loop import MessageLoop
import matplotlib.pyplot as plt


class TelegramBot():
    def __init__(self, TOKEN):
        self._topico = 'iot_cloud_br/'
        self._bot = telepot.Bot(TOKEN)
        self._fk_user = ''
        self._chat_id = ''

    @property
    def bot(self):
        return self._bot

    @property
    def topico(self):
        return self._topico

    @topico.setter
    def topico(self, valor):
        self._topico = valor

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, chat_id):
        self._chat_id = chat_id

    @property
    def fk_user(self):
        return self._fk_user

    @fk_user.setter
    def fk_user(self, fk_user):
        self._fk_user = fk_user

    def send_response(self, text):
        return self.bot.sendMessage(self.chat_id, text)

    # Função que manda uma mensagem de Bem Vindo quando o usuario está identificado
    def welcome_message(self):
        self.bot.sendMessage(self.chat_id,
                             'Bem vindo! '
                             '\nDigite /topic nome_topico para criar um topico novo'
                             '\nDigite /valores nome_do_sensor para ver os valores atuais do sensor.'
                             '\nDigite /graph_umidade nome_do_sensor para ver o gráfico de umidade.'
                             '\nDigite /graph_temperatura nome_do_sensor para ver o gráfico de temperatura.'
                             '\nDigite /media_temperatura nome_do_sensor para verificar a media dos ultimos 24 registros.'
                             '\nDigite /media_umidade nome_do_sensor para verificar a media dos ultimos 24 registros.'
                             '\nDigite /deletar nome_do_sensor para deletar o sensor dos registros.')

    # Função que manda uma mensagem quando o usuario não está identificado
    def unidentified_user(self):
        self.bot.sendMessage(self.chat_id,
                             'Notei que você não está identificado no nosso sistema. '
                             '\nUtilize /identify para identificarmos se você está no sistema ou '
                             'para crirar um novo usuario')

    # Função que cria um topico MQTT(ainda não funciona)
    def create_topic(self, msg):
        if msg != '':
            resp = 'iot_cloud_br/' + msg
            self.topico = resp
            self.bot.sendMessage(self.chat_id, 'Topico criado: ' + resp)
        else:
            self.bot.sendMessage(self.chat_id, 'Necessario criar um nome para o topico')

    # Função que recebe o último valor adicionado do sensor do usuario
    def get_last_values(self, sensor_name, user):
        try:
            user_fk = user_dao.search_id_user(user.user)
            temperature = sensor_dao.select_temperature(user_fk, sensor_name)
            humidity = sensor_dao.select_humidity(user_fk, sensor_name)
            date = sensor_dao.select_date(user_fk, sensor_name)
            hour = sensor_dao.select_hour(user_fk, sensor_name)
            if temperature is not None:
                temperature = f'Temperatura: {temperature} C'
                humidity = f'Umidade: {humidity} %'
                date = f'Data: {date: %d/%m/%Y}'
                hour = f'Hora: {hour}'
                self.bot.sendMessage(self.chat_id, temperature)
                self.bot.sendMessage(self.chat_id, humidity)
                self.bot.sendMessage(self.chat_id, date)
                self.bot.sendMessage(self.chat_id, hour)
            elif temperature != 'None':
                self.bot.sendMessage(self.chat_id, 'Não há registro de valores ainda')
        except Exception as e:
            print(e)
            self.bot.sendMessage(self.chat_id, 'Deve esperar um valor ser inserido!')

    # Função que plota o grafico de temperatura
    def plot_temperature(self, hour, temperature, id):
        plt.plot(hour, temperature)
        plt.xlabel('Hora do dia')
        plt.ylabel('Temperatura')
        plt.savefig('B:/iot_cloud_br_v2/local/graph_temperature' + str(id) + '_.png', format='png')
        image = open('B:/iot_cloud_br_v2/local/graph_temperature' + str(id) + '_.png', 'rb')
        self.bot.sendPhoto(self.chat_id, image)

    # Função que plota o grafico de umidade
    def plot_humidity(self, hour, humidity, id):
        plt.plot(hour, humidity)
        plt.xlabel('Hora do dia')
        plt.ylabel('Umidade')
        plt.savefig('B:/iot_cloud_br_v2/local/graph_humidity' + str(id) + '_.png', format='png')
        image = open('B:/iot_cloud_br_v2/local/graph_humidity' + str(id) + '_.png', 'rb')
        self.bot.sendPhoto(self.chat_id, image)

    # Função que demonstra o grafico de temperatura para o telegram
    def show_graph_temperature(self, sensor_name, user):
        try:
            user_fk = user_dao.search_id_user(user.user)
            temperature = sensor_dao.select_temperature_ten_rows(user_fk, sensor_name)
            hour = sensor_dao.select_hour_ten_rows(user_fk, sensor_name)
            if temperature is not None:
                self.plot_temperature(hour, temperature, user_fk)
            elif temperature != 'None':
                self.bot.sendMessage(self.chat_id, 'Não há registro de valores ainda!')
        except Exception as e:
            print(e)
            self.bot.sendMessage(self.chat_id, 'Deve esperar um valor ser inserido!')

    # Função que demonstra o grafico de umidade para o telegram
    def show_graph_humidity(self, sensor_name, user):
        try:
            user_fk = user_dao.search_id_user(user.user)
            humidity = sensor_dao.select_humidity_ten_rows(user_fk, sensor_name)
            hour = sensor_dao.select_hour_ten_rows(user_fk, sensor_name)
            if humidity is not None:
                self.plot_humidity(hour, humidity, user_fk)
            elif humidity != 'None':
                self.bot.sendMessage(self.chat_id, 'Não há registro de valores ainda!')
        except Exception as e:
            print(e)
            self.bot.sendMessage(self.chat_id, 'Deve esperar um valor ser inserido!')

    # Função que identifica/cria usuario
    def identify_user(self, user):
        try:
            user_dao.insert_user(user.user, user.pwd)
            self.bot.sendMessage(self.chat_id, 'Usuario criado!!')
            self.bot.sendMessage(self.chat_id, 'Seu usuario: ' + user.user)
            self.bot.sendMessage(self.chat_id, 'Sua senha: ' + user.pwd)
            self.bot.sendMessage(self.chat_id, 'Digite /start para começar novamente!')
        except Exception as e:
            self.bot.sendMessage(self.chat_id, 'Usuario identificado!')
            self.bot.sendMessage(self.chat_id, 'Seu usuario: ' + user.user)
            self.bot.sendMessage(self.chat_id, 'Sua senha: ' + user.pwd)
            self.bot.sendMessage(self.chat_id, 'Digite /start para começar novamente!')

    # Função media temperatura
    def avg_temperature(self, sensor_name, user):
        try:
            user_fk = user_dao.search_id_user(user.user)
            temperature = sensor_dao.select_temperature_average(user_fk, sensor_name)
            if temperature is not None:
                self.bot.sendMessage(self.chat_id, temperature)
            elif temperature != 'None':
                self.bot.sendMessage(self.chat_id, 'Não há registro de valores ainda')
        except Exception as e:
            print(e)
            self.bot.sendMessage(self.chat_id, 'Deve esperar um valor ser inserido!')

    def avg_humidity(self, sensor_name, user):
        try:
            user_fk = user_dao.search_id_user(user.user)
            humidity = sensor_dao.select_humidity_average(user_fk, sensor_name)
            if humidity is not None:
                self.bot.sendMessage(self.chat_id, humidity)
            elif humidity != 'None':
                self.bot.sendMessage(self.chat_id, 'Não há registro de valores ainda')
        except Exception as e:
            print(e)
            self.bot.sendMessage(self.chat_id, 'Deve esperar um valor ser inserido!')

    # Função que deleta o sensor do usuario
    def delete_sensor(self, sensor_name, user):
        try:
            if sensor_name != '':
                user_fk = user_dao.search_id_user(user.user)
                sensor_dao.delete_sensor(sensor_name, user_fk)
            else:
                self.bot.sendMessage(self.chat_id, 'Digite o nome do sensor')
        except Exception as e:
            print(e)

    # Função principal
    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.chat_id = chat_id
        if content_type == 'text':
            is_user = user_dao.select_users(new_user.user, new_user.pwd)
            if msg['text'] == '/start':
                if is_user is True:
                    self.welcome_message()
                elif is_user is False:
                    self.unidentified_user()
            elif '/topic' in msg['text'] and is_user is True:
                nome_topico = msg['text'][7:]
                self.create_topic(nome_topico)
            elif '/valores' in msg['text'] and is_user is True:
                # self.bot.sendMessage(chat_id, user_dao.select_sensors(self.get_nome_tabela()))
                sensor_name = msg['text'][9:]
                self.get_last_values(sensor_name, new_user)
            elif '/graph_umidade' in msg['text'] and is_user is True:
                sensor_name = msg['text'][15:]
                self.show_graph_humidity(sensor_name, new_user)
            elif '/graph_temperatura' in msg['text'] and is_user is True:
                sensor_name = msg['text'][19:]
                self.show_graph_temperature(sensor_name, new_user)
            elif '/media_umidade' in msg['text'] and is_user is True:
                sensor_name = msg['text'][15:]
                self.avg_humidity(sensor_name, new_user)
            elif '/media_temperatura' in msg['text'] and is_user is True:
                sensor_name = msg['text'][19:]
                self.avg_temperature(sensor_name, new_user)
            elif '/delete' in msg['text'] and is_user is True:
                sensor_name = msg['text'][8:]
                print(sensor_name)
                self.delete_sensor(sensor_name, new_user)
            if msg['text'] == '/identify':
                login = str(msg['from']['first_name'] + '_' + str(msg['from']['id'])).lower()
                senha = str(msg['from']['id'])[4:]
                new_user.user = login
                new_user.pwd = senha
                self.identify_user(new_user)


user_dao = UsuarioDao(connection.db)
sensor_dao = SensorsDao(connection.db)
new_user = User('', '')
