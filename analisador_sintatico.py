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
                raise Exception(f"Erro Sintático esperava: ident para sequência PARAMLIST = ((int | float | string) *ident* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}") 
            else:
                self.set_indice(self.indice_atual + 1)
                if self.token_atual == ")":
                    return True
                elif self.token_atual == ",":
                    self.set_indice(self.indice_atual + 1)
                    return self.eh_paramlist()
                else:
                    raise Exception(f"Erro Sintático esperava: ) para sequência PARAMLIST = ((int | float | string) ident *)* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
    
    def eh_vardecl(self):
        if self.token_atual in self.valid_types:
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "ident":
                raise Exception(f"Erro Sintático esperava: ident para sequência VARDECL = (int | float | string) *ident* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            else:
                self.set_indice(self.indice_atual + 1)
                if self.token_atual != "[":
                    return True
                else:
                    self.set_indice(self.indice_atual + 1)
                    if self.token_atual != "int_constant":
                        raise  Exception(f"Erro Sintático esperava: int_constant para sequência VARDECL = (int | float | string) ident[*int_constant* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                    else: 
                        self.set_indice(self.indice_atual + 1)
                        if self.token_atual != "]":
                            raise Exception(f"Erro Sintático esperava: ] para sequência VARDECL = (int | float | string) ident[int_constant *]* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
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
                    raise  Exception(f"Erro Sintático esperava: NUM_EXPRESSION para sequência FACTOR = {' | '.join([valid_tokens + 'LVALUE'])} (*NUM_EXPRESSION* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                if self.token_atual != ")":
                    raise Exception(f"Erro Sintático esperava: ) para sequência FACTOR = {' | '.join([valid_tokens + 'LVALUE'])} (NUM_EXPRESSION*)* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
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
                    raise Exception(f"Erro Sintático esperava: UNARY_EXPRESSION para sequência TERM = {' | '.join(['*', '/', '%'])} UNARY_EXPRESSION recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            return True
        return False
    
    
    def eh_num_expression(self):
        if self.eh_term():
            if self.token_atual in ["+", "-"]:
                self.set_indice(self.indice_atual + 1)
                if not self.eh_term():
                    raise  Exception(f"Erro Sintático esperava: TERM para sequência NUM_EXPRESSION = TERM {' | '.join(['+', '-'])} *TERM* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
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
                    raise Exception(f"Erro Sintático esperava: NUM_EXPRESSION para sequência LVALUE = ident[*NUM_EXPRESSION* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                else: 
                    if self.token_atual != "]":
                        raise Exception(f"Erro Sintático esperava: ] para sequência LVALUE = ident[NUM_EXPRESSION*]* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
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
                    raise Exception(f"Erro Sintático esperava: NUM_EXPRESSION para sequência EXPRESSION = NUM_EXPRESSION {' | '.join(operators)} *NUM_EXPRESSION* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            return True
        return False
    
    def eh_alloc_expression(self):
        if self.token_atual == "new":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual not in ["int", "float", "string"]:
                raise Exception(f"Erro Sintático esperava: (int | float | string) para sequência ALLOC_EXPRESSION = new *(int | float | string)* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            self.set_indice(self.indice_atual + 1)
            if self.token_atual == "[":
                self.set_indice(self.indice_atual + 1)
                if not self.eh_num_expression():
                    raise Exception(f"Erro Sintático esperava: NUM_EXPRESSION para sequência ALLOC_EXPRESSION = new (int | float | string)[*NUM_EXPRTESSION* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                if self.token_atual != "]":
                    raise Exception(f"Erro Sintático esperava: ] para sequência ALLOC_EXPRESSION = new (int | float | string)[NUM_EXPRTESSION*]* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                self.set_indice(self.indice_atual + 1)
            return True
        
    def eh_paramlist_call(self):
        if self.token_atual != "ident":
            raise Exception(f"Erro Sintático esperava: ident para sequência PARAMLIST_CALL = *ident* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
        else:
            self.set_indice(self.indice_atual + 1)
            if self.token_atual == ")":
                return True
            elif self.token_atual == ",":
                self.set_indice(self.indice_atual + 1)
                return self.eh_paramlist_call()
            else:
               return False
    
    
    def eh_func_call(self):
        indice_inicial= self.indice_atual
        if self.token_atual == "ident":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "(":
                self.set_indice(indice_inicial)
                return False
            self.set_indice(self.indice_atual + 1)
            if not self.eh_paramlist_call():
                raise Exception(f"Erro Sintático esperava: PARAMLIST_CALL para sequência FUNC_CALL = ident(*PARAMLIST_CALL* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            if self.token_atual != ")":
                raise Exception(f"Erro Sintático esperava: ) para sequência FUNC_CALL = ident(PARAMLIST_CALL*)* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            self.set_indice(self.indice_atual + 1)
            return True
        return False

    def eh_atribstat(self):
        if self.eh_lvalue():
            if self.token_atual != "=":
                raise Exception(f"Erro Sintático esperava: = para sequência ATRIBSTAT = LVALUE *=* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            else:
                self.set_indice(self.indice_atual + 1)
                if self.eh_func_call():
                    return True
                elif self.eh_expression():
                    return True
                elif self.eh_alloc_expression():
                    return True
                else:
                    raise Exception(f"Erro Sintático esperava: (EXPRESSION | ALLOC_EXPRESSION | FUNC_CALL) para sequência ATRIBSTAT = LVALUE = (EXPRESSION | ALLOC_EXPRESSION | FUNC_CALL) recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
        else:
            return False

    def eh_print(self):
        if self.token_atual == "print":
            self.set_indice(self.indice_atual + 1)
            if not self.eh_expression():
                raise Exception(f"Erro Sintático esperava: EXPRESSION para sequência print *EXPRESSION* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            return True
        return False

    def eh_read(self):
        if self.token_atual == "read":
            self.set_indice(self.indice_atual + 1)
            if not self.eh_lvalue():
                raise Exception(f"Erro Sintático esperava: LVALUE para sequência read *LVALUE* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            return True
        return False
    
    def eh_return(self):
        if self.token_atual == "return":
            self.set_indice(self.indice_atual + 1)
            self.eh_expression()
            return True
        return False
    
    def eh_if(self):
        if self.token_atual == "if":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "(":
                raise Exception(f"Erro Sintático esperava: ( para sequência if *(* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            self.set_indice(self.indice_atual + 1)
            if not self.eh_expression():
                raise Exception(f"Erro Sintático esperava: EXPRESSION para sequência if (*EXPRESSION* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            if self.token_atual != ")":
                raise Exception(f"Erro Sintático esperava: ) para sequência if (EXPRESSION*)* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            self.set_indice(self.indice_atual + 1)
            if not self.eh_statement():
                raise Exception(f"Erro Sintático esperava: STATEMENT para sequência if (EXPRESSION) STATEMENT recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            
            if self.token_atual == "else":
                self.set_indice(self.indice_atual + 1)
                if not self.eh_statement():
                    raise Exception(f"Erro Sintático esperava: STATEMENT para sequência if (EXPRESSION) STATEMENT else *STATEMENT* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            return True
        return False

    def eh_for(self):
        if self.token_atual == "for":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != "(":
                raise Exception(f"Erro Sintático esperava: ( para sequência for *(* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            self.set_indice(self.indice_atual + 1)
            if not self.eh_atribstat():
                raise Exception(f"Erro Sintático esperava: ATRIBSTAT para sequência for(*ATRIBSTAT* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            if self.token_atual != ";":
                raise Exception(f"Erro Sintático esperava: ; para sequência for(ATRIBSTAT*;* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            self.set_indice(self.indice_atual + 1)
            if not self.eh_expression():
                raise Exception(f"Erro Sintático esperava: EXPRESSION para sequência for(ATRIBSTAT;*EXPRESSION* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            if self.token_atual != ";":
                raise Exception(f"Erro Sintático esperava: ; para sequência for(ATRIBSTAT;EXPRESSION*;* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            self.set_indice(self.indice_atual + 1)
            if not self.eh_atribstat():
                raise Exception(f"Erro Sintático esperava: ATRIBSTAT para sequência for(ATRIBSTAT;EXPRESSION;*ATRIBSTAT* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            if self.token_atual != ")":
                raise Exception(f"Erro Sintático esperava: ) para sequência for(ATRIBSTAT;EXPRESSION;ATRIBSTAT*)* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            self.set_indice(self.indice_atual + 1)
            if not self.eh_statement():
                raise Exception(f"Erro Sintático esperava: STATEMENT para sequência for(ATRIBSTAT;EXPRESSION;ATRIBSTAT)*STATEMENT* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            return True
        return False

    def eh_statement(self):
        if self.eh_vardecl():
            if self.token_atual != ";":
                raise Exception(f"Erro Sintático esperava: ; para sequência STATEMENT = VARDECL*;* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            else:
                self.set_indice(self.indice_atual + 1)
                return True
            
        if self.eh_atribstat():
            if self.token_atual != ";":
                raise Exception(f"Erro Sintático esperava: ; para sequência STATEMENT = ATRIBSTAT*;* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            else:
                self.set_indice(self.indice_atual + 1)
                return True
                
        if self.eh_print():
            if self.token_atual != ";":
                raise Exception(f"Erro Sintático esperava: ; para sequência STATEMENT = PRINT*;* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            else:
                self.set_indice(self.indice_atual + 1)
                return True
                
        if self.eh_read():
            if self.token_atual != ";":
                raise Exception(f"Erro Sintático esperava: ; para sequência STATEMENT = READ*;* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            else:
                self.set_indice(self.indice_atual + 1)
                return True
    
        if self.eh_return():
            if self.token_atual != ";":
                raise Exception(f"Erro Sintático esperava: ; para sequência STATEMENT = RETURN*;* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
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
                raise Exception(f"Erro Sintático esperava: {'}'} para sequência STATEMENT = {'{'}STATELIST{'*}*'} recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            else:
                self.set_indice(self.indice_atual + 1)
                return True

        if self.token_atual == "break":
            self.set_indice(self.indice_atual + 1)
            if self.token_atual != ";":
                raise Exception(f"Erro Sintático esperava: ; para sequência STATEMENT = break*;* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
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
                raise Exception(f"Erro Sintático esperava: ident para sequência FUNCDEF = def *ident* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
            else:
                self.set_indice(self.indice_atual + 1)
                if self.token_atual != "(":
                    raise Exception(f"Erro Sintático esperava: ( para sequência FUNCDEF = def ident*(* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                else:
                    self.set_indice(self.indice_atual + 1)
                    if self.token_atual != ")":
                        if not self.eh_paramlist():
                            raise Exception(f"Erro Sintático esperava: PARAMLIST para sequência FUNCDEF = def ident(*PARAMLIST* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                    if self.token_atual != ")":
                        raise Exception(f"Erro Sintático esperava: ) para sequência FUNCDEF = def ident(PARAMLIST*)* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                    else:
                        self.set_indice(self.indice_atual + 1)
                        if self.token_atual != "{":
                            raise Exception(f"Erro Sintático esperava: {'{'} para sequência FUNCDEF = def ident(PARAMLIST)*{'{'}* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                        else:
                            self.set_indice(self.indice_atual + 1)
                            if not self.eh_statelist():
                                raise Exception(f"Erro Sintático esperava: STATELIST para sequência FUNCDEF = def ident(PARAMLIST){'{'}*STATELIST* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                            if self.token_atual != "}":
                                raise Exception(f"Erro Sintático esperava: {'}'} para sequência FUNCDEF = def ident(PARAMLIST){'{'} STATELIST {'*}*'} recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
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
                    raise Exception(f"Erro Sintático esperava: (FUNCLIST | STATEMENT) para sequência PROGRAM = *(FUNCLIST | STATEMENT)* recebeu {self.token_atual} na linha {self.tabela.recupera_tabela()[self.indice_atual][-1]}")
                else:
                    pass
