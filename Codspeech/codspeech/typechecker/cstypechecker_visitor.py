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
        self.visit(ast)
        ctx = copy(self._getEnv())
        self._resetEnv()
        return ctx


    def _getEnv(self):
        return self.env[-1]

    def _resetEnv(self):
        self.env = [{}]

    def _pop(self):
        self.env.pop()

    def _put(self):
        self.env.append(copy(self._getEnv()))

    def _add(self, ident, type):
        if self._varExist(ident.name):
            _error_ref(
                ident.coord,
                "multiple definitions of '%s'" % ident.name)
        else:
            self._getEnv()[ident.name] = type

    def _addParameter(self, node, io):
        if self._getEnv()[io].has_key(node.ident.name):
            _error_ref(
                node.ident.coord,
                "multiple definitions of '%s'" % node.ident.name)
        elif node.default and node.type.type != node.default.type.type:
            _error_type(
                node.ident.coord,
                "default value type doesn't match '%s'" % node.type.type)
        else:
            self._getEnv()[io][node.ident.name] = node.type.type
        
    def _varExist(self,var):
        return self._getEnv().has_key(var)

    def _debug(self, node, msg):
        if self.debug:
            print 'Visiting:', node.__class__.__name__, msg
        else:
            pass

    def _getType(self, node):
        pass

    def visit_Program(self, node):
        self._debug(node, '')
        for comp in node.components:
            self._add(
                comp.header.ident,
                { 'in'  : comp.header.inputs,
                  'out' : comp.header.outputs })
        for cname, c in node.children():
            self.visit(c)
        
    def visit_Component(self, node):
        self._debug(node, node.header.ident.name)
        self._put()
        self._add(csast.Ident('in'),{})
        self._add(csast.Ident('out'),{})
        self.visit(node.header)
        self._pop()

    def visit_Header(self, node):
        self._debug(node,'')
        for cname, c in node.children():
            self.visit(c)

    def visit_InParameter(self, node):
        self._debug(node,node.ident.name)
        self._addParameter(node, 'in')

    def visit_OutParameter(self, node):
        self._debug(node,node.ident.name)
        self._addParameter(node, 'out')

    def visit_Network(self, node):
        self._debug(node,'')
        for cname, c in node.children():
            self.visit(c)

    def visit_Controller(self, node):
        self._debug(node,'')
        pass

    def visit_Connection(self, node):
        self._debug(node,'')
        pass

    def visit_Assignment(self, node):
        self._debug(node,'')
        pass

    def visit_ComponentStmt(self, node):
        self._debug(node,'')
        pass