class TabelaSimbolos:
    def __init__(self):
        self.__tabela = []

    ## entrada deve ser um array de tres atributos
    ## [TIPO_TOKEN, VALOR, LINHA]
    def adiciona_entrada(self, entrada):
        self.__tabela.append(entrada)
    
    def recupera_tabela(self):
        return self.__tabela