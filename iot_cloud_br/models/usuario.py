class User():
    def __init__(self, login, pwd):
        self._user = login
        self._pwd = pwd

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, pwd):
        self._pwd = pwd