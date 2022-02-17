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
# ident - Representa um identificado
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


class AnalisadorLexico():
    def __init__(self):
        self.__entrada = "entrada.txt"
        self.__saida = "saida.txt"

    def mudaEntrada(self, novaEntrada):
        self.__entrada = novaEntrada

    def recuperaEntrada(self):
        return self.__entrada

    def recuperaSaida(self):
        return self.__saida

    def ehDelimitador(self, caractere):
        delimitadores = ["()", "{}", ",", ";", "[]"]
        if caractere in delimitadores:
            return caractere
        else:
            return False

    def ehOperador(self, caractere):
        operadores = ["=", "<", ">", "<=", ">=",
                      "==", "!=", "+", "-", "*", "/", "%"]
        if caractere in operadores:
            return caractere
        else:
            return False

    def ehLetra(self, caractere):
        letras = string.ascii_letters

        if caractere in letras:
            return caractere
        else:
            return False

    def ehDigito(self, caractere):
        digitos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        if caractere in digitos:
            return caractere
        else:
            return False

    def ehReservada(self, palavra):
        reservadas = ["def", "int", "float", "string",
                      "break", "print", "read", "return",
                      "if", "else", "for", "new", "int_constant",
                      "float_constant", "string_constant", "null"]
        
        if palavra in reservadas:
            return palavra
        else:
            return False
