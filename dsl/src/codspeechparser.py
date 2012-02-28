import codspeechlexer
import ply.yacc as yacc

precedence = ()

names = {}


def p_component(p):
  '''statement : COMPONENT args args'''
  p[0] = ('COMPONENT',p[2],p[3])

def p_args(p):
  '''statement : IN  decl
               | OUT decl'''
  p[0] = ('args',p[1],p[2])

def p_decl(p):
  '''decl : type item COMMA decl
          | type item'''
  if len(p) == 5:
    p[0] = ('decl',p[1],p[2],p[4])
  else:
    p[0] = ('decl',p[1],p[2])

def p_item_id(p):
  '''expr : ID'''
  p[0] = ('ID',p[1])

def p_type(p):
  '''expr : FILE
          | FLOAT
          | INT'''
  p[0] = p[1]



#### Catastrophic error handler
def p_error(p):
    if not p:
        print "SYNTAX ERROR AT EOF"

parser = yacc.yacc()

def parse(data):
  parser.error = 0
  p = parser.parse(data)
  if parser.error: return None
  print(p)
  return p
