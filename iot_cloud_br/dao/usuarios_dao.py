SQL_SELECT_USERS = 'SELECT login, senha FROM USUARIOS'
SQL_INSERT_USER = 'INSERT into usuarios(login, senha) values(%s, %s)'
SQL_SELECT = 'SELET * FROM '


class UsuarioDao():
    def __init__(self, db):
        self.db = db

    def insert_user(self, login, pwd):
        cursor = self.db.cursor()
        cursor.execute(SQL_INSERT_USER, (login, pwd))
        self.db.commit()

    def select_users(self, user, pwd):
        cursor = self.db.cursor()
        cursor.execute(SQL_SELECT_USERS)
        result = cursor.fetchall()
        result = dict(result)
        for key, value in result.items():
            if key == user and value == pwd:
                return True
        return False

    def search_id_user(self, user):
        cursor = self.db.cursor()
        cursor.execute("SELECT id_users FROM usuarios WHERE login = '" + user + "'")
        result = cursor.fetchall()
        for results in result:
            return results[0]