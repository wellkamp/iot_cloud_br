import telepot

from dao.usuarios_dao import UsuarioDao
from models.usuario import User
from dao.sensores_dao import SensoresDao
from helpers import connection


user_dao = UsuarioDao(connection.db)
sensor_dao = SensoresDao(connection.db)
user = User()


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
                             '\nDigite /valores nome_do_sensor para ver os valores atuais do sensor')

    # Função que manda uma mensagem quando o usiario não está identificado
    def unidentified_user(self):
        self.bot.sendMessage(self.chat_id,
                             'Notei que você não está identificado no nosso sistema. '
                             '\nUtilize /identify para identificarmos se você está no sistema ou '
                             'para crirar um novo usuario')

    # Função que cria um topico MQTT(ainda não funcional)
    def create_topic(self, msg):
        if msg != '':
            resp = 'iot_cloud_br/' + msg
            self.topico = resp
            self.bot.sendMessage(self.chat_id, 'Topico criado: ' + resp)
        else:
            self.bot.sendMessage(self.chat_id, 'Necessario criar um nome para o topico')

    # Função que recebe o último valor adicionado do sensor do usuario
    def get_last_values(self, sensor_name):
        try:
            user_fk = user_dao.busca_id_usuario(user.user)
            temperatura = sensor_dao.select_temperatura(user_fk, sensor_name)
            umidade = sensor_dao.select_umidade(user_fk, sensor_name)
            date = sensor_dao.select_date(user_fk, sensor_name)
            hour = sensor_dao.select_hour(user_fk, sensor_name)
            if temperatura is not None:
                temperatura = f'Temperatura: {temperatura} C'
                umidade = f'Umidade: {umidade} %'
                date = f'Data: {date: %d/%m/%Y}'
                hour = f'Hora: {hour}'
                self.bot.sendMessage(self.chat_id, temperatura)
                self.bot.sendMessage(self.chat_id, umidade)
                self.bot.sendMessage(self.chat_id, date)
                self.bot.sendMessage(self.chat_id, hour)
            elif temperatura != 'None':
                self.bot.sendMessage(self.chat_id, 'Verificar o nome da tabela')
        except Exception as e:
            print(e)
            self.bot.sendMessage(self.chat_id, 'Deve esperar um valor ser inserido!')

    # Função que identifica/cria usuario
    def identify_user(self, login, senha):
        user.user = login
        user.pwd = senha
        try:
            user_dao.insert_usuario(login, senha)
            self.bot.sendMessage(self.chat_id, 'Usuario criado!!')
            self.bot.sendMessage(self.chat_id, 'Seu usuario: ' + user.user)
            self.bot.sendMessage(self.chat_id, 'Sua senha: ' + user.pwd)
            self.bot.sendMessage(self.chat_id, 'Digite /start para começar novamente!')
        except Exception as e:
            self.bot.sendMessage(self.chat_id, 'Usuario identificado!')
            self.bot.sendMessage(self.chat_id, 'Seu usuario: ' + user.user)
            self.bot.sendMessage(self.chat_id, 'Sua senha: ' + user.pwd)
            self.bot.sendMessage(self.chat_id, 'Digite /start para começar novamente!')

    # Função principal
    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.chat_id = chat_id
        is_user = user_dao.select_users(user.user, user.pwd)
        if content_type == 'text':
            if msg['text'] == '/start':
                if is_user is True:
                    self.welcome_message()
                elif is_user is False:
                    self.unidentified_user()
            elif '/topic' in msg['text'] and is_user is True:
                nome_topico = msg['text'][7:]
                print(nome_topico)
                self.create_topic(nome_topico)
            elif '/valores' in msg['text'] and is_user is True:
                # self.bot.sendMessage(chat_id, user_dao.select_sensors(self.get_nome_tabela()))
                sensor_name = msg['text'][9:]
                self.get_last_values(sensor_name)
            if msg['text'] == '/identify':
                login = str(msg['from']['first_name'] + '_' + str(msg['from']['id'])).lower()
                senha = str(msg['from']['id'])[4:]
                self.identify_user(login, senha)
