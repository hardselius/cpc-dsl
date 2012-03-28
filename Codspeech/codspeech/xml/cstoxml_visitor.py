# ------------------------------------------------------------------
# Codspeech/codspeech/typechecker: cstypechecker_visitor.py
#
# A typechecker for Codspeech
# ------------------------------------------------------------------

from copy import copy
from ..ast import csast
from ..parser.plyparser import Coord
    
class XMLGenerator(csast.NodeVisitor):
    def __init__(self, debug=False, ind = 4):
        self.ind = ind
        self.indent = ' '*ind
        self.debug = debug
        if self.debug:
            print '\nDebug: ON'

            
    def generateXML(self, ast, ctx, types = [], file = "output.xml"):
        """ Generate XML from the AST

        Keyword arguments:
        ast - Duh...
        
        """
        self.ctx = ctx
        self.types = types
        self.f = open(file,"w")
        self.temp = 0
        self.visit(ast)


    def print_debug(self, node, msg):
        if self.debug:
            print "Visiting: '%s'" % node.__class__.__name__, msg


    #---------------------------------------------------------------------
    # Write XML functions
    #---------------------------------------------------------------------

    def _ind(self):
        self.indent += ' '*self.ind


    def _unind(self):
        self.indent = self.indent[:len(self.indent)-self.ind]


    def _init(self):
        self.f.write("<?xml version=\"1.0\" ?>\n<cpc>\n")


    def _end(self):
        self.f.write("</cpc>\n")
        self.f.close()


    def _startFun(self,id,type):
        self.f.write(
            self.indent + "<function id=\"" + id \
            + "\" type=\"" + type + "\">\n")
        self._ind()


    def _endFun(self):
        self._unind()
        self.f.write(self.indent + "</function>\n")


    def _startInput(self):
        self.f.write(self.indent + "<inputs>\n")
        self._ind()


    def _endInput(self):
        self._unind()
        self.f.write(self.indent + "</inputs>\n")


    def _startOutput(self):
        self.f.write(self.indent + "<outputs>\n")
        self._ind()


    def _endOutput(self):
        self._unind()
        self.f.write(self.indent + "</outputs>\n")


    def _putParam(self,node):
        self.f.write(
            self.indent + "<field type=\"" + self.visit(node.ident) \
            + "\" id=\"" + self.visit(node.type) + "\"")
        if type(node) == csast.InParameter:
            if self.visit(node.optional):
                self.f.write(" opt=\"true\"")
        if node.doc.doc:
            self.f.write(">\n")
            self._ind()
            self.visit(node.doc)
            self._unind()
            self.f.write(self.indent + "</field>\n")
        else:
            self.f.write(" />\n")


    def _putDoc(self,desc):
        if desc != None:
            self.f.write(self.indent + "<desc>" + desc + "</desc>\n")


    def _putController(self,opts):
        self.f.write(self.indent + "<controller ")
        for x in opts:
            self.f.write(
                x.option.translate(None, '"') + \
                    "=\"" + x.value + "\"")
            if x == opts[-1]:
                self.f.write(" />\n")
            else:
                self.f.write("\n" + self.indent + "            ")


    def _putImport(self,module):
        self.f.write(self.indent + "<import name=\"" \
                                 + module + "\" />\n")


    def _startNet(self):
        self.f.write(self.indent + "<network>\n")
        self._ind()


    def _endNet(self):
        self._unind()
        self.f.write(self.indent + "</network>\n")


    def _startType(self,type):
        self.f.write(
            self.indent + "<type id=\"" + self.visit(type) + \
                "\" base=\"list\">\n")
        self._ind()


    def _endType(self):
        self._unind()
        self.f.write(self.indent + "</type>\n")


    def _putTypeField(self,ident,type):
        self.f.write(
            self.indent + "<field id=\"" + self.visit(ident) + \
                "\" type=\"" + self.visit(type) + "\" />\n")


    def _putConnection(self,src,dest):
        self.f.write(
            self.indent + "<connection src=\"" + \
                self.visit(src) + "\" dest=\"" + \
                self.visit(dest) + "\" />\n")


    def _putInstance(self,id,fun):
        self.f.write(
            self.indent + "<instance id=\"" + \
                self.visit(id) + "\" function=\"" + \
                self.visit(fun) + "\" />\n")


    def _showIdent(self,a):
        if type(a) == csast.This:
            return "self:ext_" + a.io + "." + a.ident.name
        elif type(a) == csast.Other:
            return a.component.name + ":" + a.io + "." + a.ident.name
        elif type(a) == csast.Comp:
            return a.component.ident.name + ":" + a.io + \
                                            "." + a.ident.name
        else:
            return a.name

    #-----------------------------------------------------------------

    
    def visit_Program(self, node):
        self._init()
        self.generic_visit(node)
        self._end()


    def visit_Import(self,node):
        pass


    def visit_NewType(self,node):
        self._startType(node.type)
        map(self.visit,node.typedecl)
        self.visit(node.doc)
        self._endType()


    def visit_TypeDecl(self,node):
        self._putTypeField(node.ident,node.type)

        
    def visit_Component(self, node):
        if type(node.body) == csast.Network:
            self._startFun(
                self.visit(node.header.ident),
                "network")
        else:
            self._startFun(
                self.visit(node.header.ident),
                self.visit(node.body.atomtype))
        self.visit(node.header)
        self.visit(node.body)
        self._endFun()


    def visit_Header(self, node):
        self.visit(node.doc)
        self._startInput()
        map(self.visit,node.inputs)
        self._endInput()
        self._startOutput()
        map(self.visit,node.outputs)
        self._endOutput()


    def visit_InParameter(self, node):
        self._putParam(node)
        

    def visit_OutParameter(self, node):
        self._putParam(node)


    def visit_Atom(self, node):
        self._putController(node.options)


    def visit_AtomType(self, node):
        return node.type


    def visit_Network(self, node):
        self._startNet()
        self.generic_visit(node)        
        self._endNet()


    def visit_Controller(self, node):
        pass


    def visit_Assignment(self, node):
        cs = self.visit(node.comp)
        self._putInstance(node.ident,node.comp.ident)
        for src,dest in cs:
            self._putConnection(
                src,
                csast.ParamRef(
                    node.ident,
                    csast.Ref('in'),
                    csast.Ident(dest)))
        self.f.write("\n")


    def visit_ComponentStmt(self, node):
        cs = []
        args = self.ctx[self.visit(node.ident)]['in']
        for i, x in enumerate(node.inputs):
            if type(x.comp) == csast.ComponentStmt:
                self.temp += 1
                ident = csast.Ident("TEMP%s" % self.temp)
                outRef = csast.ParamRef(ident, x.io, x.ident)
                c = self.visit(x.comp)
                self._putInstance(ident,x.comp.ident)
                for src,dest in c:
                    self._putConnection(
                        src,
                        csast.ParamRef(
                            ident,
                            csast.Ref('in'),
                            csast.Ident(dest)))
                self.f.write("\n")
                cs.append((outRef,args[i][0]))
            else:
                cs.append((x,args[i][0]))
        return cs


    def visit_Connection(self, node):
        self._putConnection(node.left,node.right)


    def visit_Constant(self, node):
        pass

        
    def visit_Ident(self, node):
        return node.name


    def visit_Type(self, node):
        return node.type.lower()


    def visit_ParamRef(self, node):
        s = ""
        if node.comp:
            s += self.visit(node.comp) + ":"
        else:
            s += "self:ext_"
        s += self.visit(node.io) + "."
        s += self.visit(node.ident)
        return s


    def visit_Ref(self,node):
        return node.ref


    def visit_DocString(self, node):
        self._putDoc(node.doc)


    def visit_Optional(self, node):
        return node.bool
