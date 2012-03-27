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

def _error_type(coord,msg):
    raise TypeError("%s: %s" % (coord,msg))

def _error_ref(coord,msg):
    raise ReferenceError("%s: %s" % (coord,msg))

    
class TypeChecker(csast.NodeVisitor):
    def __init__(self, debug=False):
        self.env = [{}]
        self.debug = debug
        if self.debug:
            print '\nDebug: ON'

            
    def typecheck(self, ast):
        """ Typechecks the AST

        Keyword arguments:
        ast - Duh...
        
        """
        self.visit(ast)

    def print_debug(self, node, msg):
        if self.debug:
            print "Visiting: '%s'" % node.__class__.__name__, msg


    def pop(self):
        self.env.pop()

    def push(self):
        self.env.append(copy(self.getEnv()))

    def getEnv(self):
        return self.env[-1]

    def add (self, ident, type):
        id = ident.name
        if self.getEnv().has_key(id):
            _error_ref(ident.coord, "ident already defined")
        else:
            self.getEnv()[id] = type


    def getType(self, node):
        try:
            if type(node) == csast.Ident:
                return self.getEnv()[self.visit(node)]
            elif type(node) == csast.ParamRef:                
                io    = self.visit(node.ref)
                pname = self.visit(node.ident)
                c     = node.comp
                if c:
                    if type(c) == csast.Ident:
                        cname = self.visit(c)
                    elif type(c) == csast.ComponentStmt:
                        cname = self.visit(c.ident)
                    else:
                        pass # some error?
                else:
                    cname = self.visit(self.component.header.ident)
                return self.getParamType(
                    pname,
                    self.getEnv()[cname][io])
            else:
                return None                
        except KeyError:
            _error_ref(node.coord, "not defined")


    def getParamType(self, id, tupleList):
        for i, t in tupleList:
            if i == id: return t

    
    def visit_Program(self, node):
        self.print_debug(node, 'lol')
        for cname, c in node.children():
            if type(c) == csast.Import:
                pass
            elif type(c) == csast.Component:
                self.add(
                    c.header.ident,
                    self.visit(c.header))
            elif type(c) == csast.NewType:
                pass
            else:
                pass
        self.generic_visit(node)
        

        
    def visit_Component(self, node):
        self.print_debug(node, '')
        self.component = node
        self.visit(node.body)
        self.env = {}


    def visit_Header(self, node):
        self.print_debug(node, 'Adding component types')
        inp  = []
        outp = []
        for i in node.inputs:
            if self.getParamType(i.ident.name, inp):
                _error_ref(
                    i.ident.coord,
                    "multiple definitions of '%s'" % i.ident.name)
            else:
                inp.append((i.ident.name, self.visit(i)))
                
        for o in node.outputs:
            if self.getParamType(o.ident.name, inp):
                _error_ref(
                    o.ident.coord,
                    "multiple definitions of '%s'" % o.ident.name)
            else:
                outp.append((o.ident.name, self.visit(o)))
        return { 'in'  : inp,
                 'out' : outp }

            
    def visit_InParameter(self, node):
        self.print_debug(node, '')
        if node.default:
            t = self.visit(node.type)
            d = self.visit(node.default)
            if not t == d:
                _error_type(
                    node.default.coord,
                    "Constant type '%s' does not match '%s'" % d, t)
        else:
            return self.visit(node.type)
        

    def visit_OutParameter(self, node):
        self.print_debug(node, '')
        return self.visit(node.type)


    def visit_Atom(self, node):
        self.print_debug(node, '')


    def visit_Network(self, node):
        self.print_debug(node, '')
        self.generic_visit(node)
        

    def visit_Controller(self, node):
        self.print_debug(node, '')
        self.add(node.ident, self.getType(node.comp))


    def visit_Constant(self, node):
        self.print_debug(node, '')
        return self.visit(node.type)

        
    def visit_Ident(self, node):
        self.print_debug(node, node.name)
        return node.name
        

    def visit_Type(self, node):
        self.print_debug(node, '')
        return node.type


    def visit_Ref(self, node):
        self.print_debug(node, node.ref)
        return node.ref




        



















        
#    def _getEnv(self):
#        """Returns the last record of the environment."""
#        return self.env[-1]
#
#    def _resetEnv(self):
#        """Resest the environment."""
#        self.env = [{}]
#
#    def _pop(self):
#        self.env.pop()
#
#    def _put(self):
#        self.env.append(copy(self._getEnv()))
#                    
#
#    def visit_Program(self, node):
#        """
#        Visit Program-nodes.
#        *   Add all Component names and their types to the environment.
#        *   [TODO] Add newtypes
#        *   [TODO] Add imports?
#        """
#        self._debug(node, '')
#        for comp in node.components:
#            self._add(
#                comp.header.ident,
#                { 'in'  : comp.header.inputs,
#                  'out' : comp.header.outputs })
#        for cname, c in node.children():
#            self.visit(c)
#
#
#    def visit_Component(self, node):
#        self._debug(node, node.header.ident.name)
#        self._put()
#        self._add(csast.Ident('in'),{})
#        self._add(csast.Ident('out'),{})
#        for cname, c in node.children():
#            self.visit(c)
#        self._pop()
#
#        
#    def visit_Header(self, node):
#        self._debug(node,'')
#        self.currentComp = node.ident.name
#        for cname, c in node.children():
#            self.visit(c)
#
#            
#    def visit_InParameter(self, node):
#        self._debug(node,node.ident.name)
#        self._addParameter(node, 'in')
#
#        
#    def visit_OutParameter(self, node):
#        self._debug(node,node.ident.name)
#        self._addParameter(node, 'out')
#
#        
#    def visit_Network(self, node):
#        self._debug(node,'')
#        for cname, c in node.children():
#            self.visit(c)
#
#            
#    def visit_Controller(self, node):
#        self._debug(node,'')
#        pass
#
#        
#    def visit_Connection(self, node):
#        self._debug(node,'')
#        pass
#
#        
#    def visit_Assignment(self, node):
#        self._debug(node,'')
#        pass
#
#        
#    def visit_ComponentStmt(self, node):
#        self._debug(node,'')
#        pass
#
#        
#    def _inferType(self, node):
#        if type(node) == csast.Const:
#            return node.type.type
#        elif type(node) == csast.Ident:
#            return self._getEnv()[node.name]
#            elif type(node) = csast.
#        elif type(node) == csast.ParamRef:
#            io = node.io.ref
#            if type(node.comp) == csast.Ident:
#                return self._typeParams(
#                    node.comp.name,
#                    self._getEnv()[]
#                )
#            elif type(node.comp) == csast.ComponentStmt:
#                pass
#            else:
#                return self._lookupParamType(
#                    node.ident.name,
#                    self._getEnv()[self.currentComp][io])
#
#    def _lookupParamType(self, id, params):
#        for p in params:
#            if p.ident.name == id: return p.type.type
#       
#
#    def _add(self, ident, type):
#        if self._varExist(ident.name):
#            _error_ref(
#                ident.coord,
#                "multiple definitions of '%s'" % ident.name)
#        else:
#            self._getEnv()[ident.name] = type
#
#    def _addParameter(self, node, io):
#        if self._getEnv()[io].has_key(node.ident.name):
#            _error_ref(
#                node.ident.coord,
#                "multiple definitions of '%s'" % node.ident.name)
#        elif node.default and node.type.type != node.default.type.type:
#            _error_type(
#                node.ident.coord,
#                "default value type doesn't match '%s'" % node.type.type)
#        else:
#            self._getEnv()[io][node.ident.name] = node.type.type
#        
#    def _varExist(self,var):
#        return self._getEnv().has_key(var)
#
#    def _debug(self, node, msg):
#        if self.debug:
#            print 'Visiting:', node.__class__.__name__, msg
#        else:
#            pass
