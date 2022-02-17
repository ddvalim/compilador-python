class TabelaSimbolos:
    def __init__(self):
        self.__tabela = []

    ## entrada deve ser um array de tres atributos
    ## [TIPO_TOKEN, VALOR, LINHA]
    def adicionaEntrada(self, entrada):
        self.__tabela.append(entrada)
    
    def recuperaTabela(self):
        return self.__tabela