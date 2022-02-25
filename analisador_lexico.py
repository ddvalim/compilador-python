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
import sys
import os.path
import string
from tabela_simbolos import TabelaSimbolos


class AnalisadorLexico:
    def __init__(self, arquivo):
        self.__entrada = arquivo
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
            {'nome': 'DPAREN', 'token': '('},
            {'nome': 'EPAREN', 'token': ')'},
            {'nome': 'ECHAVE', 'token': '{'},
            {'nome': 'ECHAVE', 'token': '}'},
            {'nome': 'VIRGULA', 'token': ','},
            {'nome': 'PONTOVIRGULA', 'token': ';'},
            {'nome': 'ECOL', 'token': '['},
            {'nome': 'DCOL', 'token': ']'}
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

    def eh_simbolo(self, caractere):
        simbolos = [
            {'nome': 'EXCLAMACAO', 'token': '!'},
            {'nome': 'ASPA_DUPLA', 'token': '"'},
            {'nome': 'CERQUILHA', 'token': '#'},
            {'nome': 'DOLAR', 'token': '$'},
            {'nome': 'PORCENTAGEM', 'token': '%'},
            {'nome': 'E_COMERCIAL', 'token': '&'},
            {'nome': 'ASPA_SIMPLES', 'token': "'"},
            {'nome': 'DPAREN', 'token': ')'},
            {'nome': 'E_PAREN', 'token': '('},
            {'nome': 'ASTERISCO', 'token': '*'},
            {'nome': 'MAIS', 'token': '+'},
            {'nome': 'VIRGULA', 'token': ','},
            {'nome': 'MENOS', 'token': '-'},
            {'nome': 'PONTO', 'token': '.'},
            {'nome': 'BARRA', 'token': '/'},
            {'nome': 'BARRA_INVERTIDA', 'token': r"'\'"},
            {'nome': 'ZERO', 'token': '0'},
            {'nome': 'UM', 'token': '1'},
            {'nome': 'DOIS', 'token': '2'},
            {'nome': 'TRES', 'token': '3'},
            {'nome': 'QUATRO', 'token': '4'},
            {'nome': 'CINCO', 'token': '5'},
            {'nome': 'SEIS', 'token': '6'},
            {'nome': 'SETE', 'token': '7'},
            {'nome': 'OITO', 'token': '8'},
            {'nome': 'NOVE', 'token': '9'},
            {'nome': 'VIRGULA', 'token': ','},
            {'nome': 'PONTOVIRGULA', 'token': ';'},
            {'nome': 'ATRIBUICAO', 'token': '='},
            {'nome': 'MENOR', 'token': '<'},
            {'nome': 'MAIOR', 'token': '>'},
            {'nome': 'INTERROGACAO', 'token': '?'},
            {'nome': 'ARROBA', 'token': '@'},
            {'nome': 'ECOL', 'token': '['},
            {'nome': 'DCOL', 'token': ']'},
            {'nome': 'CIRCUNFLEXO', 'token': '^'},
            {'nome': 'UNDERLINE', 'token': '_'},
            {'nome': 'GRAVE', 'token': '`'},
            {'nome': 'PIPE', 'token': '|'},
            {'nome': 'ECHAVE', 'token': '{'},
            {'nome': 'ECHAVE', 'token': '}'},
            {'nome': 'TIL', 'token': '~'},
            {'nome': 'A_MAIUSCULO', 'token': 'A'},
            {'nome': 'B_MAIUSCULO', 'token': 'B'},
            {'nome': 'C_MAIUSCULO', 'token': 'C'},
            {'nome': 'D_MAIUSCULO', 'token': 'D'},
            {'nome': 'E_MAIUSCULO', 'token': 'E'},
            {'nome': 'F_MAIUSCULO', 'token': 'F'},
            {'nome': 'G_MAIUSCULO', 'token': 'G'},
            {'nome': 'H_MAIUSCULO', 'token': 'H'},
            {'nome': 'J_MAIUSCULO', 'token': 'J'},
            {'nome': 'K_MAIUSCULO', 'token': 'K'},
            {'nome': 'L_MAIUSCULO', 'token': 'L'},
            {'nome': 'M_MAIUSCULO', 'token': 'M'},
            {'nome': 'N_MAIUSCULO', 'token': 'N'},
            {'nome': 'O_MAIUSCULO', 'token': 'O'},
            {'nome': 'P_MAIUSCULO', 'token': 'P'},
            {'nome': 'Q_MAIUSCULO', 'token': 'Q'},
            {'nome': 'R_MAIUSCULO', 'token': 'R'},
            {'nome': 'S_MAIUSCULO', 'token': 'S'},
            {'nome': 'T_MAIUSCULO', 'token': 'T'},
            {'nome': 'U_MAIUSCULO', 'token': 'U'},
            {'nome': 'V_MAIUSCULO', 'token': 'V'},
            {'nome': 'W_MAIUSCULO', 'token': 'W'},
            {'nome': 'X_MAIUSCULO', 'token': 'X'},
            {'nome': 'Y_MAIUSCULO', 'token': 'Y'},
            {'nome': 'Z_MAIUSCULO', 'token': 'Z'},
            {'nome': 'A_MINUSCULO', 'token': 'a'},
            {'nome': 'B_MINUSCULO', 'token': 'b'},
            {'nome': 'C_MINUSCULO', 'token': 'c'},
            {'nome': 'D_MINUSCULO', 'token': 'd'},
            {'nome': 'E_MINUSCULO', 'token': 'e'},
            {'nome': 'F_MINUSCULO', 'token': 'f'},
            {'nome': 'G_MINUSCULO', 'token': 'g'},
            {'nome': 'H_MINUSCULO', 'token': 'h'},
            {'nome': 'I_MINUSCULO', 'token': 'i'},
            {'nome': 'J_MINUSCULO', 'token': 'j'},
            {'nome': 'K_MINUSCULO', 'token': 'k'},
            {'nome': 'L_MINUSCULO', 'token': 'l'},
            {'nome': 'M_MINUSCULO', 'token': 'm'},
            {'nome': 'N_MINUSCULO', 'token': 'n'},
            {'nome': 'O_MINUSCULO', 'token': 'o'},
            {'nome': 'P_MINUSCULO', 'token': 'p'},
            {'nome': 'Q_MINUSCULO', 'token': 'q'},
            {'nome': 'R_MINUSCULO', 'token': 'r'},
            {'nome': 'S_MINUSCULO', 'token': 's'},
            {'nome': 'T_MINUSCULO', 'token': 't'},
            {'nome': 'U_MINUSCULO', 'token': 'u'},
            {'nome': 'V_MINUSCULO', 'token': 'v'},
            {'nome': 'W_MINUSCULO', 'token': 'w'},
            {'nome': 'X_MINUSCULO', 'token': 'x'},
            {'nome': 'Y_MINUSCULO', 'token': 'y'},
            {'nome': 'Z_MINUSCULO', 'token': 'z'}
        ]

        eh_simbolo = list(
            filter(lambda item: item['token'] == caractere, simbolos))

        if len(eh_simbolo) == 1:
            return eh_simbolo[0]
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

                # Verifica se o caractere_atual eh um delimitador
                if (self.eh_delimitador(caractere_atual)):
                    self.adiciona_token(caractere_atual)

                    entrada = self.eh_delimitador(caractere_atual)

                    self.__tabela_simbolos.adiciona_entrada(
                        [entrada['nome'], entrada['token'], numero_linha])

                    indice_caractere += 1
                    continue

                # Verifica se o caractere_atual+prox_caractere formam um operador
                elif (prox_caractere != None and self.eh_operador(caractere_atual+prox_caractere)):
                    self.adiciona_token(caractere_atual+prox_caractere)

                    entrada = self.eh_operador(caractere_atual+prox_caractere)

                    self.__tabela_simbolos.adiciona_entrada(
                        [entrada['nome'], entrada['token'], numero_linha])

                    indice_caractere += 1
                    continue

                # Verifica se o caractere_atual eh um operador
                elif self.eh_operador(caractere_atual):
                    self.adiciona_token(caractere_atual)

                    entrada = self.eh_operador(caractere_atual)

                    self.__tabela_simbolos.adiciona_entrada(
                        [entrada['nome'], entrada['token'], numero_linha])

                    indice_caractere += 1
                    continue

                # Se um caractere for ", ele precisa ser fechado com "
                elif (caractere_atual == string.punctuation[1]):
                    indice_caractere += 1
                    if (linha[indice_caractere:].find(string.punctuation[1]) == -1):
                        raise Exception(
                            f'Erro léxico! String não fechada - Linha: {numero_linha} - Coluna: {indice_caractere}')
                    else:
                        fim_string = indice_caractere + \
                            linha[indice_caractere:].find(
                                string.punctuation[1])

                        nova_string = linha[i:fim_string]

                        indice_caractere = fim_string

                        for caractere in nova_string:
                            if (not self.eh_simbolo(caractere)):
                                raise Exception(
                                    f'Erro léxico! - Tamanho ou simbolo de caractere inválido - Linha: {numero_linha} - Coluna: {indice_caractere}')
                        continue

                # Se o caractere for letra, eu preciso checar se ele eh IDENT
                elif (self.eh_letra(caractere_atual)):
                    string = caractere_atual
                    indice_caractere += 1

                    while indice_caractere < tamanho_linha:
                        c_atual = linha[indice_caractere]
                        c_prox = None

                        if (indice_caractere + 1 < tamanho_linha):
                            c_prox = linha[indice_caractere+1]

                        if (self.eh_letra(c_atual) or c_atual == '_' or self.eh_digito(c_atual)):
                            string += c_atual

                        elif (self.eh_delimitador(c_atual)):
                            indice_caractere -= 1
                            break

                        elif (c_prox is not None and self.eh_operador(c_atual+c_prox)) or self.eh_operador(c_atual):
                            i -= 1
                            break

                        elif (c_atual == ' '):
                            break

                    if (len(string) > 0):
                        if (self.eh_reservada(string)):
                            self.adiciona_token(string)

                            entrada = self.eh_reservada(string)

                            self.__tabela_simbolos.adiciona_entrada(
                                [entrada['nome'], entrada['token'], numero_linha])
                            continue
                        else:
                            self.adiciona_token('ident')

                            self.__tabela_simbolos.adiciona_entrada(
                                [string, 'IDENT', numero_linha])

                elif (self.eh_digito(caractere_atual)):
                    string = caractere_atual
                    indice_caractere += 1
                    caractere_atual = linha[indice_caractere]

                    nro_digitos_float = 0

                    while (self.eh_digito(caractere_atual) and (indice_caractere + 1 < tamanho_linha)):
                        string += caractere_atual
                        indice_caractere += 1
                        caractere_atual = linha[indice_caractere]

                    if (caractere_atual == '.'):
                        if ((indice_caractere + 1) < tamanho_linha):
                            string += caractere_atual
                            indice_caractere += 1
                            caracter_atual = linha[i]

                        while self.eh_digito(caractere_atual) and (indice_caractere + 1 < tamanho_linha):
                            string += caracter_atual
                            nro_digitos_float += 1

                            indice_caractere += 1

                            caractere_atual = linha[indice_caractere]

                        if caractere_atual == '.' and linha[indice_caractere - 1] != self.eh_digito(linha[indice_caractere - 1]) and linha[indice_caractere + 1] != self.eh_digito(linha[indice_caractere + 1]):
                            raise Exception(
                                f'Erro léxico! - Número de ponto flutuante mal formado - Linha: {numero_linha} - Coluna: {indice_caractere}')

                        if (nro_digitos_float > 0):
                            self.adiciona_token('float')

                            self.__tabela_simbolos.adiciona_entrada(
                                [string, 'FLOAT', numero_linha])
                            continue
                        else:
                            raise Exception(
                                f'Erro léxico! - Número de ponto flutuante mal formado - Linha: {numero_linha} - Coluna: {indice_caractere}')
                    else:
                        self.adiciona_token('int')

                        self.__tabela_simbolos.adiciona_entrada(
                            [string, 'INT', numero_linha])
                        continue
