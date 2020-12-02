SQL_SELECT_USERS = 'SELECT login, senha FROM USUARIOS'
SQL_INSERT_USUARIO = 'INSERT into usuarios(login, senha) values(%s, %s)'
SQL_SELECT = 'SELET * FROM '


class UsuarioDao():
    def __init__(self, db):
        self.db = db

    def insert_usuario(self, valor1, valor2):
        cursor = self.db.cursor()
        cursor.execute(SQL_INSERT_USUARIO, (valor1, valor2))
        self.db.commit()

    def select_usuarios(self):
        cursor = self.db.cursor()
        cursor.execute(SQL_SELECT_USERS)
        resultado = cursor.fetchall()
        return dict(resultado)

    def select_users(self, usuario, senha):
        cursor = self.db.cursor()
        cursor.execute(SQL_SELECT_USERS)
        resultado = cursor.fetchall()
        dict(resultado)
        for chave, valor in self.select_usuarios().items():
            if chave == usuario and valor == senha:
                return True
        return False

    def busca_id_usuario(self, usuario):
        cursor = self.db.cursor()
        cursor.execute("SELECT id_users FROM usuarios WHERE login = '" + usuario + "'")
        resultado = cursor.fetchall()
        for resultados in resultado:
            return resultados[0]