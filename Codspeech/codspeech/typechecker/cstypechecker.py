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


    def print_env(self):
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
        self.push()
        self.visit(node.body)
        if self.debug: self.print_env()
        self.pop()


    def visit_Import(self, node):
        pass


    def visit_NewType(self, node):
        pass


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
        self.add(node.ident, self.visit(node.comp))


    def visit_Connection(self, node):
        self.print_debug(node, '')
        tl = self.visit(node.left)
        tr = self.visit(node.right)
        if tl != tr:
            _error_type(
                left.coord,
                "type '%s' does not match type of left hand side ('%s')"\
                % tr, tl)
        else:
            return tl
        

    def visit_Assignment(self, node):
        self.print_debug(node, '')
        self.add(
            node.ident,
            self.visit(node.comp.ident))
        self.visit(node.comp)


    def visit_ComponentStmt(self, node):
        self.print_debug(node, '')
        inparams = copy(self.visit(node.ident)['in'])
        for i in node.inputs:
            if inparams:
                name, par_typ = inparams.pop(0)
                inp_typ       = self.visit(i)
                if inp_typ != par_typ:
                    _error_type(node.ident.coord, "componentstmt error")
            


    def visit_Const(self, node):
        self.print_debug(node, '')
        return self.visit(node.type)

        
    def visit_ParamRef(self, node):
        self.print_debug(node, '')
        try:
            io = node.io.ref
            pname = node.ident.name
            c = node.comp
            if type(c) == csast.Ident:
                cname = c.name
            elif type(c) == csast.ComponentStmt:
                cname = c.ident.name
            else:
                cname = self.component.header.ident.name
            return self.getParamType(pname, self.getEnv()[cname][io])
        except KeyError:
            _error_ref(
                node.ident.coord,
                "'%s' not defined" % (cname + '.' + pname))

        
    def visit_Ident(self, node):
        self.print_debug(node, node.name)
        try:
            return self.getEnv()[node.name]
        except KeyError:
            _error_ref(node.coord, "ident '%s': not defined" % node.name)
        

    def visit_Type(self, node):
        self.print_debug(node, '')
        return node.type


    def visit_Ref(self, node):
        self.print_debug(node, node.ref)
        return node.ref
