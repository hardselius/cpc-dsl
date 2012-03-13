import sys
sys.path.insert(0,"../..")

import codspeechlexer  as cslex
import codspeechparser as csparse


lexer  = cslex.lex.lex(module=cslex)
parser = csparse.yacc.yacc(module=csparse)

def get_tokens(path):
    f = open(path)
    s = f.read()
    lexer.lineno = 1
    lexer.input(s)
    while 1:
        t = lexer.token()
        if not t:
            break
        print t

def get_ast(path):
    f = open(path)
    s = f.read()
    lexer.lineno = 1
    parser.error = 0
    p = parser.parse(s)
    if parser.error:
        return None
    return p
