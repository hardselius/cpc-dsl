
# ------------------------------------------------------------------
# codspeechlexer.py
#
# A lexer for Codspeech
# ------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

import ply.lex as lex
from ply.lex import TOKEN

# Reserved words
reserved = {
    # Componet
    'Component' : 'COMPONENT',
    'in'        : 'IN',
    'out'       : 'OUT',
    'default'   : 'DEFAULT',

    # Function

    # Network

    # Types
    'File'      : 'FILE',
    'Float'     : 'FLOAT',
    'Int'       : 'INT'
    }

tokens = (
    # Literals
    # (identifier, integer constant, float constant, string constant)
    'ID', 'TYPEID', 'ICONST', 'FCONST', 'SCONST',

    # Operators
    # ()

    # Assignments
    # (=)
    'EQUALS',

    # Substitution :=
    'SUBSTITUTION',

    # Connection <-
    'CONNECTION',

    # Delimeters
    # ( ) [ ] { } , . ; : ::
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON', 'DOUBLECOLON'
    )

# Complex REs
digit      = r'([0-9])'
lowercase  = r'([a-z])'
uppercase  = r'([A-Z])'
nondigit   = r'([_A-Za-z])'
identifier = r'(' + lowercase + r'(' + digit + r'|' + nondigit + r')*)'


# Ignored characters
t_ignore = ' \t\x0c'

# Literals
@TOKEN(identifier)
def t_ID(t):
    t.type = reserved.get(t.value,"ID")
    return t

# Assignment operators
t_EQUALS       = r'='

# Substitution
t_SUBSTITUTION = r':='

# Connection
t_CONNECTION   = r'<-'

# Delimeters
t_LPAREN       = r'\('
t_RPAREN       = r'\)'
t_LBRACKET     = r'\['
t_RBRACKET     = r'\]'
t_LBRACE       = r'\{'
t_RBRACE       = r'\}'
t_COMMA        = r','
t_PERIOD       = r'\.'
t_SEMI         = r';'
t_COLON        = r':'
t_DOUBLECOLON  = r'::'

def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)




def test(s):
    lex.lex()
    lex.input(s)
    while 1:
        tok = lex.token()
        if not tok: break
        print tok


def t_error(t):
    print "Illegal character %s" % repr(t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
#if __name__ == "__main__":
#    lex.runmain(lexer)