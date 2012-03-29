# ----------------------------------------------------------------------
# Codspeech/codspeech/parser: csparser.py
#
# A parser for Codspeech
# ----------------------------------------------------------------------

from ..ply      import yacc
from ..ast      import csast
from .cslexer   import CodspeechLexer
from .plyparser import PLYParser, Coord, ParseError


class CodspeechParser(PLYParser):
    def __init__(self):
        """Create a new CodspeechParser.
        
        """
        self.cslex = CodspeechLexer(
            error_func = self._lex_error_func)
        self.cslex.build()
        self.tokens = self.cslex.tokens
        self.csparser = yacc.yacc(
            module=self,
            start='entrypoint',
        )
        self.dim = ''

        
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


    # ------------------------------------------------------ PRIVATE
    # Internal auxiliary methods
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
                   | empty
        """
        if len(p) == 3:
            p[0] = p[2]
        else:
            p[0] = p[1]


    def p_program(self,p):
        """
        program : top_def_list opt_cr
        """
        p[0] = csast.Program(p[1])


    def p_top_def_list(self, p):
        """
        top_def_list : top_def
                     | top_def_list cr top_def
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_top_def(self, p):
        """
        top_def : import_stmt
                | newtype_decl
                | atom_decl
                | network_decl
        """
        p[0] = p[1]


    # --------------------------------------------------------------
    # Import Statement
    # --------------------------------------------------------------
    def p_import_stmt(self, p):
        """
        import_stmt : IMPORT package_path
        """
        p[0] = csast.Import(p[2])


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
        package_identifier : IDENT
        """
        p[0] = p[1]


    # --------------------------------------------------------------
    # Newtype
    # --------------------------------------------------------------
    # A NewType statement consists of a new type name, documentation
    # and a list of type declaratins
    def p_newtype_decl(self,p):
        '''
        newtype_decl : TYPE type docstring cr lparen type_decl_list rparen
        '''
        p[0] = csast.Newtype(
            type     = p[2],
            doc      = p[3],
            typedecl = p[6])


    def p_type_decl_list(self, p):
        """
        type_decl_list : type_decl
                       | type_decl_list comma_sep type_decl
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_type_decl(self, p):
        """
        type_decl : type COLON ident
        """
        p[0] = csast.TypeDecl(p[1],p[3])


    # --------------------------------------------------------------
    # Atom Declaration
    # --------------------------------------------------------------
    def p_atom_decl(self, p):
        """
        atom_decl : ATOM atomtype header optionblock
        """
        p[0] = csast.Atom(
            atomtype    = p[2],
            header      = p[3],
            optionblock = p[4])


    def p_atomtype(self, p):
        """
        atomtype : ATOMTYPE
        """
        p[0] = csast.AtomType(
            type = p[1])

    def p_optionblock(self, p):
        """
        optionblock : OPTIONS opt_cr lparen atom_option_list rparen
        """
        p[0] = csast.Optionblock(
            options = p[4])


    def p_atom_option_list(self, p):
        """
        atom_option_list : atom_option
                         | atom_option_list comma_sep atom_option
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_atom_option(self, p):
        """
        atom_option : sconst COLON sconst
        """
        p[0] = csast.AtomOption(
            option = p[1].value,
            value  = p[3].value)


    # --------------------------------------------------------------
    # Network Declaration
    # --------------------------------------------------------------
    def p_network_decl(self, p):
        """
        network_decl : NETWORK header networkblock
        """
        p[0] = csast.Network(
            header       = p[2],
            networkblock = p[3])


    def p_networkblock(self, p):
        """
        networkblock : stmt_block
        """
        p[0] = csast.Networkblock(
            stmts = p[1])

        
    # ------------------------------------------------------------------
    # Atom and Network Header
    # ------------------------------------------------------------------
    def p_header(self, p):
        """
        header : ident docstring cr inputs outputs
        """
        p[0] = csast.Header(
            ident   = p[1],
            doc     = p[2],
            inputs  = p[4],
            outputs = p[5])


    def p_inputs(self, p):
        """
        inputs : IN lparen input_list rparen cr
               | IN no_params cr
        """
        if len(p) == 6:
            p[0] = p[3]
        else:
            p[0] = []


    def p_outputs(self, p):
        """
        outputs : OUT lparen output_list rparen cr
                | OUT no_params cr
        """
        if len(p) == 6:
            p[0] = p[3]
        else:
            p[0] = []


    def p_input_list(self, p):
        """
        input_list : input
                   | input_list comma_sep input
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_output_list(self, p):
        """
        output_list : output
                    | output_list comma_sep output
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


    def p_no_params(self, p):
        """
        no_params : LPAREN opt_cr RPAREN
        """
        pass


    def p_input(self, p):
        """
        input : type ident docstring
              | OPTIONAL type ident docstring
              | type ident DEFAULT constant docstring
        """
        if len(p) == 4:
            p[0] = csast.InParameter(
                type  = p[1],
                ident = p[2],
                doc   = p[3])
        elif len(p) == 5:
            p[0] = csast.InParameter(
                type     = p[2],
                ident    = p[3],
                doc      = p[4],
                optional = True)
        else:
            p[0] = csast.InParameter(
                type    = p[1],
                ident   = p[2],
                doc     = p[5],
                default = p[4])


    def p_output(self, p):
        """
        output : type ident docstring
               | type ident DEFAULT constant docstring
        """
        if len(p) == 4:
            p[0] = csast.OutParameter(
                type  = p[1],
                ident = p[2],
                doc   = p[3])
        else:
            p[0] = csast.InParameter(
                type    = [1],
                ident   = p[2],
                doc     = p[5],
                default = p[4])


    # ------------------------------------------------------------------
    # Statements
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
        stmt : controller_stmt
             | connection_stmt
             | assignment_stmt
        """
        p[0] = p[1]


    # Controller
    def p_controller_stmt(self, p):
        """
        controller_stmt : CONTROLLER LPAREN ident RPAREN
        """
        p[0] = csast.ControllerStmt(
            ident = p[3],
            coord = self._coord(p.lineno(1)))

        
    # Connections.
    def p_connection_stmt(self, p):
        """
        connection_stmt : param_ref CONNECTION expr
        """
        p[0] = csast.ConnectionStmt(
            destination = p[1],
            source      = p[3],
            coord       = self._coord(p.lineno(2)))


    # Assignment.
    def p_assignment_stmt(self, p):
        """
        assignment_stmt : ident EQUALS component_stmt
        """
        p[0] = csast.AssignmentStmt(
            ident = p[1],
            comp  = p[3],
            coord = self._coord(p.lineno(2)))


    # A component statement: comp_id (expr_0, ..., expr_n)
    def p_component_stmt(self, p):
        """
        component_stmt : ident lparen expr_list rparen
        """
        p[0] = csast.ComponentStmt(
            ident  = p[1],
            inputs = p[3])


    # ------------------------------------------------------------------
    # expressions
    # ------------------------------------------------------------------
    def p_expr(self, p):
        """
        expr : constant
             | param_ref
             | ident
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
        p[0] = csast.Constant(
            type  = csast.Type('float'),
            value = p[1],
            coord = self._coord(p.lineno(1)))


    def p_iconst(self, p):
        """
        iconst : ICONST
        """
        p[0] = csast.Constant(
            type  = csast.Type('int'),
            value = p[1],
            coord = self._coord(p.lineno(1)))


    def p_sconst(self, p):
        """
        sconst : SCONST
        """
        p[0] = csast.Constant(
            type  = csast.Type('string'),
            value = p[1],
            coord = self._coord(p.lineno(1)))


    # Idents.
    def p_ident(self, p):
        """
        ident : IDENT
        """
        p[0] = csast.Ident(
            name  = p[1],
            coord = self._coord(p.lineno(1)))


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
            p[0] = csast.ParamRef(
                comp  = None,
                io    = csast.Ref(p[1]),
                ident = p[3])
        elif len(p) == 6:
            p[0] = csast.ParamRef(
                comp  = p[1],
                io    = csast.Ref(p[3]),
                ident = p[5])
        else:
            p[0] = csast.ParamRef(
                comp  = p[2],
                io    = csast.Ref(p[5]),
                ident = p[7])


    # ------------------------------------------------------------------
    # types
    # ------------------------------------------------------------------
    # The different types of the language.
    def p_type(self, p):
        """
        type : FILE
             | FLOAT
             | INT
             | STRING
             | IDENT
             | LBRACKET type RBRACKET
        """
        if len(p) == 2:
            p[0] = csast.Type(p[1] + self.dim)
            self.dim = ''
        else:
            self.dim += ('*')
            p[0] = p[2]


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
            p[0] = csast.DocString(p[1])
        else:
            p[0] = csast.DocString(None)


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
