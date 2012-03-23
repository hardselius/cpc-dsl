# ----------------------------------------------------------------------
# Codspeech/codspeech/ast: csast.py
#
# AST Node classes for Codspeech
# ----------------------------------------------------------------------

import sys

class Node(object):
    """Abstract base class for AST nodes."""
    def children(self):
        """A sequence of all children that are Nodes"""
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



indent = ""

def strNewLine(x):
        if x == []:
            return ""
        else:
            y = x.pop(0)
            return "\n" + indent + str(y) + strNewLine(x)

class Program(object):
    def __init__(self, imports, components, newtypes, coord=None):
        self.imports    = imports
        self.components = components
	self.newtypes   = newtypes
        self.coord      = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.imports or []):
            nodelist.append("imports[%d]" % i, child)
        for i, child in enumerate(self.components or []):
            nodelist.append("components[%d]" % i, child)
        for i, child in enumerate(self.newtypes or []):
            nodelist.append("newtypes[%d]" % i, child)
        return tuple(nodelist)

    attr_names = ()

    def __str__(self):
        global indent
        indent = "    "
        s = "Program:" + indent + strNewLine(self.imports) + \
            "\n" + indent + strNewLine(self.newtypes) + \
            "\n" + indent + strNewLine(self.components)
        indent = ""
        return s


class Import(object):
    def __init__(self, path):
        self.path = p

    def __str__(self):
        global indent
        return "Import: " + str(self.path)


class NewType(object):
    def __init__(self,id,b,d = None):
        self.ident = id
	self.body  = b
	self.doc   = d

    def __str__(self):
        global indent
        indent += "    "
        s = "NewType: " + str(self.ident) + \
            indent + strNewLine(self.body)
        indent = indent[:len(indent)-4]
        return s


class NewTypeObject(object):
    def __init__(self,id,t):
        self.ident = id
	self.type  = t

    def __str__(self):
        global indent
        return "NWObject: " + str(self.ident) + ", " + str(self.type)


class Import(object):
    def __init__(self,p):
        self.path = p

    def __str__(self):
        global indent
        return "Import: " + str(self.path)


class Component(object):
    def __init__(self,h,b):
        self.header = h
        self.body   = b

    def __str__(self):
        global indent
        indent += "    "
        s = "Component:\n" + indent + str(self.header) + \
            "\n" + indent + str(self.body)
        indent = indent[:len(indent)-4]
	return s


class Header(object):
    def __init__(self,id,i,o,d = None):
        self.ident   = id
        self.doc     = d
        self.inputs  = i
        self.outputs = o

    def __str__(self):
        global indent
        indent += "    "
        s = "Header:\n" + indent + str(self.ident) + \
            "\n" + indent + str(self.doc) + \
            "\n" + indent + strNewLine(self.inputs) + \
            "\n" + indent + strNewLine(self.outputs)
        indent = indent[:len(indent)-4]
	return s


class InParameter(object):
    def __init__(self,id,t,d = None,de = None,opt = False):
        self.ident    = id
        self.type     = t
        self.doc      = d
        self.optional = opt
        self.default  = de

    def __str__(self):
        global indent
        indent += "    "
        s = "InParameter:\n" + indent + str(self.ident) + \
            "\n" + indent + str(self.type) + \
            "\n" + indent + str(self.optional) + \
            "\n" + indent + str(self.default) + \
            "\n" + indent + str(self.doc)
        indent = indent[:len(indent)-4]
	return s


class OutParameter(object):
    def __init__(self,id,t,d = None,de = None):
        self.ident    = id
        self.type     = t
        self.doc      = d
        self.default  = de

    def __str__(self):
        global indent
        indent += "    "
        s = "OutParameter:\n" + indent + str(self.ident) + \
            "\n" + indent + str(self.type) + \
            "\n" + indent + str(self.default) + \
            "\n" + indent + str(self.doc)
        indent = indent[:len(indent)-4]
	return s


class Network(object):
    def __init__(self,b,contr = None):
        self.body       = b
        self.controller = contr

    def __str__(self):
        global indent
        indent += "    "
        s = "Network:\n" + indent + str(self.controller) + \
            indent + strNewLine(self.body)
        indent = indent[:len(indent)-4]
	return s


class Controller(object):
    def __init__(self,t,id):
        self.type  = t
        self.ident = id

    def __str__(self):
        global indent
        indent += "    "
        s = "Controller: " + str(self.type) + \
            "\n" + indent + str(self.ident)
        indent = indent[:len(indent)-4]
	return s


class Atom(object):
    def __init__(self,t,opts):
        self.type    = t
        self.options = opts

    def __str__(self):
        global indent
        indent += "    "
        s = "Atom: " + str(self.type) + \
            "\n" + indent + strNewLine(self.options)
        indent = indent[:len(indent)-4]
	return s


class AtomOption(object):
    def __init__(self,opt,val):
        self.option = opt
        self.value  = val

    def __str__(self):
        global indent
        indent += "    "
        s = "AtomOption:\n" + indent + str(self.option) + \
               "\n" + indent + str(self.value)
        indent = indent[:len(indent)-4]
	return s


class Connection(object):
    def __init__(self,l,r):
        self.left  = l
        self.right = r

    def __str__(self):
        global indent
        indent += "    "
        s = "Connection:\n" + indent + str(self.left) + \
            "\n" + indent + str(self.right)
        indent = indent[:len(indent)-4]
	return s


class Assignment(object):
    def __init__(self,id,comp):
        self.ident     = id
        self.component = comp

    def __str__(self):
        global indent
        indent += "    "
        s = "Assignment:\n" + indent + str(self.ident) + \
            "\n" + indent + str(self.component)
        indent = indent[:len(indent)-4]
	return s


class ComponentStmt(object):
    def __init__(self,id,i):
        self.ident  = id
        self.inputs = i

    def __str__(self):
        global indent
        indent += "    "
        s = "ComponentStmt:\n" + indent + str(self.ident) + \
            indent + strNewLine(self.inputs)
        indent = indent[:len(indent)-4]
	return s


class Const(object):
    def __init__(self,t,v):
        self.type  = t
        self.value = v

    def __str__(self):
        global indent
        return "Const: " + str(self.type) + " " + str(self.value)


class This(object):
    def __init__(self,id,io):
        self.ident     = id
        self.io        = io

    def __str__(self):
        global indent
        indent += "    "
        s = "This: " + str(self.io) + " " + str(self.ident)
        indent = indent[:len(indent)-4]
	return s


class Other(object):
    def __init__(self,id,io,comp):
        self.ident     = id
        self.io        = io
        self.component = comp

    def __str__(self):
        global indent
        indent += "    "
        s = "Other: " + str(self.component) + \
            " " + str(self.io) + " " + str(self.ident)
        indent = indent[:len(indent)-4]
	return s


class Comp(object):
    def __init__(self,id,io,comp):
        self.ident     = id
        self.io        = io
        self.component = comp

    def __str__(self):
        global indent
        indent += "    "
        s = "Comp: " + str(self.io) + " " + str(self.ident) + \
            "\n" + indent + str(self.component)
        indent = indent[:len(indent)-4]
	return s


class Ident(object):
    def __init__(self,n,p = '?'):
        self.name = n
        self.pos  = p

    def __str__(self):
        global indent
        return "Ident: " + str(self.name) + " " + str(self.pos)
