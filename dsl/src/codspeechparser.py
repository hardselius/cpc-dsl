
# ----------------------------------------------------------------------
# codspeechparser.py
#
# A parser for Codspeech
# ----------------------------------------------------------------------


import sys
sys.path.insert(0,"../..")

import codspeechlexer as lex
import ply.yacc as yacc

tokens = lex.tokens

precedence = ()


# ----------------------------------------------------------------------
# Program
# ----------------------------------------------------------------------

def p_entrypoint(p):
  """
  entrypoint : opt_cr program
  """
  if len(p) == 3:
    p[0] = p[2]
  else:
    p[0] = p[1]


def p_program(p):
  """
  program : import_stmt_list cr component_decl_list opt_cr
          | import_stmt_list opt_cr
          | component_decl_list opt_cr
          | empty
  """
  if len(p) == 5:
    p[0] = ['PROGRAM',p[1],p[3]]
  elif len(p) == 3:
    p[0] = ['PROGRAM',p[1]]
  else:
    p[0] = []


# ----------------------------------------------------------------------
# import statements
# ----------------------------------------------------------------------

def p_import_stmt_list(p):
  """
  import_stmt_list : import_stmt
                   | import_stmt_list cr import_stmt
  """
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]


def p_import_stmt(p):
  """
  import_stmt : IMPORT package_path
  """
  p[0] = ['IMPORT', p[2]]


def p_package_path(p):
  """
  package_path : package_identifier
               | package_path PERIOD package_identifier
  """
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]


def p_package_identifier(p):
  """
  package_identifier : ID
  """
  p[0] = p[1]


# ----------------------------------------------------------------------
# Component declarations
# ----------------------------------------------------------------------

def p_component_decl_list(p) :
  """
  component_decl_list : component_decl
                      | component_decl_list cr component_decl
  """
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]


def p_component_decl(p):
  """
  component_decl : COMPONENT ident docstring in_params out_params network_stmt
                 | COMPONENT ident docstring in_params out_params atom_stmt
  """
  p[0] = ['COMPONENT',p[2],p[3],p[4],p[5],p[6]]


# ----------------------------------------------------------------------
# parameter lists
# ----------------------------------------------------------------------

def p_in_params(p):
  """
  in_params : IN lparen param_list rparen cr
            | IN no_params cr
  """
  if len(p) == 6:
    p[0] = p[3]
  else:
    p[0] = []


def p_out_params(p):
  """
  out_params : OUT lparen param_list rparen cr
             | OUT no_params cr
  """

  if len(p) == 6:
    p[0] = p[3]
  else:
    p[0] = []


def p_param_list(p):
  """
  param_list : param
             | param_list param_sep param
  """
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]


def p_no_params(p):
  """
  no_params : LPAREN opt_cr RPAREN
  """
  pass


def p_param(p):
  """
  param : type ident
        | type ident DEFAULT constant
  """
  if len(p) == 3:
    p[0] = [p[1],p[2]]
  else:
    p[0] = [p[1],p[2],'DEFAULT',p[4]]


def p_param_sep(p):
  """
  param_sep : opt_cr COMMA opt_cr
  """
  pass


# ----------------------------------------------------------------------
# network statements
# ----------------------------------------------------------------------

def p_network_stmt(p):
  """
  network_stmt : NETWORK stmt_block
               | NETWORK opt_cr network_controller stmt_block
  """
  if len(p) == 3:
    p[0] = ['NETWORK',[],p[2]]
  else:
    p[0] = ['NETWORK',p[3],p[4]]


def p_network_controller(p):
  """
  network_controller : CONTROLLER ident ident
  """
  p[0] = ['CONTROLLER',p[2],p[3]]


# ----------------------------------------------------------------------
# atom statement
# ----------------------------------------------------------------------

def p_atom_stmt(p):
  """
  atom_stmt : ATOM ATOMOPTION stmt_block
  """
  p[0] = ['ATOM',p[2],p[3]]


# ----------------------------------------------------------------------
# statements
# ----------------------------------------------------------------------

def p_stmt_block(p):
  """
  stmt_block : opt_cr lbrace stmt_list rbrace
             | opt_cr LBRACE opt_cr RBRACE
  """
  if len(p) == 5:
    p[0] = p[3]
  else:
    p[0] = []


# statement list
def p_stmt_list(p):
  """
  stmt_list : stmt
            | stmt_list stmt_sep stmt
  """
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]


# Statement
def p_stmt(p):
  """
  stmt : connection
       | sass
       | expr
  """
  p[0] = p[1]


def p_connection(p):
  """
  connection : ident CONNECTION ident
  """
  p[0] = ['CONNECTION',p[1],p[3]]


# statement assignment
def p_sass(p):
  """
  sass : ident EQUALS ident param_ref_list
  """
  p[0] = ['ASSIGNMENT',p[1],p[3],p[4]]



# ----------------------------------------------------------------------
# expressions
# ----------------------------------------------------------------------

def p_expr_list(p):
  """
  expr_list : expr
            | expr_list COMMA expr
  """
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]

def p_expr(p):
  """
  expr : constant
       | ident
       | param_ref
  """
  p[0] = p[1]


def p_constant(p):
  """
  constant : FCONST
           | ICONST
           | SCONST
  """
  p[0] = [p.type,p[1]]


def p_ident(p):
  """
  ident : ID
  """
  p[0] = ['IDENT',p[1],(row_col(p.lineno(1),p.lexpos(1),p.lexer.lexdata))]


def p_param_ref(p):
  """
  param_ref : IN PERIOD ident
            | ident PERIOD IN PERIOD ident
            | OUT PERIOD ident
            | ident PERIOD OUT PERIOD ident
  """
  if len(p) == 4:
    p[0] = [p[1],p[3]]
  else:
    p[0] = [p[1],p[3],p[5]]


def p_param_ref_list(p):
  """
  param_ref_list : param_ref
                 | param_ref_list COMMA param_ref
  """
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[1] + [p[3]]


# ----------------------------------------------------------------------
# types
# ----------------------------------------------------------------------

def p_type(p):
  """
  type : FILE
       | FLOAT
       | INT
       | TYPE
  """
  p[0] = p[1]


# ----------------------------------------------------------------------
# docstring
# ----------------------------------------------------------------------

def p_docstring(p):
  """
  docstring : DOCSTRING cr
            | empty
  """
  if len(p) == 3:
    p[0] = p[1]
  else:
    p[0] = []


# ----------------------------------------------------------------------
# special productions
# ----------------------------------------------------------------------

def p_cr(p):
  """
  cr : CR
     | cr CR
  """
  pass

def p_opt_cr(p):
  """
  opt_cr : cr
         | empty
  """
  pass

def p_stmt_sep(p):
  """
  stmt_sep : SEMI
                | cr
  """
  pass

def p_lbrace(p):
  """
  lbrace : LBRACE opt_cr
  """
  pass

def p_rbrace(p):
  """
  rbrace : opt_cr RBRACE
  """
  pass

def p_lparen(p):
  """
  lparen : LPAREN opt_cr
  """
  pass

def p_rparen(p):
  """
  rparen : opt_cr RPAREN
  """
  pass

def p_empty(p):
  """
  empty :
  """
  pass


# ----------------------------------------------------------------------
# error
# ----------------------------------------------------------------------

def p_error(p):
  if not p:
    print "SYNTAX ERROR AT EOF"
  else:
    syntaxerror(p)


# ----------------------------------------------------------------------
# lulz
# ----------------------------------------------------------------------

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
  #row, col =
  #cr = "(ln " + str(row) + "; col " + str(col) + ")" + "\t"
  print row_col(token), ("Syntax error at: '%s'" % token.value)






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

