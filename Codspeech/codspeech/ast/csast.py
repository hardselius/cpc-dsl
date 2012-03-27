# ----------------------------------------------------------------------
# Codspeech/codspeech/ast: csast.py
#
# AST Node classes for Codspeech
# ----------------------------------------------------------------------

import sys


class Node(object):
    """ Abstract base class for AST nodes.
    """
    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def show(
        self,
        buf=sys.stdout,
        offset=0,
        attrnames=False,
        nodenames=False,
        showcoord=False,
        _my_node_name=None):
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
    def __init__(self, definitions, coord=None):
        self.definitions = definitions
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.definitions or []):
            nodelist.append(("definitions[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class Import(Node):
    def __init__(self, path, coord=None):
        self.path = path
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('path',)

class NewType(Node):
    def __init__(self, type, typedecl, doc, coord=None):
        self.type = type
        self.typedecl = typedecl
        self.doc = doc
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        for i, child in enumerate(self.typedecl or []):
            nodelist.append(("typedecl[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class TypeDecl(Node):
    def __init__(self, type, ident, coord=None):
        self.type = type
        self.ident = ident
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        if self.ident is not None: nodelist.append(("ident", self.ident))
        return tuple(nodelist)

    attr_names = ()


class Component(Node):
    def __init__(self, header, body, coord=None):
        self.header = header
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.header is not None: nodelist.append(("header", self.header))
        if self.body is not None: nodelist.append(("body", self.body))
        return tuple(nodelist)

    attr_names = ()

class Header(Node):
    def __init__(self, ident, doc, inputs, outputs, coord=None):
        self.ident = ident
        self.doc = doc
        self.inputs = inputs
        self.outputs = outputs
        self.coord = coord

    def children(self):
        nodelist = []
        if self.ident is not None: nodelist.append(("ident", self.ident))
        if self.doc is not None: nodelist.append(("doc", self.doc))
        for i, child in enumerate(self.inputs or []):
            nodelist.append(("inputs[%d]" % i, child))
        for i, child in enumerate(self.outputs or []):
            nodelist.append(("outputs[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class InParameter(Node):
    def __init__(self, ident, type, doc, optional=False, default=None, coord=None):
        self.ident = ident
        self.type = type
        self.doc = doc
        self.optional = Optional(optional)
        self.default = default
        self.coord = coord

    def children(self):
        nodelist = []
        if self.ident is not None: nodelist.append(("ident", self.ident))
        if self.type is not None: nodelist.append(("type", self.type))
        if self.doc is not None: nodelist.append(("doc", self.doc))
        if self.optional is not None: nodelist.append(("optional", self.optional))
        if self.default is not None: nodelist.append(("default", self.default))
        return tuple(nodelist)

    attr_names = ()

class OutParameter(Node):
    def __init__(self, ident, type, doc, default=None, coord=None):
        self.ident = ident
        self.type = type
        self.doc = doc
        self.default = default
        self.coord = coord

    def children(self):
        nodelist = []
        if self.ident is not None: nodelist.append(("ident", self.ident))
        if self.type is not None: nodelist.append(("type", self.type))
        if self.doc is not None: nodelist.append(("doc", self.doc))
        if self.default is not None: nodelist.append(("default", self.default))
        return tuple(nodelist)

    attr_names = ()

class Network(Node):
    def __init__(self, body, controller=None, coord=None):
        self.body = body
        self.controller = controller
        self.coord = coord

    def children(self):
        nodelist = []
        if self.controller is not None: nodelist.append(("controller", self.controller))
        for i, child in enumerate(self.body or []):
            nodelist.append(("body[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class Controller(Node):
    def __init__(self, type, ident, coord=None):
        self.type = type
        self.ident = ident

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        if self.ident is not None: nodelist.append(("ident", self.ident))
        return tuple(nodelist)

    attr_names = ()

class Atom(Node):
    def __init__(self, comp, options, coord=None):
        self.comp = comp
        self.options = options
        self.coord = coord

    def children(self):
        nodelist = []
        if self.comp is not None: nodelist.append(("comp", self.comp))
        for i, child in enumerate(self.options or []):
            nodelist.append(("options[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class AtomType(Node):
    def __init__(self, type, coord=None):
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('type',)

class AtomOption(Node):
    def __init__(self, option, value, coord=None):
        self.option = option
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('option','value')

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

class Assignment(Node):
    def __init__(self, ident, comp, coord=None):
        self.ident = ident
        self.comp = comp
        self.coord = coord

    def children(self):
        nodelist = []
        if self.ident is not None: nodelist.append(("ident", self.ident))
        if self.comp is not None: nodelist.append(("comp", self.comp))
        return tuple(nodelist)

    attr_names = ()

class ComponentStmt(Node):
    def __init__(self, ident, inputs, coord=None):
        self.ident = ident
        self.inputs = inputs
        self.coord = coord

    def children(self):
        nodelist = []
        if self.ident is not None: nodelist.append(("ident", self.ident))
        for i, child in enumerate(self.inputs or []):
            nodelist.append(("inputs[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class Const(Node):
    def __init__(self, type, value, coord=None):
        self.type = type
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        return tuple(nodelist)

    attr_names = ('value',)

class ParamRef(Node):
    def __init__(self, comp, io, ident, coord=None):
        self.comp = comp
        self.io = io
        self.ident = ident
        self.coord = coord

    def children(self):
        nodelist = []
        if self.comp is not None: nodelist.append(("comp", self.comp))
        if self.io is not None: nodelist.append(("io", self.io))
        if self.ident is not None: nodelist.append(("ident", self.ident))
        return tuple(nodelist)

    attr_names = ()

class Ident(Node):
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('name',)

class Type(Node):
    def __init__(self, type, coord=None):
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('type',)

class DocString(Node):
    def __init__(self, doc, coord=None):
        self.doc = doc
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('doc',)

class Optional(Node):
    def __init__(self, bool, coord=None):
        self.bool = bool
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('bool',)

class Ref(Node):
    def __init__(self, ref, coord=None):
        self.ref = ref
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('ref',)
