
# ------------------------------------------------------------------
# codspeechparser.py
#
# A parser for Codspeech
# ------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

import codspeechlexer as lex
import ply.yacc as yacc

tokens = lex.tokens

precedence = ()

# ------------------------------------------------------------------
# Program
# ------------------------------------------------------------------

def p_program(p):
  '''program : import_statements component_declarations
             | import_statements
             | component_declarations
             | '''
  if len(p) == 3:
    p[0] = ['PROGRAM',p[1],p[2]]
  elif len(p) == 2:
    p[0] = ['PROGRAM',p[1]]
  else:
    p[0] = []

def p_program_error(p):
  'program : error'
  p[0] = None
  p.parser.error = 1




# ------------------------------------------------------------------
# import statements
# ------------------------------------------------------------------

def p_import_statements(p):
  '''import_statements : import_statement
                       | import_statements import_statements'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[2]]

def p_import_statement(p):
  'import_statement : IMPORT package_path'
  p[0] = ['IMPORT', p[2]]

def p_package_path(p):
  '''package_path : package_identifier
                  | package_path PERIOD package_identifier'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]

def p_package_identifier(p):
  'package_identifier : ID'
  p[0] = p[1]




# ------------------------------------------------------------------
# Component declarations
# ------------------------------------------------------------------

def p_component_declarations(p):
  '''component_declarations : component_declaration
                            | component_declarations component_declaration'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[2]]

def p_component_declaration(p):
  '''component_declaration : COMPONENT identifier docstring\
                             in_parameters \
                             out_parameters \
                             network_statement
                           | COMPONENT identifier docstring\
                             in_parameters \
                             out_parameters \
                             atom_statement'''
  p[0] = ['COMPONENT',p[2],p[3],p[4],p[5],p[6]]




# ------------------------------------------------------------------
# network statements
# ------------------------------------------------------------------

def p_network_statement(p):
  '''network_statement : NETWORK statement_block
                       | NETWORK network_controller statement_block'''
  if len(p) == 3:
    p[0] = ['NETWORK',[],p[2]]
  else:
    p[0] = ['NETWORK',p[2],p[3]]

def p_network_controller(p):
  'network_controller : CONTROLLER identifier identifier'
  p[0] = ['CONTROLLER',p[2],p[3]]




# ------------------------------------------------------------------
# atom statement
# ------------------------------------------------------------------

def p_atom_statement(p):
  'atom_statement : ATOM ATOMOPTION statement_block'
  p[0] = ['ATOM',p[2],p[3]]




# ------------------------------------------------------------------
# parameter lists
# ------------------------------------------------------------------

def p_in_parameters(p):
  '''in_parameters : IN LPAREN parameter_list RPAREN
                   | IN LPAREN RPAREN'''
  if len(p) == 5:
    p[0] = p[3]
  else:
    p[0] = []

def p_out_parameters(p):
  '''out_parameters : OUT LPAREN parameter_list RPAREN
                    | OUT LPAREN RPAREN'''
  if len(p) == 5:
    p[0] = p[3]
  else:
    p[0] = []

def p_parameter_list(p):
  '''parameter_list : parameter
                    | parameter_list COMMA parameter'''
  if len(p) == 4:
    p[0] = p[1] + [p[3]]
  else:
    p[0] = [p[1]]



def p_parameter(p):
  '''parameter : type identifier
               | type identifier DEFAULT constant'''
  if len(p) == 3:
    p[0] = [p[1],p[2]]
  else:
    p[0] = [p[1],p[2],'DEFAULT',p[4]]

#def p_parameter_error(p):
#  '''parameter : type error'''
#  print "Syntax error ", p.lineno(1)




# ------------------------------------------------------------------
# statements
# ------------------------------------------------------------------

def p_statement_block(p):
  '''statement_block : LBRACE statement_list RBRACE
                     | LBRACE RBRACE'''
  if len(p) == 4:
    p[0] = p[2]
  else:
    p[0] = []

def p_statement_list(p):
  '''statement_list : statement
                    | statement_list statement'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[2]]

def p_statement(p):
  '''statement : connection
               | expression'''
  p[0] = p[1]

def p_connection(p):
  'connection : identifier CONNECTION identifier'
  p[0] = ['CONNECTION',p[1],p[3]]




# ------------------------------------------------------------------
# expressions
# ------------------------------------------------------------------

def p_expression_list(p):
  '''expression_list : expression
                     | expression_list COMMA expression'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]

def p_expression(p):
  '''expression : constant
                | ident
                | assignment'''

  p[0] = p[1]

def p_constant(p):
  '''constant : FCONST
              | ICONST
              | SCONST'''
  p[0] = [p.type,p[1]]

def p_ident(p):
  'ident : ID'
  p[0] = ['IDENT',p[1]]

def p_assignment(p):
  'assignment : identifier EQUALS identifier expression_list'
  p[0] = ['ASSIGNMENT',p[1],p[3],p[4]]




# ------------------------------------------------------------------
# types
# ------------------------------------------------------------------

def p_type(p):
  '''type : FILE
          | FLOAT
          | INT
          | TYPE'''
  p[0] = p[1]


def p_type_error(p):
  'type : error'
  print col_row(p[1]), "syntax error:", p[1].value, "not a type"

# ------------------------------------------------------------------
# docstring
# ------------------------------------------------------------------

def p_docstring(p):
  '''docstring : DOCSTRING
               | '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = []




# ------------------------------------------------------------------
# identifiers
# ------------------------------------------------------------------

def p_identifier(p):
  'identifier : ID'
  p[0] = p[1]

def p_identifier_error(p):
  'identifier : error'
  print col_row(p[1]), "syntax error"

# ------------------------------------------------------------------
# lulz
# ------------------------------------------------------------------


def col_row(token):
  ln  = token.lineno
  col = lex.find_column(token.lexer.lexdata,token)
  return "[" + str(ln) + ":" + str(col) + "]" + "\t"



def p_error(p):
  if not p:
    print "SYNTAX ERROR AT EOF"

parser = yacc.yacc()

def parse(data):
  lex.lexer.lineno = 1
  parser.error = 0
  p = parser.parse(data)
  if parser.error: return None
  return p

def test():
  f = open('test.cod')
  x = f.read()
  p = parse(x)
  parser.restart()
  return p


















#def p_stmt(p):
#  '''stmt : stmt_block
#          | stmt_component
#          | stmt_connect
#          | stmt_assign
#          | stmt_import'''
#  p[0] = p[1]
#
#def p_stmt_block(p):
#  '''stmt_block : LBRACE stmt_list RBRACE
#                | LBRACE RBRACE'''
#  if len(p) == 4:
#    p[0] = p[2]
#  else:
#    p[0] = []

#def p_stmt_block_error1(p):
#  'stmt_block : LBRACE stmt_list'
#  print "SYNTAX ERROR[missing '}'] at line %s" % (p.lineno(1))
#  p.parser.error = 1

#def p_stmt_block_error2(p):
#  'stmt_block : stmt_list RBRACE'
#  print "SYNTAX ERROR[missing '{'] at line %s" % (p.lineno(1))
#  p.parser.error = 1

#def p_stmt_list(p):
#  '''stmt_list : stmt
#               | stmt_list stmt'''
#  if len(p) == 2:
#    p[0] = [p[1]]
#  else:
#    p[0] = p[1] + [p[2]]
#
#def p_stmt_import(p):
#  'stmt_import : IMPORT expr_path'
#  p[0] = ['IMPORT',p[2]]
#
#def p_stmt_network(p):
#  '''stmt_network : NETWORK stmt_block
#                  | NETWORK stmt_controller stmt_block'''
#  if len(p) == 3:
#    p[0] = ['NETWORK',[],p[2]]
#  else:
#    p[0] = ['NETWORK',p[2],p[3]]
#
#def p_stmt_controller(p):
#  'stmt_controller : CONTROLLER expr_id expr_id'
#  p[0] = ['CONTROLLER',p[2],p[3],p.lineno(1)]
#
#def p_stmt_component(p):
#  '''stmt_component : COMPONENT expr_id expr_doc expr_params_in \
#                      expr_params_out stmt_network
#                    | COMPONENT expr_id expr_doc expr_params_in \
#                      expr_params_out stmt_atom'''
#  p[0] = ['COMPONENT',p[2],p[3],p[4],p[5],p[6]]
#
#def p_stmt_component_error(p):
#  'stmt_component : COMPONENT expr_id expr_doc expr_params_in \
#                    expr_params_out error'
#  print "SYNTAX ERROR[network error] at line %s" % p.lineno(6)
#  p.parse.error = 1
#
#
#def p_stmt_atom(p):
#  'stmt_atom : ATOM ATOMOPTION stmt_block'
#  p[0] = ['ATOM',p[2],p[3]]

#def p_stmt_connect(p):
#  'stmt_connect : expr_id CONNECTION expr_id'
#  p[0] = ['CONNECT',p[1],p[3],p.lineno(2)]

#def p_stmt_assign(p):
#  'stmt_assign : expr_id EQUALS expr_idlist'
#  p[0] = ['ASSIGN',p[1],p[3],p.lineno(2)]
#



# ------------------------------------------------------------------
# Expressions
# ------------------------------------------------------------------

#def p_params_in(p):
#  '''expr_params_in : IN  LPAREN expr_decllist RPAREN
#                    | IN  LPAREN RPAREN'''
#  if len(p) == 5:
#    p[0] = p[3]
#  else:
#    p[0] = []
#
#def p_params_out(p):
#  '''expr_params_out : OUT LPAREN expr_decllist RPAREN
#                     | OUT LPAREN RPAREN'''
#  if len(p) == 5:
#    p[0] = p[3]
#  else:
#    p[0] = []

#def p_expr_decllist(p):
#  '''expr_decllist : expr_decl
#                   | expr_decllist COMMA expr_decl'''
#  if len(p) == 2:
#    p[0] = [p[1]]
#  else:
#    p[0] = p[1] + [p[3]]
#
#def p_expr_decl(p):
#  '''expr_decl : type ID
#               | type ID DEFAULT expr_const'''
#  p[0] = [p[1],p[2],p.lineno(2)]
#  if len(p) == 5 : p[0].append(p[4])

#def p_expr_const(p):
#  '''expr_const : ICONST
#                | FCONST
#                | SCONST'''
#  p[0] = p[1]

#def p_expr_path(p):
#  '''expr_path : expr_id
#               | expr_path PERIOD expr_id'''
#  if len(p) == 2:
#    p[0] = [p[1]]
#  else:
#    p[0] = p[1] + [p[3]]

#def p_expr_idlist(p):
#  '''expr_idlist : expr_id
#                 | expr_idlist expr_id'''
#  if len(p) == 2:
#    p[0] = [p[1]]
#  else:
#    p[0] = p[1] + [p[2]]

#def p_expr_id(p):
#  'expr_id : ID'
#  p[0] = p[1]

#def p_expr_id_error(p):
#  'expr_id : error'
#  print "SYNTAX ERROR[invalid variable name] at line %s: %s" % (p.lineno(1),p[1].value)
#  p.parser.error = 1

#def p_expr_doc(p):
#  '''expr_doc : DOCSTRING
#               | '''
#  if len(p) == 2:
#    p[0] = ['DOC',p[1]]
#  else:
#    p[0] = []

#def p_type(p):
#  '''type : FILE
#          | FLOAT
#          | INT
#          | NEWTYPE'''
#  p[0] = p[1]

################################################################################

#### Catastrophic error handler
