# Hengqi Zhu 111212811
import math
dictionary = {}


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

class NoneNode(Node):
    def __init__(self):
        pass

    def execute(self):
        pass

class StringNode(Node):
    def __init__(self, v):
        if v[0]=='"' or v[0]=="'":
            self.value = v[1:-1]
        else:
            self.value=v

    def evaluate(self):
        return self.value

class VariableNode(Node):
    def __init__(self, v):
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

class emptyListNode(Node):
    def __init__(self):
        self.value=[]
    
    def evaluate(self):   
        return self.value

class ListNode(Node):
    def __init__(self, v,index):
        # if type(v) is VariableNode:
        #     v = dictionary.get(v.evaluate())
        self.value=v
        # if type(index) is VariableNode:
        #     self.index = dictionary.get(index.evaluate())
        # else:
        self.index = index
        # print(self.value,self.index)


    def evaluate(self):
        if type(self.value) is VariableNode:
            a = dictionary.get(self.value.evaluate())
        else:
            a = self.value.evaluate()
        if type(self.index) is VariableNode:
            b = dictionary.get(self.index.evaluate())
        else:
            b = self.index.evaluate()
        return a[b]


class SingleNode(Node):
    def __init__(self, op, v1):
        self.v1 = v1
        self.op = op

    def evaluate(self):
        if type(self.v1) is VariableNode:
            a = dictionary.get(self.v1.evaluate())
        else:
            a = self.v1.evaluate()
        if (self.op == 'not'):
            return not a
        elif (self.op == '-'):
            return 0-a

class BopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if type(self.v1) is VariableNode:
            a = dictionary.get(self.v1.evaluate())
        else:
            a = self.v1.evaluate()
        if type(self.v2) is VariableNode:
            b = dictionary.get(self.v2.evaluate())
        else:
            b = self.v2.evaluate()
        
        if (self.op == '+'):
            return a + b
        elif (self.op == '-'):
            return a - b
        elif (self.op == '*'):
            return a * b
        elif (self.op == '/'):
            return a / b
        elif(self.op == '**'):
            return math.pow(a,b)
        elif (self.op == '%'):
            return a % b
        elif (self.op == '//'):
            return math.floor((a / b))
        elif (self.op == '<'):
            return a < b
        elif (self.op == '<='):
            return a <= b
        elif (self.op == '=='):
            return a == b
        elif (self.op == '<>'):
            return a != b
        elif (self.op == '>'):
            return a > b
        elif (self.op == '>='):
            return a >= b
        elif (self.op == 'and'):
            return a and b  
        elif (self.op == 'or'):
            return a or b
        elif (self.op == 'in'):
            return a in b

class assignNode(Node):
    def __init__(self, v1,v2):
        self.v1 = v1
        self.v2 = v2

    def execute(self):
        if type(self.v2) is VariableNode:
            a = dictionary.get(self.v2.evaluate())
        else:
            a = self.v2.evaluate()
        dictionary[self.v1.evaluate()]=a

class assignNode1(Node):
    def __init__(self, v1,v2,v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def execute(self):
        if type(self.v2) is VariableNode:
            a = dictionary.get(self.v2.evaluate())
        else:
            a = self.v2.evaluate()
        if type(self.v3) is VariableNode:
            b = dictionary.get(self.v3.evaluate())
        else:
            b = self.v3.evaluate()
        if type(self.v1) is VariableNode:
            c = dictionary.get(self.v1.evaluate())
        else:
            c = self.v1.evaluate()
        c[a]=b


class calculateNode(Node):
    def __init__(self, v):
        self.value = v

    def execute(self):
        if type(self.value) is StringNode:
            self.value = self.value.evaluate()
            return "'"+self.value+"'"
        elif hasattr(self.value,'evaluate'):
            self.value = self.value.evaluate()
            return self.value
        else:
            return self.value


class ifNode(Node):
    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2


    def execute(self):
        if type(self.v1) is VariableNode:
            a = dictionary.get(self.v1.evaluate())
        else:
            a = self.v1.evaluate()
        if a:
            self.v2.execute()

class PrintNode(Node):
    def __init__(self, v):
        self.value = v

    def execute(self):     
        if type(self.value) == VariableNode:
            print(dictionary.get(self.value.evaluate()))
        elif hasattr(self.value,'evaluate'):
            self.value = self.value.evaluate()
            print(self.value)
        else:
            print(self.value)


class ifelseNode(Node):
    def __init__(self,v1,v2,v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def execute(self):
        if type(self.v1) is VariableNode:
            a = dictionary.get(self.v1.evaluate())
        else:
            a = self.v1.evaluate()
        if a:
            self.v2.execute()
        else:
            self.v3.execute()

class whileNode(Node):
    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2

    def execute(self):
        if type(self.v1) is VariableNode:
            a = dictionary.get(self.v1.evaluate())
        else:
            a = self.v1.evaluate()
        while a:
            self.v2.execute()
            if type(self.v1) is VariableNode:
                a = dictionary.get(self.v1.evaluate())
            else:
                a = self.v1.evaluate()


class BlockNode(Node):
    def __init__(self, s):
        self.sl = [s]

    def evaluate(self):
        return self.sl

class BraceNode(Node):
    def __init__(self, s):
        self.sl = [s]

    def execute(self):
        for statement in self.sl:
            if statement is None:
                pass
            else:
                statement.execute()

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'print' : 'PRINT',
   'and' : 'AND',
   'or' : 'OR',
   'not' : 'NOT',
   'in' : 'IN'
}


tokens = [
    'LBRACE', 'RBRACE','STRING','QUATION','LBRACKT','RBRACKT','ASSIGN',
    'LPAREN', 'RPAREN', 'SEMI',
    'NUMBER','POWER', 'MODULUS','FLOOR','BOOLEAN',
    'PLUS','MINUS','TIMES','DIVIDE','LESS','LEEEQUE','EUQAL',
    'NOTEQUAL','LARGE','LARGEEQUE','COMMA','VARIABLE','ID'
    ]+list(reserved.values())


# Tokens

t_LBRACKT  = r'\['
t_RBRACKT = r'\]'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
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

t_COMMA=r','
t_ASSIGN = r'\='



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


def t_ID(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    t.type = reserved.get(t.value,'ID')
    if t.value in reserved:
        return t
    else:
        t.value = VariableNode(t.value)
        return t

# def t_VARIABLE(t):
#     r'[A-Za-z][A-Za-z0-9_]*'
#     t.value = VariableNode(t.value)
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
    ('left','ASSIGN'),
    ('left','OR'),
    ('left','AND'),
    ('left','NOT'),
    ('left','LESS','LEEEQUE','EUQAL','NOTEQUAL','LARGE','LARGEEQUE'),
    ('left','IN'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','MODULUS','FLOOR'),
    ('left','LBRACKT'),
    ('right','POWER')
    )

def p_block1(t):
    """
    block : LBRACE RBRACE
    """
    t[0] = NoneNode()


def p_block(t):
    """
    block : LBRACE inbrace RBRACE
    """
    t[0] = t[2]


def p_inbrace(t):
    """
    inbrace : smt inbrace
    """
    t[0] = t[2]
    t[0].sl.insert(0,t[1])

def p_inbrace2(t):
    """
    inbrace : smt
    """
    t[0] = BraceNode(t[1])


def p_smt_empty(t):
    """
    smt : LBRACE RBRACE
    """
    t[0] = NoneNode()

def p_smt_emptyp1(t):
    """
    smt : block
    """
    t[0] = t[1]

def p_smt_cal(t):
    """
    smt : expression
    """
    t[0] = calculateNode(t[1])


def p_smt_assign1(t):
    """
    smt : expression LBRACKT factor RBRACKT ASSIGN expression SEMI
    """
    t[0] = assignNode1(t[1],t[3],t[6])

def p_smt_assign(t):
    """
    smt : factor ASSIGN expression SEMI
    """
    t[0] = assignNode(t[1],t[3])

def p_smt_ifelse(t):
    """
    smt : IF LPAREN expression RPAREN smt ELSE smt
    """
    t[0] = ifelseNode(t[3],t[5],t[7])

def p_smt_if(t):
    """
    smt : IF LPAREN expression RPAREN smt
    """
    t[0] = ifNode(t[3],t[5])

def p_smt_while(t):
    """
    smt : WHILE LPAREN expression RPAREN block
    """
    t[0] = whileNode(t[3],t[5])


def p_smt_print(t):
    """
    smt : PRINT LPAREN expression RPAREN SEMI
    """
    t[0] = PrintNode(t[3])

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
    
def p_expression_listElement(t):
    """
    expression : expression LBRACKT expression RBRACKT 
    """
    t[0] = ListNode(t[1],t[3])


def p_inblock2(t):
    """
    expression : LPAREN expression RPAREN
    """
    t[0] = t[2]

def p_expression_list1(t):
    """
    expression : LBRACKT RBRACKT 
    """
    t[0] = emptyListNode() 

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


def p_expression_single(t):
    '''expression : NOT expression
                  | MINUS expression'''
    t[0] = SingleNode(t[1], t[2])

# def p_expression_variable(t):
#     '''expression : VARIABLE'''
#     t[0] = returnVarNode(t[1])

def p_expression_factor(t):
    '''expression : factor'''
    t[0] = t[1]

def p_factor_number(t):
    'factor : NUMBER'
    t[0] = t[1]

def p_factor_boolean(t):
    'factor : BOOLEAN'
    t[0] = t[1]

def p_factor_string(t):
    'factor : STRING'
    t[0] = t[1]

def p_factor_variable(t):
    'factor : VARIABLE'
    t[0] = t[1]

def p_factor_id(t):
    'factor : ID'
    t[0] = t[1]

def p_error(t):
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
    code = ""
    for x in codes:
        code += x.strip('\n')
    try:
        # lex.input(code)
        # while True:   
        #    token = lex.token()
        #    if not token: break
        #    print(token)
        ast = yacc.parse(code)
        ast.execute()
    except Exception as e:
        if str(e)== "Syntax Error" :
            print("SYNTAX ERROR")
        else:
            print("SEMANTIC ERROR")


    


