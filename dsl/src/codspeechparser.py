import sys
sys.path.insert(0,"../..")

import codspeechlexer
import ply.yacc as yacc

tokens = codspeechlexer.tokens

precedence = ()

names = {}

def p_program(p):
  'program : stmt_list'
  p[0] = p[1]

################################################################################
# Statements

def p_stmt(p):
  '''stmt : stmt_block
          | stmt_component
          | stmt_connect
          | stmt_assign'''
  p[0] = p[1]

def p_stmt_block(p):
  '''stmt_block : LBRACE stmt_list RBRACE
                | LBRACE RBRACE'''
  if len(p) == 4:
    p[0] = ['BLOCK',p[2]]
  else:
    p[0] = ['BLOCK',[]]

def p_stmt_list(p):
  '''stmt_list : stmt
               | stmt_list stmt'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = [p[2]] + p[1]

def p_stmt_import(p):
  'stmt_import : IMPORT expr_path'
  p[0] = ['IMPORT',p[2]]

def p_stmt_component(p):
  'stmt_component : COMPONENT expr_id expr_args expr_args stmt_block'
  p[0] = ['COMPONENT',p[2],p[3],p[4],p[5]]

def p_stmt_connect(p):
  'stmt_connect : expr_id CONNECTION expr_id'
  p[0] = ['CONNECT',p[1],p[3]]

def p_stmt_assign(p):
  'stmt_assign : expr_id EQUALS expr_idlist'
  p[0] = ['ASSIGN',p[1],p[3]]

################################################################################
# Expressions

#def p_expr(p):
#  'expr : expr_idlist'
#  p[0] = p[1]

#def p_expr_component(p):
#  'expr_component : expr_idlist'
#  p[0] = p[1]

def p_args(p):
  '''expr_args : IN  expr_decllist
               | OUT expr_decllist'''
  p[0] = [p[1],p[2]]

def p_expr_decllist(p):
  '''expr_decllist : expr_decl
                   | expr_decllist COMMA expr_decl'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = [p[3]] + p[1]

def p_expr_decl(p):
  '''expr_decl : type expr_id
               | type expr_id DEFAULT expr_const'''
  p[0] = [p[1],p[2]]
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
    p[0] = [p[3]] + p[1]  

def p_expr_idlist(p):
  '''expr_idlist : expr_id
                 | expr_idlist expr_id'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = [p[2]] + p[1]  

def p_expr_id(p):
  'expr_id : ID'
  p[0] = ['ID',p[1]]

#def p_expr_desc(p):
#  'expr_desc : DESCRIPTION'
#  p[0] = ['DESC',p[1]]

def p_type(p):
  '''type : FILE
          | FLOAT
          | INT'''
  p[0] = ['TYPE',p[1]]

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
  print(x + '\n')
  p = parse(x)
  print(p)
  return p

test()
