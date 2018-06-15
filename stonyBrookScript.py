import math



class Node:
    def __init__(self):
        print("init node")

    def evaluate(self):
        return 0

    def execute(self):
        return 0

class NumberNode(Node):
    def __init__(self, v):
        if('.' in v):
            self.value = float(v)
        else:
            self.value = int(v)

    def evaluate(self):
        return self.value


class StringNode(Node):
    def __init__(self, v):
        if v[0]=='"' or v[0]=="'":
            self.value = v[1:-1]
        else:
            self.value=v

    def evaluate(self):
        return self.value

class BooleanNode(Node):
    def __init__(self, v):
        self.value = v

    def evaluate(self):
        if self.value == "True":
            return True
        elif self.value == "False":
            return False 

class ListNode(Node):
    def __init__(self, v,index):
        self.value=v
        self.index = index.evaluate()
        
    def evaluate(self):
        return (self.value.evaluate())[self.index]


class SingleNode(Node):
    def __init__(self, op, v1):
        self.v1 = v1
        self.op = op

    def evaluate(self):
        if (self.op == 'not'):
            return not self.v1.evaluate()

class BopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if (self.op == '+'):
            return self.v1.evaluate() + self.v2.evaluate()
        elif (self.op == '-'):
            return self.v1.evaluate() - self.v2.evaluate()
        elif (self.op == '*'):
            return self.v1.evaluate() * self.v2.evaluate()
        elif (self.op == '/'):
            return self.v1.evaluate() / self.v2.evaluate()
        elif(self.op == '**'):
            return math.pow(self.v1.evaluate(),self.v2.evaluate())
        elif (self.op == '%'):
            return self.v1.evaluate() % self.v2.evaluate()
        elif (self.op == '//'):
            return math.floor((self.v1.evaluate() / self.v2.evaluate()))
        elif (self.op == '<'):
            return self.v1.evaluate() < self.v2.evaluate()
        elif (self.op == '<='):
            return self.v1.evaluate() <= self.v2.evaluate()
        elif (self.op == '=='):
            return self.v1.evaluate() == self.v2.evaluate()
        elif (self.op == '<>'):
            return self.v1.evaluate() != self.v2.evaluate()
        elif (self.op == '>'):
            return self.v1.evaluate() > self.v2.evaluate()
        elif (self.op == '>='):
            return self.v1.evaluate() >= self.v2.evaluate()
        elif (self.op == 'and'):
            return self.v1.evaluate() and self.v2.evaluate()  
        elif (self.op == 'or'):
            return self.v1.evaluate() or self.v2.evaluate()
        elif (self.op == 'in'):
            return self.v1.evaluate() in self.v2.evaluate()
        


class assignNode(Node):
    def __init__(self, v):
        self.value = v

    def execute(self):
        if type(self.value.evaluate()) is str:
            self.value = self.value.evaluate()
            return "'"+self.value+"'"
        else:
            self.value = self.value.evaluate()
            return self.value

class BlockNode(Node):
    def __init__(self, s):
        self.sl = [s]

    def evaluate(self):
        return self.sl

tokens = (
    'LBRACE', 'RBRACE','STRING','QUATION','LBRACKT','RBRACKT',
    'LPAREN', 'RPAREN', 'SEMI', 'LIST','NOT','IN','OR',
    'NUMBER','POWER', 'MODULUS','FLOOR','BOOLEAN',
    'PLUS','MINUS','TIMES','DIVIDE','LESS','LEEEQUE','EUQAL',
    'NOTEQUAL','LARGE','LARGEEQUE','AND','COMMA'
    )

# Tokens
t_LBRACKT  = r'\['
t_RBRACKT = r'\]'
# t_PRINT    = 'print'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_SEMI  = r';'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_POWER = r'\*\*'
t_DIVIDE  = r'/'
t_MODULUS = r'\%'
t_FLOOR = r'//'
t_QUATION = r'"'
t_LESS = r'\<'
t_LEEEQUE = r'\<\='
t_EUQAL = r'\=\='
t_NOTEQUAL = r'\<\>'
t_LARGE = r'\>'
t_LARGEEQUE = r'\>\='
t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'
t_IN = r'in'
t_COMMA=r','


def t_NUMBER(t):
    r'\d*(\d\.|\.\d)\d* | \d+'
    try:
        t.value = NumberNode(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_STRING(t):
    r'\"(\\.|[^\\"])*\"|\'(\\.|[^\\\'])*\''
    t.value = StringNode(t.value)
    return t

def t_BOOLEAN(t):
    r'True|False'
    t.value = BooleanNode(t.value)
    return t

# def t_LIST(t):
#     # a=\[(\d*,)+\d*
#     r'\[(\d*,)+\d*'
#     t.value = ListNode(t.value)
#     return t


# Ignored characters
t_ignore = " \t"

def t_error(t):
    raise Exception("Syntax Error")
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules
precedence = (
    ('left','AND'),
    ('left','NOT'),
    ('left','LESS','LEEEQUE','EUQAL','NOTEQUAL','LARGE','LARGEEQUE'),
    ('left','IN'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','MODULUS','FLOOR'),
    ('right','POWER')
    )

def p_smt(t):
    """
    smt : expression 
    """
    t[0] = assignNode(t[1])

def p_expression_listElement(t):
    """
    expression : expression LBRACKT factor RBRACKT 
    """
    t[0] = ListNode(t[1],t[3])

def p_inblock2(t):
    """
    expression : LPAREN expression RPAREN
    """
    t[0] = t[2]


def p_expression_list(t):
    """
    expression : LBRACKT inblock RBRACKT 
    """
    t[0] = t[2]


def p_inblock(t):
    """
    inblock : expression COMMA inblock
    """
    t[0] = t[3]
    t[0].sl.insert(0,t[1].evaluate())

def p_inblock3(t):
    """
    inblock : expression
    """
    t[0] = BlockNode(t[1].evaluate())

# def p_index(t):
#     'index : factor'
#     print("index",t[1].evaluate())
#     t[0] = t[1]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression
                  | expression MODULUS expression
                  | expression FLOOR expression
                  | expression LESS expression
                  | expression LEEEQUE expression
                  | expression EUQAL expression
                  | expression NOTEQUAL expression
                  | expression LARGE expression
                  | expression LARGEEQUE expression
                  | expression AND expression
                  | expression OR expression
                  | expression IN expression'''
    t[0] = BopNode(t[2], t[1], t[3])

def p_expression_single(t):
    '''expression : NOT expression'''
    t[0] = SingleNode(t[1], t[2])

# def p_expression_getList(t):
#     '''expression : expression LISTGET factor RBRACKT'''
#     t[0] = getListElemet(t[1],t[3])

def p_expression_factor(t):
    '''expression : factor'''
    t[0] = t[1]

def p_factor_number(t):
    'factor : NUMBER'
    t[0] = t[1]

def p_factor_boolean(t):
    'factor : BOOLEAN'
    t[0] = t[1]

# def p_factor_list(t):
#     'factor : LIST'
#     t[0] = t[1]

def p_factor_string(t):
    'factor : STRING'
    t[0] = t[1]


def p_error(t):
    # print("Syntax Error")
    raise Exception("Syntax Error")

import ply.yacc as yacc
yacc.yacc()

import sys

#if (len(sys.argv) != 2):
#    sys.exit("invalid arguments")
#fd = open(sys.argv[1], 'r')
#code = ""
#for line in fd:
#    code += line.strip()


with open(sys.argv[1],'r') as txt:
    codes=txt.readlines()
    for code in codes:
        code = code.strip('\n')
        try:
            # lex.input(code)
            # while True:
            #    token = lex.token()
            #    if not token: break
            #    print(token)
            ast = yacc.parse(code)
            print(ast.execute())
        except Exception as e:
            if str(e)== "Syntax Error" :
                print("SYNTAX ERROR")
            else:
                print("SEMANTIC ERROR")


    


