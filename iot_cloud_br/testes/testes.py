class Pessoa():
    def __init__(self, nome, idade):
        self._nome = nome
        self._idade = idade

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, idade):
        self._idade = idade


def print_nome_idade(Pessoa):
    print(Pessoa.nome)
    print(Pessoa.idade)


pessoa = Pessoa('joão', 12)
print_nome_idade(pessoa)