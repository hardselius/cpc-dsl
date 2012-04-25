# ------------------------------------------------------------------
# Codspeech/codspeech/typechecker: cstypechecker_visitor.py
#
# A typechecker for Codspeech
# ------------------------------------------------------------------

from copy import copy
from ..ast import csast
from ..parser.plyparser import Coord


class TypeError(Exception): pass


class ReferenceError(Exception): pass

    
class TypeChecker(csast.NodeVisitor):
    def __init__(self, debug=False):
        self.env = [{}]
        self.newtypes = {}
        self.arrays = []
        self.debug = debug
        if self.debug:
            print '\nDebug: ON'

            
    def typecheck(self, ast):
        """ Typechecks the AST

        Keyword arguments:
        ast - Duh...
        
        """
        self.env = [{}]
        self.newtypes = {}
        self.arrays = []
        self.visit(ast)


    def print_env(self):
        """Pretty-print the environment."""
        ind = '    '
        e = self.getEnv()
        for k, v in e.iteritems():
            if type(v) == dict:
                print k, ':'
                for kv, vv in e[k].iteritems():
                    print 1*ind, kv, ':'
                    for t in vv:
                        print 2*ind, t
            else:
                print k, ':', v

                
    def getEnv(self):
        return self.env[-1]

        
    ## 
    ## INTERNAL AUXILIARY METHODS -- PRIVATE
    ## 

    def _print_debug(self, node, msg):
        """Prints debug messages if debugmode is on."""
        if self.debug:
            print "Visiting: '%s'" % node.__class__.__name__, msg

        
    def _pop(self):
        self.env.pop()

        
    def _push(self):
        self.env.append(copy(self.getEnv()))

    
    def _add(self, ident, t):
        id = ident.name
        if self.getEnv().has_key(id):
            self._ref_error(ident.coord, "ident already defined")
        else:
            self.getEnv()[id] = t


    def _getParamType(self, id, tupleList):
        for i, t in tupleList:
            if i == id: return t


    def _type_error(self, coord, msg):
        raise TypeError("Type Error %s: %s" % (coord,msg))


    def _ref_error(self, coord, msg):
        raise ReferenceError("Reference Error %s: %s" % (coord,msg))


    ## 
    ## VISITOR METHODS
    ##

    ## PROGRAM
    
    def visit_Program(self, node):
        """Will add the top-level definitions to the context before
        continuing with type checking of Atoms and Networks.

        """
        self._print_debug(node, "Checking top-level definitions")
        self.generic_visit(node)
        

    ## IMPORT

    def visit_Import(self, node):
        self.generic_visit(node)


    ## NEWTYPE
        
    def visit_Newtype(self, node):
        t = dict(map(self.visit_TypeDecl,node.typedecl))
        self.newtypes[node.type.type] = t


    def visit_TypeDecl(self, node):
        return (node.ident.name,node.type.type)

            
    ## ATOM

    def visit_Atom(self, node):
        self._print_debug(node, '')
        self.generic_visit(node)
        

    def visit_AtomType(self, node):
        self._print_debug(node, 'Nothing to do here...')


    def visit_Optionblock(self, node):
        self._print_debug(node, 'Nothing to do here...')


    def visit_AtomOption(self, node):
        self._print_debug(node, 'Nothing to do here...')


    ## NETWORK
        
    def visit_Network(self, node):
        self._print_debug(node, '')
        self.scope = node
        self.generic_visit(node)


    def visit_Networkblock(self, node):
        self._print_debug(node, 'Entering new scope')
        self._push()
        self.generic_visit(node)
        self._pop()


    ## HEADER

    def visit_Header(self, node):
        self._print_debug(node, 'Adding header types')
        inp  = []
        outp = []
        for i in node.inputs:
            if dict(inp).get(i.ident.name):
                self._ref_error(
                    i.ident.coord,
                    "multiple definitions of '%s'" % i.ident.name)
            else:
                inp.append((i.ident.name, self.visit(i)))
                
        for o in node.outputs:
            if dict(outp).get(o.ident.name):
                self._ref_error(
                    o.ident.coord,
                    "multiple definitions of '%s'" % o.ident.name)
            else:
                outp.append((o.ident.name, self.visit(o)))
        self._add(node.ident, {'in':inp, 'out':outp})

            
    def visit_InParameter(self, node):
        self._print_debug(node, '')
        t = self.visit(node.type)
        if node.default:
            d = self.visit(node.default)
            if not t == d:
                self._type_error(
                    node.default.coord,
                    "Constant type '%s' does not match '%s'" % d, t)

        self._addArrays(t)
        return t
        

    def visit_OutParameter(self, node):
        self._print_debug(node, '')
        t = self.visit(node.type)
        self._addArrays(t)
        return t


    def _addArrays(self,t):
        temp = t
        tempA = []
        while self._isArray(temp):
            if not any(temp == s for s in self.arrays):
                tempA.append(temp)
            temp = temp[:-2]
        tempA.reverse()
        self.arrays += tempA

    ## STATEMENTS
        

    def visit_ControllerStmt(self, node):
        self._print_debug(
            node,
            "Checking if '%s' is in scope" % node.ident.name)
        if not self.getEnv().has_key(node.ident.name):
            self._ref_error(
                node.coord,
                "'%s' not in scope" % node.ident.name)


    def visit_ConnectionStmt(self, node):
        self._print_debug(node, "Checking 'source' and 'destination' types")
        t_dest   = self.visit(node.destination)
        t_source = self.visit(node.source)
        if t_dest != t_source:
            self._type_error(
                node.coord,
                "destination type '%s' does not match source type '%s'"\
                % (t_dest, t_source))
        else:
            return t_source
        

    def visit_AssignmentStmt(self, node):
        self._print_debug(node, "Adding new component to the context")
        self._add(
            node.ident,
            self.visit(node.comp.ident))
        self.visit(node.comp)


    def visit_ComponentStmt(self, node):
        self._print_debug(node, '')
        inparams = copy(self.visit(node.ident)['in'])
        for i in node.inputs:
            if inparams:
                name, par_typ = inparams.pop(0)
                inp_typ       = self.visit(i)
                if inp_typ != par_typ:
                    self._type_error(
                        node.ident.coord,
                        "input '{0}' has type '{1}', expected '{2}'".format(
                            i.__class__.__name__,
                            inp_typ,
                            par_typ))
            

    ## EXPRESSIONS
    
    def visit_Constant(self, node):
        self._print_debug(node, '')
        return self.visit(node.type)

        
    def visit_ParamRef(self, node):
        self._print_debug(node, '')
        io = node.io.ref
        pname = node.ident.name
        c = node.comp
        if type(c) == csast.Ident:
            cname = c.name
        elif type(c) == csast.ComponentStmt:
            self.visit(c)
            cname = c.ident.name
        else:
            cname = self.scope.header.ident.name
        t = dict(self.getEnv()[cname][io]).get(pname)
        if t:
            if node.settId:
                if type(node.settId) == int:
                    if self._isArray(t):
                        if self._isArray(t[:-2]):
                            return t[:-2]
                        else:
                            return self._checkNew(t[:-2])
                    else:
                        self._type_error(
                            node.ident.coord,
                            "'%s' is not an array" % \
                                (cname + '.' + pname))
                elif t.has_key(node.settId.name):
                    return t[node.settId.name]
                else:
                    self._ref_error(
                        node.ident.coord,
                        "'%s' has no variable %s" % \
                            (cname + '.' + pname,node.settId.name))
            else:
                return t
        else:
            self._ref_error(
                node.ident.coord,
                "'%s' not defined" % (cname + '.' + pname))


    def visit_Ref(self, node):
        self._print_debug(node, node.ref)
        return node.ref

        
    def visit_Ident(self, node):
        self._print_debug(node, node.name)
        try:
            return self.getEnv()[node.name]
        except KeyError:
            self._ref_error(
                node.coord,
                "ident '%s': not defined" % node.name)
        

    ## TYPE
            
    def visit_Type(self, node):
        self._print_debug(node, '')
        return self._checkNew(node.type)


    def _isArray(self,t):
        return type(t) == str and t[-2:] == '[]'


    def _checkNew(self,t):
        if self.newtypes.has_key(t):
            return self.newtypes[t]
        else:
            return t
