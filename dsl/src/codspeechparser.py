
# ----------------------------------------------------------------------
# codspeechparser.py
#
# A parser for Codspeech
# ----------------------------------------------------------------------


import sys
sys.path.insert(0,"../..")

import codspeechlexer as cslex
import ply.yacc as yacc

tokens = cslex.tokens

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
            | import_stmt_list empty opt_cr
            | component_decl_list opt_cr
            | empty
    """
    if len(p) == 5:
        p[0] = ['PROGRAM',p[1],p[3]]
    elif len(p) == 4:
        p[0] = ['PROGRAM',p[1],[]]
    elif len(p) == 3:
        p[0] = ['PROGRAM',[],p[1]]
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


# Import statements
def p_import_stmt(p):
    """
    import_stmt : IMPORT package_path
    """
    p[0] = ['IMPORT',p[2]]


def p_package_path(p):
    """
    package_path : package_identifier
                 | package_path PERIOD package_identifier
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2] + p[3]


def p_package_identifier(p):
    """
    package_identifier : ID
    """
    p[0] = p[1]


# ----------------------------------------------------------------------
# Component declarations
# ----------------------------------------------------------------------


# A list of components consists of either a single component or
# several components separated by newlines.
def p_component_decl_list(p) :
    """
    component_decl_list : component_decl
                        | component_decl_list cr component_decl
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# A component declaratation consists of the component header and
# either a network statement or an atom statement.
def p_component_decl(p):
    """
    component_decl : COMPONENT component_header network_stmt
                   | COMPONENT component_header atom_stmt
    """
    p[0] = ['COMPONENT'] + p[2] + [p[3]]


# A component header consists of the the name of the component, a
# doctring and the i/o parameters.
def p_component_header(p):
    """
    component_header : ident docstring cr in_params out_params
    """
    p[0] = [p[1],p[2],p[4],p[5]]


# ----------------------------------------------------------------------
# parameter lists
# ----------------------------------------------------------------------


# The in-parameters consists of either a non-empty list of parameters
# or no parameters at all.
def p_in_params(p):
    """
    in_params : IN lparen in_param_list rparen cr
              | IN no_params cr
    """
    if len(p) == 6:
        p[0] = p[3]
    else:
        p[0] = []


# The otu-parameters consists of either a non-empty list of parameters
# or no parameters at all.
def p_out_params(p):
    """
    out_params : OUT lparen out_param_list rparen cr
               | OUT no_params cr
    """
    if len(p) == 6:
        p[0] = p[3]
    else:
        p[0] = []


# Either a single parameter or a list of parameters separated by ','
# and possibly on separate lines.
def p_in_param_list(p):
    """
    in_param_list : in_param
                  | in_param_list comma_sep in_param
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_out_param_list(p):
    """
    out_param_list : out_param
                   | out_param_list comma_sep out_param
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# An empty parenthesis. The left and right parenthesis may be on
# different lines.
def p_no_params(p):
    """
    no_params : LPAREN opt_cr RPAREN
    """
    pass


# A parameter is either just a type and an ident or extended with a
# default value.
def p_in_param(p):
    """
    in_param : type ident docstring
             | OPTIONAL type ident docstring
             | type ident DEFAULT constant docstring
    """
    if len(p) == 4:
        p[0] = [p[1],p[2],p[3]]
    elif len(p) == 5:
        p[0] = [p[2],p[3],'OPTIONAL',p[4]]
    else:
        p[0] = [p[1],p[2],'DEFAULT',p[4],p[5]]


def p_out_param(p):
    """
    out_param : type ident docstring
              | type ident DEFAULT constant docstring
    """
    if len(p) == 4:
        p[0] = [p[1],p[2],p[3]]
    else:
        p[0] = [p[1],p[2],'DEFAULT',p[4],p[5]]


# ----------------------------------------------------------------------
# network statements
# ----------------------------------------------------------------------


# A networks statement consists of either a network and a statement
# block, or a network with an associated network controller and a
# statement block.
def p_network_stmt(p):
    """
    network_stmt : NETWORK stmt_block
                 | NETWORK opt_cr network_controller stmt_block
    """
    if len(p) == 3:
        p[0] = ['NETWORK',[],p[2]]
    else:
        p[0] = ['NETWORK',p[3],p[4]]


# A network controller is a component and the controller alias?
def p_network_controller(p):
    """
    network_controller : CONTROLLER ident ident
    """
    p[0] = ['CONTROLLER',p[2],p[3]]


# ----------------------------------------------------------------------
# atom statement
# ----------------------------------------------------------------------


# An atom consist of an atom option descrbing what the following atom
# block contains.
def p_atom_stmt(p):
    """
    atom_stmt : ATOM MODULE opt_cr lparen atom_conf_list rparen
    """
    p[0] = ['ATOM',p[2],p[5]]


def p_atom_conf_list(p):
    """
    atom_conf_list : atom_conf
                   | atom_conf_list comma_sep atom_conf
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_atom_conf(p):
    """
    atom_conf : sconst COLON sconst
    """
    p[0] = [p[1],p[3]]



# ----------------------------------------------------------------------
# statements
# ----------------------------------------------------------------------


# A statement block contains a list of statements enclosed in braces.
def p_stmt_block(p):
    """
    stmt_block : opt_cr lbrace stmt_list rbrace
               | opt_cr stmt_block_empty
    """
    if len(p) == 5:
        p[0] = p[3]
    else:
        p[0] = []

def p_stmt_block_emtpy(p):
    """
    stmt_block_empty : LBRACE opt_cr RBRACE
    """
    pass


# A list of single statements on separate lines.
def p_stmt_list(p):
    """
    stmt_list : stmt
              | stmt_list cr stmt
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# Statement types.
def p_stmt(p):
    """
    stmt : connection
         | sass
         | expr
    """
    p[0] = p[1]


# Connections.
def p_connection(p):
    """
    connection : param_ref CONNECTION param_ref
    """
    p[0] = ['CONNECTION',p[1],p[3]]


# Assignment.
def p_sass(p):
    """
    sass : ident EQUALS component_stmt
    """
    p[0] = ['ASSIGNMENT',p[1],p[3]]


# A component statement: comp_id (expr_0, ..., expr_n)
def p_component_stmt(p):
    """
    component_stmt : ident lparen expr_list rparen
    """
    p[0] = [p[1],p[3]]


# ----------------------------------------------------------------------
# expressions
# ----------------------------------------------------------------------


def p_expr(p):
    """
    expr : constant
         | ident
         | param_ref
    """
    p[0] = p[1]


# Expression list: expr_0, ..., expr_n
def p_expr_list(p):
    """
    expr_list : expr
              | expr_list comma_sep expr
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# Constants or literals.
def p_constant(p):
    """
    constant : fconst
             | iconst
             | sconst
    """
    p[0] = p[1]
    
    
def p_fconst(p):
    """
    fconst : FCONST
    """
    p[0] = ['FLOAT',p[1]]


def p_iconst(p):
    """
    iconst : ICONST
    """
    p[0] = ['INT',p[1]]


def p_sconst(p):
    """
    sconst : SCONST
    """
    p[0] = ['STRING',p[1]]


# Idents.
def p_ident(p):
    """
    ident : ID
    """
    p[0] = ['IDENT',p[1],(row_col(p.lineno(1),p.lexpos(1),p.lexer.lexdata))]


# A parameter reference references either the component it's stated
# in, or a component from an earlier assignment.
def p_param_ref(p):
    """
    param_ref : IN PERIOD ident
              | OUT PERIOD ident
              | ident PERIOD IN PERIOD ident
              | ident PERIOD OUT PERIOD ident
              | lparen component_stmt rparen PERIOD OUT PERIOD ident
    """
    if len(p) == 4:
        p[0] = ['THIS',p[1],p[3]]
    elif len(p) == 6:
        p[0] = ['OTHER',p[1],p[3],p[5]]
    else:
        p[0] = ['COMP',p[2],p[5],p[7]]


# ----------------------------------------------------------------------
# types
# ----------------------------------------------------------------------


# The different types of the language.
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


# Docstrings. Used for documentation.
def p_docstring(p):
    """
    docstring : DOCSTRING empty
              | empty
    """
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = []


# ----------------------------------------------------------------------
# special productions
# ----------------------------------------------------------------------


# A non-empty sequence of new lines.
def p_cr(p):
    """
    cr : CR
       | cr CR
    """
    pass


# A sequence of new lines which may be empty.
def p_opt_cr(p):
    """
    opt_cr : cr
           | empty
    """
    pass


# A left brace succeeded by optional new lines
def p_lbrace(p):
    """
    lbrace : LBRACE opt_cr
    """
    pass

# A right brace preceded by optional new lines.
def p_rbrace(p):
    """
    rbrace : opt_cr RBRACE
    """
    pass


# A left parenthesis succeeded by optional new lines.
def p_lparen(p):
    """
    lparen : LPAREN opt_cr
    """
    pass


# A right parenthesis preceded by opional new lines.
def p_rparen(p):
    """
    rparen : opt_cr RPAREN
    """
    pass


# An empty production.
def p_empty(p):
    """
    empty :
    """
    pass


# Comma separator
def p_comma_sep(p):
    """
    comma_sep : opt_cr COMMA opt_cr
    """
    pass


# ----------------------------------------------------------------------
# error
# ----------------------------------------------------------------------


# Catches erroneous productions.
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


lexer = cslex.lex.lex()
parser = yacc.yacc()

def parse(data):
    lexer.lineno = 1
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

