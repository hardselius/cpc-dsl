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
        self.topdefenv = {}
        self.env = {}
        self.debug = debug
        if self.debug:
            print '\nDebug: ON'

            
    def typecheck(self, ast):
        """ Typechecks the AST

        Keyword arguments:
        ast - Duh...
        
        """
        self.visit(ast)
        #ctx = copy(self._getEnv())
        #self._resetEnv()
        #return ctx

        
    def add (self, env, id, type):
        env[id] = type

    def paramTypes(self, paramList):
        ps = []
        for p in paramList:
            if p.default:
                if not p.type.type == p.default.type.type:
                    _error_type(
                        p.default.coord,
                        "Constant type '%s' does not match '%s'"\
                        % p.default.type.type, p.type.type)
            elif self.getParamType(p.ident.name, ps):
                _error_ref(
                    p.ident.coord,
                    "multiple definitions of '%s'" % p.ident.name)
            else:
                ps.append((p.ident.name, p.type.type))
        return ps


    def getParamType(self, id, tupleList):
        for i, t in tupleList:
            if i == id: return t
        

    
    def visit_Program(self, node):
        for cname, c in node.children():
            if type(c) == csast.Import:
                pass
            elif type(c) == csast.Component:
                self.add(
                    self.topdefenv,
                    c.header.ident.name,
                    { 'in'  : self.paramTypes(c.header.inputs),
                      'out' : self.paramTypes(c.header.outputs) }
                )
            elif type(c) == csast.NewType:
                pass
            else:
                pass
        print self.topdefenv

        
    def visit_Component(self, node):
        self.component = node.header.ident.name
        pass
        



















        
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
