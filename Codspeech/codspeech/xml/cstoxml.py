# This file is part of Copernicus
# http://www.copernicus-computing.org/
# 
# Copyright (C) 2011, Sander Pronk, Iman Pouya, Erik Lindahl, Viktor Almqvist, Martin Hardselius, and others.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published 
# by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


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
        self.f.close()


    def print_debug(self, node, msg):
        if self.debug:
            print "Visiting: '%s'" % node.__class__.__name__, msg


    ##################################################################
    # Write XML functions

    def _ind(self):
        self.indent += ' '*self.ind


    def _unind(self):
        self.indent = self.indent[:len(self.indent)-self.ind]


    def _startFun(self,id,type):
        self.f.write(
            self.indent + "<function id=\"" + id \
            + "\" type=\"" + type + "\">\n")
        self._ind()


    def _endFun(self):
        self._unind()
        self.f.write(self.indent + "</function>\n")


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


    def _startType(self,type):
        self.f.write(
            self.indent + "<type id=\"" + self.visit(type) + \
                "\" base=\"list\">\n")
        self._ind()


    def _endType(self):
        self._unind()
        self.f.write(self.indent + "</type>\n")


    def _putTypeField(self,id,type):
        self.f.write(
            self.indent + "<field id=\"" + self.visit(id) + \
                "\" type=\"" + self.visit(type) + "\" />\n")


    def _putConnection(self,src,dest):
        if type(src) == csast.Constant:
            self.f.write(
                self.indent + "<assign type=\"" + \
                    self.visit(src.type) + "\" value=\"" + \
                    src.value.__str__() + "\" dest=\"" + \
                    self.visit(dest) + "\" />\n")
        else:
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

    ##################################################################
    # Visitor defenitions

    
    def visit_Program(self, node):
        self.f.write("<?xml version=\"1.0\" ?>\n<cpc>\n")
        self.generic_visit(node)
        self.f.write("</cpc>\n")


    def visit_Import(self,node):
        pass


    def visit_Newtype(self,node):
        self._startType(node.type)
        map(self.visit,node.typedecl)
        self.visit(node.doc)
        self._endType()


    def visit_TypeDecl(self,node):
        self._putTypeField(node.ident,node.type)


    def visit_Header(self, node):
        self.visit(node.doc)
        self.f.write(self.indent + "<inputs>\n")
        self._ind()
        map(self.visit,node.inputs)
        self._unind()
        self.f.write(self.indent + "</inputs>\n")
        self.f.write(self.indent + "<outputs>\n")
        self._ind()
        map(self.visit,node.outputs)
        self._unind()
        self.f.write(self.indent + "</outputs>\n")


    def visit_Atom(self, node):
        self._startFun(
            self.visit(node.header.ident),
            self.visit(node.atomtype))
        self.visit(node.header)
        self.visit(node.optionblock)
        self._endFun()


    def visit_AtomType(self, node):
        return node.type


    def visit_Optionblock(self,node):
        self._putController(node.options)


    def visit_Network(self, node):
        self._startFun(
            self.visit(node.header.ident),
            "network")
        self.visit(node.header)
        self.f.write(self.indent + "<network>\n")
        self._ind()
        self.visit(node.networkblock)
        self._unind()
        self.f.write(self.indent + "</network>\n")
        self._endFun()


    def visit_Networkblock(self,node):
        map(self.visit,node.stmts)


    def visit_InParameter(self, node):
        self._putParam(node)
        

    def visit_OutParameter(self, node):
        self._putParam(node)


#    def visit_Controller(self, node):
#        pass


    def visit_AssignmentStmt(self, node):
        pass
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
            if type(x) == csast.ParamRef and \
                    type(x.comp) == csast.ComponentStmt:
                self.temp += 1
                ident = csast.Ident("_t%s" % self.temp)
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


    def visit_ConnectionStmt(self, node):
        self._putConnection(node.source,node.destination)


    def visit_Constant(self, node):
        return node.value

        
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
        if node.doc != None:
            self.f.write(
                self.indent + "<desc>" + node.doc + "</desc>\n")


    def visit_Optional(self, node):
        return node.bool
