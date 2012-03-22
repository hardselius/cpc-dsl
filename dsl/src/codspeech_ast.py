#-----------------------------------------------------------------
# ** ATTENTION **
# This code was automatically generated from the file:
# _codspeech_ast.cfg
#
# Do not modify it directly. Modify the configuration file and
# run the generator again.
# ** ** *** ** **
#
# pycparser: c_ast.py
#
# AST Node classes.
#
# Copyright (C) 2008-2012, Eli Bendersky
# License: BSD
#-----------------------------------------------------------------


import sys


class Node(object):
    """ Abstract base class for AST nodes.
    """
    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
        """ Pretty print the Node and all its attributes and
            children (recursively) to a buffer.

            buf:
                Open IO buffer into which the Node is printed.

            offset:
                Initial offset (amount of leading spaces)

            attrnames:
                True if you want to see the attribute names in
                name=value pairs. False to only see the values.

            nodenames:
                True if you want to see the actual node names
                within their parents.

            showcoord:
                Do you want the coordinates of each Node to be
                displayed.
        """
        lead = ' ' * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
        else:
            buf.write(lead + self.__class__.__name__+ ': ')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self,n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showcoord:
            buf.write(' (at %s)' % self.coord)
        buf.write('\n')

        for (child_name, child) in self.children():
            child.show(
                buf,
                offset=offset + 2,
                attrnames=attrnames,
                nodenames=nodenames,
                showcoord=showcoord,
                _my_node_name=child_name)


class NodeVisitor(object):
    """ A base NodeVisitor class for visiting c_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.

        For example:

        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []

            def visit_Constant(self, node):
                self.values.append(node.value)

        Creates a list of values of all the constant nodes
        encountered below the given node. To use it:

        cv = ConstantVisitor()
        cv.visit(node)

        Notes:

        *   generic_visit() will be called for AST nodes for which
            no visit_XXX method was defined.
        *   The children of nodes for which a visit_XXX was
            defined will not be visited - if you need this, call
            generic_visit() on the node.
            You can use:
                NodeVisitor.generic_visit(self, node)
        *   Modeled after Python's own AST visiting facilities
            (the ast module of Python 3.0)
    """
    def visit(self, node):
        """ Visit a node.
        """
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for c_name, c in node.children():
            self.visit(c)


class Program(Node):
    def __init__(self, imports, components, coord=None):
        self.imports = imports
        self.components = components
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.imports or []):
            nodelist.append(("imports[%d]" % i, child))
        for i, child in enumerate(self.components or []):
            nodelist.append(("components[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class Import(Node):
    def __init__(self, package, coord=None):
        self.package = package
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('package',)

class Component(Node):
    def __init__(self, doc, name, in_params, out_params, body, coord=None):
        self.doc = doc
        self.name = name
        self.in_params = in_params
        self.out_params = out_params
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.doc is not None: nodelist.append(("doc", self.doc))
        if self.name is not None: nodelist.append(("name", self.name))
        if self.in_params is not None: nodelist.append(("in_params", self.in_params))
        if self.out_params is not None: nodelist.append(("out_params", self.out_params))
        if self.body is not None: nodelist.append(("body", self.body))
        return tuple(nodelist)

    attr_names = ()

class In(Node):
    def __init__(self, params, coord=None):
        self.params = params
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.params or []):
            nodelist.append(("params[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class Out(Node):
    def __init__(self, params, coord=None):
        self.params = params
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.params or []):
            nodelist.append(("params[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class InParam(Node):
    def __init__(self, doc, type, name, opt, default, coord=None):
        self.doc = doc
        self.type = type
        self.name = name
        self.opt = opt
        self.default = default
        self.coord = coord

    def children(self):
        nodelist = []
        if self.doc is not None: nodelist.append(("doc", self.doc))
        if self.type is not None: nodelist.append(("type", self.type))
        if self.name is not None: nodelist.append(("name", self.name))
        if self.opt is not None: nodelist.append(("opt", self.opt))
        if self.default is not None: nodelist.append(("default", self.default))
        return tuple(nodelist)

    attr_names = ()

class OutParam(Node):
    def __init__(self, doc, type, name, default, coord=None):
        self.doc = doc
        self.type = type
        self.name = name
        self.default = default
        self.coord = coord

    def children(self):
        nodelist = []
        if self.doc is not None: nodelist.append(("doc", self.doc))
        if self.type is not None: nodelist.append(("type", self.type))
        if self.name is not None: nodelist.append(("name", self.name))
        if self.default is not None: nodelist.append(("default", self.default))
        return tuple(nodelist)

    attr_names = ()

class Atom(Node):
    def __init__(self, atomtype, atomconfs, coord=None):
        self.atomtype = atomtype
        self.atomconfs = atomconfs
        self.coord = coord

    def children(self):
        nodelist = []
        if self.atomtype is not None: nodelist.append(("atomtype", self.atomtype))
        for i, child in enumerate(self.atomconfs or []):
            nodelist.append(("atomconfs[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class AtomType(Node):
    def __init__(self, atomtype, coord=None):
        self.atomtype = atomtype
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('atomtype',)

class AtomConf(Node):
    def __init__(self, option, value, coord=None):
        self.option = option
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('option','value',)

class Network(Node):
    def __init__(self, controller, stmtblock, coord=None):
        self.controller = controller
        self.stmtblock = stmtblock
        self.coord = coord

    def children(self):
        nodelist = []
        if self.controller is not None: nodelist.append(("controller", self.controller))
        if self.stmtblock is not None: nodelist.append(("stmtblock", self.stmtblock))
        return tuple(nodelist)

    attr_names = ()

class StmtBlock(Node):
    def __init__(self, stmts, coord=None):
        self.stmts = stmts
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.stmts or []):
            nodelist.append(("stmts[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class Controller(Node):
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        return tuple(nodelist)

    attr_names = ()

class Assignment(Node):
    def __init__(self, name, compstmt, coord=None):
        self.name = name
        self.compstmt = compstmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.compstmt is not None: nodelist.append(("compstmt", self.compstmt))
        return tuple(nodelist)

    attr_names = ()

class CompStmt(Node):
    def __init__(self, name, params, coord=None):
        self.name = name
        self.params = params
        self.coord = coord

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        for i, child in enumerate(self.params or []):
            nodelist.append(("params[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class Connection(Node):
    def __init__(self, left, right, coord=None):
        self.left = left
        self.right = right
        self.coord = coord

    def children(self):
        nodelist = []
        if self.left is not None: nodelist.append(("left", self.left))
        if self.right is not None: nodelist.append(("right", self.right))
        return tuple(nodelist)

    attr_names = ()

class ParamRef(Node):
    def __init__(self, comp, direction, param, coord=None):
        self.comp = comp
        self.direction = direction
        self.param = param
        self.coord = coord

    def children(self):
        nodelist = []
        if self.comp is not None: nodelist.append(("comp", self.comp))
        if self.param is not None: nodelist.append(("param", self.param))
        return tuple(nodelist)

    attr_names = ('direction',)

class ID(Node):
    def __init__(self, id, coord=None):
        self.id = id
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('id',)

class Type(Node):
    def __init__(self, type, coord=None):
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('type',)

class Optional(Node):
    def __init__(self, bool, coord=None):
        self.bool = bool
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('bool',)

class Constant(Node):
    def __init__(self, type, value, coord=None):
        self.type = type
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('type','value',)

class Docstring(Node):
    def __init__(self, doc, coord=None):
        self.doc = doc
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('doc',)

class Empty(Node):
    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    attr_names = ()

