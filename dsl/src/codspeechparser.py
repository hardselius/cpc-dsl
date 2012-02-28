import codspeechlexer
import ply.yacc as yacc

tokens = codspeechlexer.tokens

precedence = ()

names = {}


def p_statement_block(p):
  'statement : LBRACE statement RBRACE'
  p[0] = ['BLOCK',p[2]]

def p_component(p):
  'statement : COMPONENT id args args'
  p[0] = ['COMPONENT',p[2],p[3],p[4]]

def p_args(p):
  '''args : IN  decllist
          | OUT decllist'''
  p[0] = [p[1],p[2]]

def p_decllist(p):
  '''decllist : decl
              | decllist COMMA decl'''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = ['decllist',p[3],p[1]]

def p_decl(p):
  '''decl : type id
          | type id DEFAULT const'''
  p[0] = ['decl',p[1],p[2]]
  if len(p) == 5 : p[0].append(p[4])

def p_const(p):
  '''const : ICONST
           | FCONST
           | SCONST'''
  p[0] = p[1]
  


def p_id(p):
  'id : ID'
  p[0] = ['ID',p[1]]

def p_type(p):
  '''type : FILE
          | FLOAT
          | INT'''
  p[0] = ['TYPE',p[1]]



#### Catastrophic error handler
def p_error(p):
    if not p:
        print "SYNTAX ERROR AT EOF"

parser = yacc.yacc()

def parse(data):
  parser.error = 0
  p = parser.parse(data)
  if parser.error: return None
  return p
