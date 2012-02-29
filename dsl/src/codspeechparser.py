import codspeechlexer
import ply.yacc as yacc

tokens = codspeechlexer.tokens

precedence = ()

names = {}

################################################################################
# Statements

def p_statement(p):
  '''statement : statement_block
               | statement_list
               | statement_component'''
  p[0] = p[1]

def p_statement_block_1(p):
  'statement_block : LBRACE statement_list RBRACE'
  p[0] = ['BLOCK',p[2]]

def p_statement_block_2(p):
  'statement_block : LBRACE RBRACE'
  p[0] = ['BLOCK',[]]

def p_statement_list(p):
  'statement_list : statement'
  p[0] = [p[1]]

#def p_statement_list(p):
#  '''statement_list : statement
#                    | statement_list statement'''
#  if len(p) == 2:
#    p[0] = [p[1]]
#  else:
#    p[0] = [p[2]] + p[1]

def p_statement_component(p):
  'statement_component : COMPONENT ID args args statement_block'
  p[0] = ['COMPONENT',p[2],p[3],p[4],p[5]]

################################################################################

def p_args(p):
  '''args : IN  decllist
          | OUT decllist'''
  p[0] = [p[1],p[2]]

def p_decllist(p):
  '''decllist : decl
              | decllist COMMA decl'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = [p[3]] + p[1]

def p_decl(p):
  '''decl : type id
          | type id DEFAULT const'''
  p[0] = [p[1],p[2]]
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

def parse():
  f = open('test.cod')
  parser.error = 0
  p = parser.parse(f.read())
  if parser.error: return None
  return p
