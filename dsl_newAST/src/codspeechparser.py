# ----------------------------------------------------------------------
# codspeechparser.py
#
# A parser for Codspeech
# ----------------------------------------------------------------------
import ply.yacc

from codspeechlexer import CodspeechLexer
from plyparser      import PLYParser, Coord, ParseError

import ast
import sys
sys.path.insert(0,"../..")



class CodspeechParser(PLYParser):
    def __init__(self):
        """Create a new CodspeechParser.
        
        """
        self.cslex = CodspeechLexer(
            error_func = self._lex_error_func)
        self.cslex.build()
        self.tokens = self.cslex.tokens
        self.csparser = ply.yacc.yacc(
            module=self,
            start='entrypoint',
        )

        
    def parse(self, text, filename=''):
        """Parses Codspeech Code and returns an AST.

        Keyword arguments:
        text     -- A string containing the Codspeech code.
        filename -- Name of the file being parsed.

        """
        self.cslex.filename = filename
        self.cslex.reset_lineno()
        if not text or text.isspace():
            return []
        else:
            return self.csparser.parse(text, lexer=self.cslex)


    # --------------------------------------------------------------
    # PRIVATE
    # --------------------------------------------------------------
    def _lex_error_func(self, msg, line, column):
        self._parse_error(msg, self._coord(line, column))


    # --------------------------------------------------------------
    # Precedence and associativity of operators
    # --------------------------------------------------------------
    precedence = ()

    
    # --------------------------------------------------------------
    # Grammar productions
    # --------------------------------------------------------------
    def p_entrypoint(self, p):
        """
        entrypoint : opt_cr program
        """
        if len(p) == 3:
            p[0] = p[2]
        else:
            p[0] = p[1]

            
    def p_program(self, p):
        """
        program : import_stmt_list cr component_decl_list opt_cr
                | import_stmt_list empty opt_cr
                | component_decl_list opt_cr
                | empty
        """
        if len(p) == 5:
            p[0] = ast.Program(p[1],p[3])
        elif len(p) == 4:
            p[0] = ast.Program(p[1],None)
        elif len(p) == 3:
            p[0] = ast.Program([],p[3])
        else:
            p[0] = ast.Program([],None)


    def p_import_stmt_list(self, p):
        """
        import_stmt_list : import_stmt
                         | import_stmt_list cr import_stmt
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

            
    def p_import_stmt(self, p):
        """
        import_stmt : IMPORT package_path
        """
        p[0] = ast.Import(p[2])


    def p_package_path(self, p):
        """
        package_path : package_identifier
                     | package_path PERIOD package_identifier
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2] + p[3]


    def p_package_identifier(self, p):
        """
        package_identifier : ID
        """
        p[0] = p[1]


    # A list of components consists of either a single component or
    # several components separated by newlines.
    def p_component_decl_list(self, p) :
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
    def p_component_decl(self, p):
        """
        component_decl : COMPONENT component_header network_stmt
                       | COMPONENT component_header atom_stmt
        """
        p[0] = ast.Component(p[2],p[3])


    # A component header consists of the the name of the component, a
    # doctring and the i/o parameters.
    def p_component_header(self, p):
        """
        component_header : ident docstring cr in_params out_params
        """
        p[0] = ast.Header(p[1],p[4],p[5],p[2])


    # ------------------------------------------------------------------
    # parameter lists
    # ------------------------------------------------------------------
    # The in-parameters consists of either a non-empty list of parameters
    # or no parameters at all.
    def p_in_params(self, p):
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
    def p_out_params(self, p):
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
    def p_in_param_list(self, p):
        """
        in_param_list : in_param
                      | in_param_list comma_sep in_param
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_out_param_list(self, p):
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
    def p_no_params(self, p):
        """
        no_params : LPAREN opt_cr RPAREN
        """
        pass


    # A parameter is either just a type and an ident or extended with a
    # default value.
    def p_in_param(self, p):
        """
        in_param : type ident docstring
                 | OPTIONAL type ident docstring
                 | type ident DEFAULT constant docstring
        """
        if len(p) == 4:
            p[0] = ast.InParameter(p[2],p[1],p[3])
        elif len(p) == 5:
            p[0] = ast.InParameter(p[3],p[2],p[4],None,True)
        else:
            p[0] = ast.InParameter(p[2],p[1],p[5],p[4])


    def p_out_param(self, p):
        """
        out_param : type ident docstring
                  | type ident DEFAULT constant docstring
        """
        if len(p) == 4:
            p[0] = ast.OutParameter(p[2],p[1],p[3])
        else:
            p[0] = ast.InParameter(p[2],p[1],p[5],p[4])


    # ------------------------------------------------------------------
    # network statements
    # ------------------------------------------------------------------
    # A networks statement consists of either a network and a statement
    # block, or a network with an associated network controller and a
    # statement block.
    def p_network_stmt(self, p):
        """
        network_stmt : NETWORK stmt_block
                     | NETWORK opt_cr network_controller stmt_block
        """
        if len(p) == 3:
            p[0] = ast.Network(p[2])
        else:
            p[0] = ast.Network(p[4],p[3])


    # A network controller is a component and the controller alias?
    def p_network_controller(self, p):
        """
        network_controller : CONTROLLER ident ident
        """
        p[0] = ast.Controller(p[2],p[3])


    # ------------------------------------------------------------------
    # atom statement
    # ------------------------------------------------------------------
    # An atom consist of an atom option descrbing what the following atom
    # block contains.
    def p_atom_stmt(self, p):
        """
        atom_stmt : ATOM MODULE opt_cr lparen atom_conf_list rparen
        """
        p[0] = ast.Atom(p[2],p[5])


    def p_atom_conf_list(self, p):
        """
        atom_conf_list : atom_conf
                       | atom_conf_list comma_sep atom_conf
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_atom_conf(self, p):
        """
        atom_conf : sconst COLON sconst
        """
        p[0] = ast.AtomOption(p[1],p[3])


    # ------------------------------------------------------------------
    # statements
    # ------------------------------------------------------------------
    # A statement block contains a list of statements enclosed in braces.
    def p_stmt_block(self, p):
        """
        stmt_block : opt_cr lbrace stmt_list rbrace
                   | opt_cr stmt_block_empty
        """
        if len(p) == 5:
            p[0] = p[3]
        else:
            p[0] = []


    def p_stmt_block_emtpy(self, p):
        """
        stmt_block_empty : LBRACE opt_cr RBRACE
        """
        pass


    # A list of single statements on separate lines.
    def p_stmt_list(self, p):
        """
        stmt_list : stmt
                  | stmt_list cr stmt
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    # Statement types.
    def p_stmt(self, p):
        """
        stmt : connection
             | sass
             | expr
        """
        p[0] = p[1]


    # Connections.
    def p_connection(self, p):
        """
        connection : param_ref CONNECTION param_ref
        """
        p[0] = ast.Connection(p[1],p[3])


    # Assignment.
    def p_sass(self, p):
        """
        sass : ident EQUALS component_stmt
        """
        p[0] = ast.Assignment(p[1],p[3])


    # A component statement: comp_id (expr_0, ..., expr_n)
    def p_component_stmt(self, p):
        """
        component_stmt : ident lparen expr_list rparen
        """
        p[0] = ast.ComponentStmt(p[1],p[3])


    # ------------------------------------------------------------------
    # expressions
    # ------------------------------------------------------------------
    def p_expr(self, p):
        """
        expr : constant
             | ident
             | param_ref
        """
        p[0] = p[1]


    # Expression list: expr_0, ..., expr_n
    def p_expr_list(self, p):
        """
        expr_list : expr
                  | expr_list comma_sep expr
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    # Constants or literals.
    def p_constant(self, p):
        """
        constant : fconst
                 | iconst
                 | sconst
        """
        p[0] = p[1]


    def p_fconst(self, p):
        """
        fconst : FCONST
        """
        p[0] = ast.Const('FLOAT',p[1])


    def p_iconst(self, p):
        """
        iconst : ICONST
        """
        p[0] = ast.Const('INT',p[1])


    def p_sconst(self, p):
        """
        sconst : SCONST
        """
        p[0] = ast.Const('STRING',p[1])


    # Idents.
    def p_ident(self, p):
        """
        ident : ID
        """
        p[0] = ast.Ident(p[1],self._coord(p.lineno(1)))


    # A parameter reference references either the component it's stated
    # in, or a component from an earlier assignment.
    def p_param_ref(self, p):
        """
        param_ref : IN PERIOD ident
                  | OUT PERIOD ident
                  | ident PERIOD IN PERIOD ident
                  | ident PERIOD OUT PERIOD ident
                  | lparen component_stmt rparen PERIOD OUT PERIOD ident
        """
        if len(p) == 4:
            p[0] = ast.This(p[3],p[1])
        elif len(p) == 6:
            p[0] = ast.Other(p[5],p[3],p[1])
        else:
            p[0] = ast.Comp(p[7],p[5],p[2])


    # ------------------------------------------------------------------
    # types
    # ------------------------------------------------------------------
    # The different types of the language.
    def p_type(self, p):
        """
        type : FILE
             | FLOAT
             | INT
             | TYPE
        """
        p[0] = p[1]


    # ------------------------------------------------------------------
    # docstring
    # ------------------------------------------------------------------
    # Docstrings. Used for documentation.
    def p_docstring(self, p):
        """
        docstring : DOCSTRING empty
                  | empty
        """
        if len(p) == 3:
            p[0] = p[1]
        else:
            p[0] = None


    # ------------------------------------------------------------------
    # special productions
    # ------------------------------------------------------------------
    # A non-empty sequence of new lines.
    def p_cr(self, p):
        """
        cr : CR
           | cr CR
        """
        pass


    # A sequence of new lines which may be empty.
    def p_opt_cr(self, p):
        """
        opt_cr : cr
               | empty
        """
        pass


    # A left brace succeeded by optional new lines
    def p_lbrace(self, p):
        """
        lbrace : LBRACE opt_cr
        """
        pass

    # A right brace preceded by optional new lines.
    def p_rbrace(self, p):
        """
        rbrace : opt_cr RBRACE
        """
        pass


    # A left parenthesis succeeded by optional new lines.
    def p_lparen(self, p):
        """
        lparen : LPAREN opt_cr
        """
        pass


    # A right parenthesis preceded by opional new lines.
    def p_rparen(self, p):
        """
        rparen : opt_cr RPAREN
        """
        pass


    # An empty production.
    def p_empty(self, p):
        """
        empty :
        """
        p[0] = None


    # Comma separator
    def p_comma_sep(self, p):
        """
        comma_sep : opt_cr COMMA opt_cr
        """
        pass


    # ------------------------------------------------------------------
    # error handling
    # ------------------------------------------------------------------
    # Catches erroneous productions.
    def p_error(self, p):
        if p:
            self._parse_error(
                'before: %s' % p.value,
                self._coord(p.lineno))
        else:
            self._parse_error('At end of input', '')

    
    # ------------------------------------------------------------------
    # helper functions
    # ------------------------------------------------------------------
    def row_col(self, *args):
        if len(args) == 3:
            row, lexpos, lexdata = args
            col = self.find_column(lexdata,lexpos)
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


    def find_column(self, input, lexpos):
        last_cr = input.rfind('\n',0,lexpos)
        colno = (lexpos - last_cr) - 1
        return colno








        
    # --------------------------------------------------------------
    # test functions
    # --------------------------------------------------------------
def test(filepath):
    p = CodspeechParser()
    try:
        buffer = open(filepath)
    except IOError, e:
        raise e
    else:
        prog = buffer.read()
        return p.parse(prog, filepath)
        
