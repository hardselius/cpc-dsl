
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
  '''component_declaration : COMPONENT ident docstring\
                             in_parameters \
                             out_parameters \
                             network_statement
                           | COMPONENT ident docstring\
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
  'network_controller : CONTROLLER ident ident'
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
  '''parameter : type ident
               | type ident DEFAULT constant'''
  if len(p) == 3:
    p[0] = [p[1],p[2]]
  else:
    p[0] = [p[1],p[2],'DEFAULT',p[4]]


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
  'connection : ident CONNECTION ident'
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
  p[0] = ['IDENT',p[1],(row_col(p.lineno(1),p.lexpos(1),p.lexer.lexdata))]

def p_assignment(p):
  'assignment : ident EQUALS ident expression_list'
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
# error
# ------------------------------------------------------------------

def p_error(p):
  if not p:
    print "SYNTAX ERROR AT EOF"
  else:
    syntaxerror(p)


# ------------------------------------------------------------------
# lulz
# ------------------------------------------------------------------

def row_col(*args):
  if len(args) == 3:
    row, lexpos, lexdata = args
    col = find_column(lexdata,lexpos)
  elif len(args) == 1:
    t, = args
    if not t:
      return None
    else:
      row = t.lineno
      col = find_column(t.lexer.lexdata,t.lexpos)
  else:
    return None
  return (row,col)

def find_column(input,lexpos):
    last_cr = input.rfind('\n',0,lexpos)
    colno = (lexpos - last_cr) - 1
    return colno

def syntaxerror(token):
  row, col = row_col(token)
  cr = "(ln " + str(row) + "; col " + str(col) + ")" + "\t"
  print cr, ("Syntax error at: '%s'" % token.value)






parser = yacc.yacc()

def parse(data):
  lex.lexer.lineno = 1
  parser.error = 0
  p = parser.parse(data)
  if parser.error: return None
  return p

def test():
  f = open('../examples/example1.cod')
  x = f.read()
  p = parse(x)
  parser.restart()
  return p

