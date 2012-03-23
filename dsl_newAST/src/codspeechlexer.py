# ------------------------------------------------------------------
# codspeechlexer.py
#
# A lexer for Codspeech
# ------------------------------------------------------------------

import re
import sys


import ply.lex as lex
from   ply.lex import TOKEN

sys.path.insert(0,"../..")


class CodspeechLexer(object):
    """A lexer for the Codspeech Copernicus Domain Specific
       Language.

    """
    def __init__(self, error_func):
        """Create a new Lexer.

        Keyword arguments:
        error_func -- An error function. Will be called with and error
            message, line and column as arguments, in case of an error
            during lexing.

        """
        self.error_func = error_func

        
    def build(self,**kwargs):
        """Builds the lexer."""
        self.lexer = lex.lex(module=self, **kwargs)

        
    def reset_lineno(self):
        """Reset the internal line-number counter of the lexer."""
        self.lexer.lineno = 1

        
    def input(self, text):
        self.lexer.input(text)

        
    def token(self):
        g = self.lexer.token()
        return g

        
    ######################--   PRIVATE   --######################

    # --------------------------------------------------------------
    # Internal auxiliary methods
    # --------------------------------------------------------------
    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
        self.lexer.skip(1)

        
    def _find_tok_column(self, token):
        i = token.lexpos
        while i > 0:
            if self.lexer.lexdata[i] == '\n': break
            return (token.lexpos - i) + 1

            
    def _make_tok_location(self, token):
        return (token.lineno, self._find_tok_column(token))

        
    # --------------------------------------------------------------
    # reserved keywords
    # --------------------------------------------------------------
    keyword_map = {
        # Module stuff
        'import'    : 'IMPORT',

        # Component, Controller, Network, Atom, NewType
        'Component'  : 'COMPONENT',
        'Controller' : 'CONTROLLER',
        'Network'    : 'NETWORK',
        'Atom'       : 'ATOM',
        'in'         : 'IN',
        'out'        : 'OUT',
        'default'    : 'DEFAULT',
        'NewType'    : 'NEWTYPE',
        
        # Types
        'File'      : 'FILE',
        'Float'     : 'FLOAT',
        'Int'       : 'INT',}


    # --------------------------------------------------------------
    # tokens
    # --------------------------------------------------------------
    tokens = [
        # Literals: identifier, type, integer constant, float
        # constant, string constant
        'ID', 'TYPE', 'ICONST', 'FCONST', 'SCONST', 'DOCSTRING',

        # Assignments: = :
        'EQUALS', 'COLON',

        # Connection: <-
        'CONNECTION',

        # Delimeters: ( ) { } , .
        'LPAREN', 'RPAREN',
        'LBRACE', 'RBRACE',
        'COMMA', 'PERIOD',

        # Other:
        'CR', 'MODULE', 'OPTIONAL'
    ] + keyword_map.values()


    # --------------------------------------------------------------
    # regular expressions for use in tokens
    # --------------------------------------------------------------
    digits      = r'([0-9])'
    lowercase   = r'([a-z])'
    uppercase   = r'([A-Z])'
    letters     = r'([A-Za-z])'
    nondigit    = r'([_A-Za-z])'
    string      = r'([^\\\n]|(\\.))*?'
    ident       = r'(' + lowercase + r'(' + digits + r'|' + nondigit + r')*)'
    typeident   = r'(' + uppercase + r'(' + digits + r'|' + nondigit + r')*)'
    litint      = r'\d+'
    litfloat    = r'((\d+)(\.\d+)(e(\+|-)?(\d+))?)'
    litstring   = r'\"' + string + r'\"'
    description = r'(\{-)' + string + r'(-\})'
    modulename  = r'(' + nondigit + r'(.' + nondigit + r')*' +  r')'
    atommodule  = r'<( )*(?P<opt>' + modulename + r'+)( )*>'
    docstring   = r'(\'\'\')(.|\n)*?(\'\'\')'


    # --------------------------------------------------------------
    # token rules
    # --------------------------------------------------------------
    t_ignore = ' \t\x0c'

    
    @TOKEN(ident)
    def t_ID(self, t):
        t.type = self.keyword_map.get(t.value,"ID")
        return t


    @TOKEN(typeident)
    def t_TYPE(self, t):
        t.type = self.keyword_map.get(t.value,"TYPE")
        return t


    @TOKEN(litfloat)
    def t_FCONST(self, t):
        t.value = float(t.value)
        return t

    
    @TOKEN(litint)
    def t_ICONST(self, t):
        t.value = int(t.value)
        return t

    
    @TOKEN(litstring)
    def t_SCONST(self, t):
        return t


    @TOKEN(modulename)
    def t_MODULE(self, t):
        return t

    
    t_EQUALS     = r'='
    t_COLON      = r':'
    t_CONNECTION = r'<-'
    t_LPAREN     = r'\('
    t_RPAREN     = r'\)'
    t_LBRACE     = r'\{'
    t_RBRACE     = r'\}'
    t_COMMA      = r','
    t_PERIOD     = r'\.'
    t_OPTIONAL   = r'\?'

    
    @TOKEN(atommodule)
    def t_atommodule(self, t):
        t.type = 'MODULE'
        t.value = re.search(self.atommodule, t.value).group('opt')
        return t

    
    # multline comments (/# comment #/)
    def t_comment(self, t):
        r'/\#(.|\n)*?\#/'
        t.type = 'COMMENT'
        t.lexer.lineno += t.value.count('\n')
        pass

    
    # single line comment (# comment)
    def t_comment2(self, t):
        r'\#[^\\\n]*'
        t.type = 'COMMENT'
        pass

    
    # new line
    def t_CR(self, t):
        r'\n'
        t.lexer.lineno += len(t.value)
        return t


    # docstrings '''docstring'''
    @TOKEN(docstring)
    def t_docstring(self, t):
        t.type = 'DOCSTRING'
        t.lexer.lineno += t.value.count('\n')
        t.value = re.sub(r'\n( )*','\n',t.value)
        t.value = re.sub(r'(\'\'\')','',t.value)
        return t

        
    def t_error(self, t):
        msg = "Illegal character %s" % repr(t.value[0])
        self._error(msg,t)



    # test the lexer
    def test(self,data):
        self.input(data)
        while True:
            tok = self.token()
            if not tok: break
            print tok

