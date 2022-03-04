# -PROGRAM → (STATEMENT | FUNCLIST)?
# -FUNCLIST → FUNCDEF FUNCLIST | FUNCDEF
# -FUNCDEF → def ident(PARAMLIST){STATELIST}
# -PARAMLIST → (( int | float | string ) ident, PARAMLIST | ( int | float | string ) ident)?
# STATEMENT → (
    # -VARDECL; | 
    # -ATRIBSTAT; | 
    # -PRINTSTAT; | 
    # READSTAT; | 
    # RETURNSTAT; | 
    # IFSTAT | 
    # FORSTAT | 
    # {STATELIST} | 
    # break ; |
    # ;
#)
# -VARDECL → ( int | float | string ) ident ([int constant])∗
# -ATRIBSTAT → LV ALUE = ( EXPRESSION | ALLOCEXPRESSION | FUNCCALL)
# -FUNCCALL → ident(PARAMLISTCALL)
# -PARAMLISTCALL → (ident, PARAMLISTCALL | ident)?
# -PRINTSTAT → print EXPRESSION
# - READSTAT → read LV ALUE
# - RETURNSTAT → return
# - IFSTAT → if( EXPRESSION ) STATEMENT (else STATEMENT)?
# - FORSTAT → for(ATRIBSTAT; EXPRESSION; ATRIBSTAT)
#                 STATEMENT
# - STATELIST → STATEMENT (STATELIST)?
# -ALLOCEXPRESSION → new (int | float | string) ([ NUMEXPRESSION ])+
# -EXPRESSION → NUMEXPRESSION(( < | > | <= | >= | == | ! =) NUMEXPRESSION)?
# -NUMEXPRESSION → TERM ((+ |−) TERM)∗
# -TERM → UNARY EXPR(( ∗ | / | %) UNARY EXPR)∗
# -UNARY EXPR → ((+ |−))? FACTOR
# -FACTOR → (int constant | float constant | string constant | null | LV ALUE |(NUMEXPRESSION))
# -LV ALUE → ident( [NUMEXPRESSION] )∗ 

from tabela_simbolos import TabelaSimbolos


class AnalisadorSintatico:
    def __init__(self, lista_tokens: list, tabela_simbolos: TabelaSimbolos) -> None:
        self.lista_tokens = lista_tokens
        self.tabela = tabela_simbolos
        self.token_atual = None
        self.indice_atual = 0
        self.analizando = True
        self.valid_types = ["int", "float", "string"]
    
    def set_indice(self, integer: int):
        self.indice_atual = integer
        if integer >= len(self.lista_tokens):
            return
        self.token_atual = self.lista_tokens[self.indice_atual]
        
    def eh_paramlist(self):
        """
        Checa se é param list
        (( int | float | string ) ident, PARAMLIST | ( int | float | string ) ident)?
        executa uma vez o check se existe virgula chama a função recursiva a idéia é que depois do check tem que haver ou ) ou , 
        no caso de )
        retorna true isso é um paramlist
        no caso de ,
        executa a função recursivamente pois outro pramlist pode ser executado
        """
        if self.token_atual in self.valid_types:
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "ident":
                raise Exception()
            else:
                self.set_indice(self.indice_atual + 1)
                if self.token_atual == ")":
                    return True
                elif self.token_atual == ",":
                    self.set_indice(self.indice_atual + 1)
                    return self.eh_paramlist()
                else:
                    raise Exception
    
    def eh_vardecl(self):
        if self.token_atual in self.valid_types:
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "ident":
                raise Exception
            else:
                self.set_indice(self.indice_atual + 1)
                if self.token_atual != "[":
                    return True
                else:
                    self.set_indice(self.indice_atual + 1)
                    if self.token_atual != "int_constant":
                        raise Exception
                    else: 
                        self.set_indice(self.indice_atual + 1)
                        if self.token_atual != "]":
                            raise Exception
                        else: 
                            self.set_indice(self.indice_atual + 1)
                            return True
        else:
            return False

    def eh_factor(self):
        valid_tokens = ["int_constant","float_constant","string_constant", "null"]
        if self.token_atual in valid_tokens:
            self.set_indice(self.indice_atual + 1)
            return True
        elif self.eh_lvalue():
            return True
        else:
            if self.token_atual == "(":
                self.set_indice(self.indice_atual + 1)
                if not self.eh_num_expression():
                    raise
                if self.token_atual != ")":
                    raise
                self.set_indice(self.indice_atual + 1)
                return True
        return False

    def eh_unary_expression(self):
        valid_tokens = ["+", "-"]
        if self.token_atual in valid_tokens:
            self.set_indice(self.indice_atual + 1)
        return self.eh_factor()

    
    def eh_term(self):
        if self.eh_unary_expression():
            if self.token_atual in ["*", "/", "%"]:
                self.set_indice(self.indice_atual + 1)
                if not self.eh_unary_expression():
                    raise
            return True
        return False
    
    
    def eh_num_expression(self):
        if self.eh_term():
            if self.token_atual in ["+", "-"]:
                self.set_indice(self.indice_atual + 1)
                if not self.eh_term():
                    raise
            return True
        return False

    def eh_lvalue(self):
        if self.token_atual == "ident":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "[":
                return True
            else:
                self.set_indice(self.indice_atual + 1)
                if not self.eh_num_expression():
                    raise Exception
                else: 
                    if self.token_atual != "]":
                        raise Exception
                    else:
                        self.set_indice(self.indice_atual + 1)
                        return True
        else:
            return False

    def eh_expression(self):
        operators = ["<", ">", "<=", ">=", "==", "!="]
        if self.eh_num_expression():
            if self.token_atual in operators:
                self.set_indice(self.indice_atual + 1)
                if not self.eh_num_expression():
                    raise Exception
            return True
        return False
    
    def eh_alloc_expression(self):
        if self.token_atual == "new":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual not in ["int", "float", "string"]:
                raise
            self.set_indice(self.indice_atual + 1)
            if self.token_atual == "[":
                self.set_indice(self.indice_atual + 1)
                if not self.eh_num_expression():
                    raise 
                if self.token_atual != "]":
                    raise
                self.set_indice(self.indice_atual + 1)
            return True
        
    def eh_paramlist_call(self):
        if self.token_atual != "ident":
            raise Exception()
        else:
            self.set_indice(self.indice_atual + 1)
            if self.token_atual == ")":
                return True
            elif self.token_atual == ",":
                self.set_indice(self.indice_atual + 1)
                return self.eh_paramlist_call()
            else:
                raise Exception
    
    
    def eh_func_call(self):
        indice_inicial= self.indice_atual
        if self.token_atual == "ident":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "(":
                self.set_indice(indice_inicial)
                return False
            self.set_indice(self.indice_atual + 1)
            if not self.eh_paramlist_call():
                raise
            if self.token_atual != ")":
                raise
            self.set_indice(self.indice_atual + 1)
            return True
        return False

    def eh_atribstat(self):
        if self.eh_lvalue():
            if self.token_atual != "=":
                raise Exception
            else:
                self.set_indice(self.indice_atual + 1)
                if self.eh_func_call():
                    return True
                elif self.eh_expression():
                    return True
                elif self.eh_alloc_expression():
                    return True
                else:
                    raise Exception
        else:
            return False

    def eh_print(self):
        if self.token_atual == "print":
            self.set_indice(self.indice_atual + 1)
            if not self.eh_expression():
                raise
            return True
        return False

    def eh_read(self):
        if self.token_atual == "read":
            self.set_indice(self.indice_atual + 1)
            if not self.eh_lvalue():
                raise
            return True
        return False
    
    def eh_return(self):
        if self.token_atual == "return":
            self.set_indice(self.indice_atual + 1)
            return True
        return False
    
    def eh_if(self):
        if self.token_atual == "if":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "(":
                raise 
            self.set_indice(self.indice_atual + 1)
            if not self.eh_expression():
                raise 
            if self.token_atual != ")":
                raise 
            self.set_indice(self.indice_atual + 1)
            if not self.eh_statement():
                raise 
            
            if self.token_atual == "else":
                self.set_indice(self.indice_atual + 1)
                if not self.eh_statement():
                    raise
            return True
        return False

    def eh_for(self):
        if self.token_atual == "for":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "(":
                raise
            self.set_indice(self.indice_atual + 1)
            if not self.eh_atribstat():
                raise 
            if self.token_atual != ";":
                raise 
            self.set_indice(self.indice_atual + 1)
            if not self.eh_expression():
                raise 
            if self.token_atual != ";":
                raise 
            self.set_indice(self.indice_atual + 1)
            if not self.eh_atribstat():
                raise 
            if self.token_atual != ")":
                raise
            self.set_indice(self.indice_atual + 1)
            if not self.eh_statement():
                raise
            return True
        return False

    def eh_statement(self):
        if self.eh_vardecl():
            if self.token_atual != ";":
                raise Exception("Declaração de váriavel sem ';'")
            else:
                self.set_indice(self.indice_atual + 1)
                return True
            
        if self.eh_atribstat():
            if self.token_atual != ";":
                raise Exception("Atribuição de varável sem ';'")
            else:
                self.set_indice(self.indice_atual + 1)
                return True
                
        if self.eh_print():
            if self.token_atual != ";":
                raise Exception("print sem ';'")
            else:
                self.set_indice(self.indice_atual + 1)
                return True
                
        if self.eh_read():
            if self.token_atual != ";":
                raise Exception("read sem ';'")
            else:
                self.set_indice(self.indice_atual + 1)
                return True
    
        if self.eh_return():
            if self.token_atual != ";":
                raise Exception("return sem ';'")
            else:
                self.set_indice(self.indice_atual + 1)
                return True
            
        if self.eh_if():
            return True
       
        if self.eh_for():
            return True
       
        if self.token_atual == "{":
            self.set_indice(self.indice_atual + 1)
            self.eh_statelist()
            if self.token_atual != "}":
                raise Exception
            else:
                self.set_indice(self.indice_atual + 1)
                return True

        if self.token_atual == "break":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != ";":
                raise Exception
            else:
                self.set_indice(self.indice_atual + 1)
                return True

        if self.token_atual == ";":
            self.set_indice(self.indice_atual + 1)
            return True
        return False

    def eh_statelist(self):
        while self.token_atual != "}":
            self.eh_statement()
        return True
    
    def eh_funcdef(self):
        """
        Checa se os tokens seguintes configuram uma funcdef
        def ident(PARAMLIST){STATELIST}
        """
        indice_inicial = self.indice_atual
        if self.token_atual == "def":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "ident":
                raise Exception("Esperava um indentificador após uma def")
            else:
                self.set_indice(self.indice_atual + 1)
                if self.token_atual != "(":
                    raise Exception("Esperava um '(' após um identificador ao declarar uma função")
                else:
                    self.set_indice(self.indice_atual + 1)
                    if self.token_atual != ")":
                        if not self.eh_paramlist():
                            raise Exception("")
                    if self.token_atual != ")":
                        raise Exception("")
                    else:
                        self.set_indice(self.indice_atual + 1)
                        if self.token_atual != "{":
                            raise Exception("")
                        else:
                            self.set_indice(self.indice_atual + 1)
                            if not self.eh_statelist():
                                raise Exception
                            if self.token_atual != "}":
                                raise Exception
                            self.set_indice(self.indice_atual + 1)
                            return True
        self.set_indice(indice_inicial)
        return False

    
    def eh_funclist(self):
        if self.eh_funcdef():
            while self.token_atual == "def":
                self.eh_funcdef()
            return True
        return False       
        

    
    def analisador(self):
        self.set_indice(0)
        while self.indice_atual < len(self.lista_tokens):
             if not self.eh_funclist():
                if not self.eh_statement():
                    raise
                else:
                    pass
