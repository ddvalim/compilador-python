#### ANALISADOR LEXICO ####

# Palavras Reservadas
#   def
#   int
#   float
#   string
#   break
#   print
#   read
#   return
#   if
#   else
#   for
#   new
#   int_constant
#   float_constant
#   string_constant
#   null

# Operadores
#   =
#   <
#   >
#   <=
#   >=
#   ==
#   !=
#   +
#   -
#   *
#   /
#   %

# Delimitadores
#   (
#   )-
#   {
#   }
#   ,
#   ;
#   [
#   ]

# Outros
# ident - Representa um identificador
# Exemplo:
# int C = 4;
# C eh um token do tipo ident
# Na tabela de simbolos, teremos:
# ['IDENT', 'C', 48]

# Metodo analisa retorna LISTA DE TOKENS e TABELA DE SIMBOLOS

# Bibliotecas para entrada e saida de arquivos
from re import S
import sys
import os.path
import string
from tabela_simbolos import TabelaSimbolos


class AnalisadorLexico():
    def __init__(self):
        self.__entrada = "entrada.txt"
        self.__lista_tokens = []
        self.__tabela_simbolos = TabelaSimbolos()

    def muda_entrada(self, novaEntrada):
        self.__entrada = novaEntrada

    def recupera_entrada(self):
        return self.__entrada

    def adiciona_token(self, token):
        self.__lista_tokens.append(token)

    def recupera_lista_tokens(self):
        return self.__lista_tokens

    def eh_delimitador(self, caractere):
        delimitadores = [
            {'nome': 'RPAREN', 'token': '('},
            {'nome': 'LPAREN', 'token': ')'},
            {'nome': 'LCHAVE', 'token': '{'},
            {'nome': 'RCHAVE', 'token': '}'},
            {'nome': 'VIRGULA', 'token': ','},
            {'nome': 'PONTOVIRGULA', 'token': ';'},
            {'nome': 'LCOL', 'token': '['},
            {'nome': 'RCOL', 'token': ']'}
        ]

        eh_delimitador = list(
            filter(lambda item: item['token'] == caractere, delimitadores))

        if len(eh_delimitador) == 1:
            return eh_delimitador[0]
        else:
            return False

    def eh_operador(self, caractere):
        operadores = [
            {'nome': 'ATRIBUICAO', 'token': '='},
            {'nome': 'MENOR', 'token': '<'},
            {'nome': 'MAIOR', 'token': '>'},
            {'nome': 'MENORIGUAL', 'token': '<='},
            {'nome': 'MAIORIGUAL', 'token': '>='},
            {'nome': 'IGUAL', 'token': '=='},
            {'nome': 'DIFERENTE', 'token': '!='},
            {'nome': 'MAIS', 'token': '+'},
            {'nome': 'MENOS', 'token': '-'},
            {'nome': 'VEZES', 'token': '*'},
            {'nome': 'BARRA', 'token': '/'},
            {'nome': 'PORCENTAGEM', 'token': '%'},
        ]

        eh_operador = list(
            filter(lambda item: item['token'] == caractere, operadores))

        if len(eh_operador) == 1:
            return eh_operador[0]
        else:
            return False

    def eh_digito(self, caractere):
        digitos = [
            {'nome': 'ZERO', 'token': '0'},
            {'nome': 'UM', 'token': '1'},
            {'nome': 'DOIS', 'token': '2'},
            {'nome': 'TRES', 'token': '3'},
            {'nome': 'QUATRO', 'token': '4'},
            {'nome': 'CINCO', 'token': '5'},
            {'nome': 'SEIS', 'token': '6'},
            {'nome': 'SETE', 'token': '7'},
            {'nome': 'OITO', 'token': '8'},
            {'nome': 'NOVE', 'token': '9'}
        ]

        eh_digito = list(
            filter(lambda item: item['token'] == caractere, digitos))

        if len(eh_digito) == 1:
            return eh_digito[0]
        else:
            return False

    def eh_reservada(self, palavra):
        reservadas = [
            {'nome': 'DEFINE_FUNCAO', 'token': 'def'},
            {'nome': 'INTEIRO', 'token': 'int'},
            {'nome': 'FLUTUANTE', 'token': 'float'},
            {'nome': 'CADEIA', 'token': 'string'},
            {'nome': 'INTERROMPE', 'token': 'break'},
            {'nome': 'IMPRIME', 'token': 'print'},
            {'nome': 'LE', 'token': 'read'},
            {'nome': 'RETORNA', 'token': 'return'},
            {'nome': 'SE', 'token': 'if'},
            {'nome': 'SENAO', 'token': 'else'},
            {'nome': 'PARA', 'token': 'for'},
            {'nome': 'NOVO', 'token': 'new'},
            {'nome': 'INT_CONSTANT', 'token': 'int_constant'},
            {'nome': 'FLOAT_CONSTANT', 'token': 'float_constant'},
            {'nome': 'STRING_CONSTANT', 'token': 'string_constant'},
            {'nome': 'VAZIO', 'token': 'null'}
        ]

        eh_reservada = list(
            filter(lambda item: item['token'] == palavra, reservadas))

        if len(eh_reservada) == 1:
            return eh_reservada[0]
        else:
            return False

    def eh_letra(self, caractere):
        letras = string.ascii_letters

        if caractere in letras:
            return caractere
        else:
            return False

    def analisador(self):
        if not os.path.exists(self.__entrada):
            raise Exception(
                'Não foi possível encontrar um arquivo de entrada válido!')

        arquivo = open(self.__entrada, 'r')

        numero_linha = 1
        linha = arquivo.readline()

        while linha:
            indice_caractere = 0
            tamanho_linha = len(linha)

            while indice_caractere < tamanho_linha:
                caractere_atual = linha[indice_caractere]
                prox_caractere = None

                if ((indice_caractere + 1) < tamanho_linha):
                    prox_caractere = linha[indice_caractere]

                if (self.eh_delimitador(caractere_atual)):
                    self.adiciona_token(caractere_atual)

                    entrada = self.eh_delimitador(caractere_atual)

                    self.__tabela_simbolos.adiciona_entrada(
                        [entrada['nome'], entrada['token'], numero_linha])

                if (prox_caractere != None and self.eh_operador(caractere_atual)):
                    self.adiciona_token(caractere_atual)

                    entrada = self.eh_operador(caractere_atual)

                    self.__tabela_simbolos.adiciona_entrada(
                        [entrada['nome'], entrada['token'], numero_linha])

                # Se um caractere for ', ele precisa ser fechado com '
                if (caractere_atual == string.punctuation[6]):
                    if (linha[i+1] == '\n') or (not (string.punctuation[6] in linha[i+1:])):
                        raise Exception(
                            f'Erro léxico! Caractere não fechado - Linha: {numero_linha}')
                    elif self.eh_simbolo(linha[i+1]) and linha[i+1] != string.punctuation[6] and linha[i+2] == string.punctuation[6]:
                        self.adiciona_token(caractere_atual)

                        entrada = self.eh_operador(caractere_atual)

                        self.__tabela_simbolos.adiciona_entrada(
                            [entrada['nome'], entrada['token'], numero_linha])

                        i += 2
                    else:
                        raise Exception(
                            f'Erro léxico! - Tamanho ou simbolo de caractere inválido - Linha: {numero_linha}')
