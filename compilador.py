from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico
import sys

if not sys.argv[1]:
    print("Nenhum arquivo foi fornecido.\n")
else:
    try:
        lex = AnalisadorLexico(sys.argv[1])
        lex.analisador()
        lista_tokens = lex.recupera_lista_tokens()
        sin = AnalisadorSintatico(lista_tokens, None)
        sin.analisador()
    except Exception as ex:
        print(str(ex))
