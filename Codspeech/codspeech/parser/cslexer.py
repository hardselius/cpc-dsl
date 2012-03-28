# ------------------------------------------------------------------
# Codspeech/codspeech/parser: cslexer.py
#
# A lexer for Codspeech
# ------------------------------------------------------------------

import re
from ..ply     import lex
from ..ply.lex import TOKEN


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
        self.lexer = None
        
        
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
        'CR', 'ATOMTYPE', 'OPTIONAL'
    ] + keyword_map.values()


    # --------------------------------------------------------------
    # regular expressions for use in tokens
    # --------------------------------------------------------------

    # character groups
    nondigit     = r'[_A-Za-z]'
    lowercase    = r'[a-z]'
    uppercase    = r'[A-Z]'

    # atoms
    atomtypechar = r'(' + lowercase + r'|' + r'-' + ')'
    atomtype     = r'<( )*(?P<opt>' + atomtypechar + r'+)( )*>'

    # comments and docstring
    commentblock = r'/\#(.|\n)*?\#/'
    commentline  = r'\#[^\\\n]*'
    docstring    = r'(\'\'\')(.|\n)*?(\'\'\')'
    
    # idents
    identchar    = r'[_A-Za-z0-9]'
    identvar     = r'(' + lowercase + r'(' + identchar + r')*)'
    identtype    = r'(' + uppercase + r'(' + identchar + r')*)'

    # literals
    litfloat     = r'((\d+)(\.\d+)(e(\+|-)?(\d+))?)'
    litint       = r'\d+'
    litstring    = r'\"([^\\\n]|(\\.))*?\"'

    # modulename
    modulename   = r'(' + nondigit + r'(.' + nondigit + r')*' +  r')'

    
    # --------------------------------------------------------------
    # token rules
    # --------------------------------------------------------------
    t_ignore = ' \t\x0c'

    
    @TOKEN(identvar)
    def t_ID(self, t):
        t.type = self.keyword_map.get(t.value,"ID")
        return t


    @TOKEN(identtype)
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
        t.value = t.value.lstrip('"').rstrip('"')
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

    
    @TOKEN(atomtype)
    def t_atomtype(self, t):
        t.type = 'ATOMTYPE'
        t.value = re.search(self.atomtype, t.value).group('opt')
        return t

    
    # multline comments (/# comment #/)
    @TOKEN(commentblock)
    def t_commentblock(self, t):
        t.type = 'COMMENT'
        t.lexer.lineno += t.value.count('\n')
        pass

    
    # single line comment (# comment)
    @TOKEN(commentline)
    def t_commentline(self, t):
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

