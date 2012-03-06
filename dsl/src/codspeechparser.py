import sys
sys.path.insert(0,"../..")

import codspeechlexer
import ply.yacc as yacc

tokens = codspeechlexer.tokens

precedence = ()

################################################################################

def p_program(p):
  'program : stmt_list'
  p[0] = ['PROGRAM',p[1]]

def p_program_error(p):
  'program : error'
  p[0] = None
  p.parser.error = 1

################################################################################
# Statements

def p_stmt(p):
  '''stmt : stmt_block
          | stmt_component
          | stmt_connect
          | stmt_assign
          | stmt_import'''
  p[0] = p[1]

def p_stmt_block(p):
  '''stmt_block : LBRACE stmt_list RBRACE
                | LBRACE RBRACE'''
  if len(p) == 4:
    p[0] = p[2]
  else:
    p[0] = []

#def p_stmt_block_error1(p):
#  'stmt_block : LBRACE stmt_list'
#  print "SYNTAX ERROR[missing '}'] at line %s" % (p.lineno(1))
#  p.parser.error = 1

#def p_stmt_block_error2(p):
#  'stmt_block : stmt_list RBRACE'
#  print "SYNTAX ERROR[missing '{'] at line %s" % (p.lineno(1))
#  p.parser.error = 1

def p_stmt_list(p):
  '''stmt_list : stmt
               | stmt_list stmt'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[2]]

def p_stmt_import(p):
  'stmt_import : IMPORT expr_path'
  p[0] = ['IMPORT',p[2]]

def p_stmt_network(p):
  '''stmt_network : NETWORK stmt_block
                  | NETWORK stmt_controller stmt_block'''
  if len(p) == 3:
    p[0] = ['NETWORK',[],p[2]]
  else:
    p[0] = ['NETWORK',p[2],p[3]]

def p_stmt_controller(p):
  'stmt_controller : CONTROLLER expr_id expr_id'
  p[0] = ['CONTROLLER',p[2],p[3],p.lineno(1)]

def p_stmt_component(p):
  '''stmt_component : COMPONENT expr_id expr_doc expr_params_in \
                      expr_params_out stmt_network
                    | COMPONENT expr_id expr_doc expr_params_in \
                      expr_params_out stmt_atom'''
  p[0] = ['COMPONENT',p[2],p[3],p[4],p[5],p[6]]

def p_stmt_component_error(p):
  'stmt_component : COMPONENT expr_id expr_doc expr_params_in \
                    expr_params_out error'
  print "SYNTAX ERROR[network error] at line %s" % p.lineno(6)
  p.parse.error = 1


def p_stmt_atom(p):
  'stmt_atom : ATOM ATOMOPTION stmt_block'
  p[0] = ['ATOM',p[2],p[3]]

def p_stmt_connect(p):
  'stmt_connect : expr_id CONNECTION expr_id'
  p[0] = ['CONNECT',p[1],p[3],p.lineno(2)]

def p_stmt_assign(p):
  'stmt_assign : expr_id EQUALS expr_idlist'
  p[0] = ['ASSIGN',p[1],p[3],p.lineno(2)]

################################################################################
# Expressions

def p_params_in(p):
  '''expr_params_in : IN  LPAREN expr_decllist RPAREN
                    | IN  LPAREN RPAREN'''
  if len(p) == 5:
    p[0] = p[3]
  else:
    p[0] = []

def p_params_out(p):
  '''expr_params_out : OUT LPAREN expr_decllist RPAREN
                     | OUT LPAREN RPAREN'''
  if len(p) == 5:
    p[0] = p[3]
  else:
    p[0] = []

def p_expr_decllist(p):
  '''expr_decllist : expr_decl
                   | expr_decllist COMMA expr_decl'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]

def p_expr_decl(p):
  '''expr_decl : type ID
               | type ID DEFAULT expr_const'''
  p[0] = [p[1],p[2],p.lineno(2)]
  if len(p) == 5 : p[0].append(p[4])

def p_expr_const(p):
  '''expr_const : ICONST
                | FCONST
                | SCONST'''
  p[0] = p[1]

def p_expr_path(p):
  '''expr_path : expr_id
               | expr_path PERIOD expr_id'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]

def p_expr_idlist(p):
  '''expr_idlist : expr_id
                 | expr_idlist expr_id'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[2]]

def p_expr_id(p):
  'expr_id : ID'
  p[0] = p[1]

def p_expr_id_error(p):
  'expr_id : error'
  print "SYNTAX ERROR[invalid variable name] at line %s: %s" % (p.lineno(1),p[1].value)
  p.parser.error = 1

def p_expr_doc(p):
  '''expr_doc : DOCSTRING
               | '''
  if len(p) == 2:
    p[0] = ['DOC',p[1]]
  else:
    p[0] = []

def p_type(p):
  '''type : FILE
          | FLOAT
          | INT
          | NEWTYPE'''
  p[0] = p[1]

################################################################################

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

def test():
  f = open('test.cod')
  x = f.read()
  p = parse(x)
  return p
