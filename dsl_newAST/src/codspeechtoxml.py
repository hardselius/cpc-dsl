import copy
import ast

class XMLGenerator:
    def __init__(self,ind = 4):
        self.i = ind
        self.indent = ' '*ind
        self.ctx = None
        self.f = None
        self.tempName = 0

    def _ind(self):
        self.indent += ' '*self.i

    def _unind(self):
        self.indent = self.indent[:len(self.indent)-self.i]

#---------------------------------------------------------------------
# Write XML functions
#---------------------------------------------------------------------

    def _init(self):
        self.f.write("<?xml version=\"1.0\" ?>\n<cpc>\n")

    def _end(self):
        self.f.write("</cpc>\n")
        self.f.close()

    def _startFun(self,id,type):
        self.f.write(self.indent + "<function id=\"" + id
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

    def _putParam(self,param):
        self.f.write(self.indent + "<field type=\"" + param.type.lower() \
                                 + "\" id=\"" + param.ident.name + "\"")
        if type(param) == ast.InParameter and param.optional:
            self.f.write(" opt=\"true\"")
        if param.doc == None:
            self.f.write(" />\n")
        else:
            self.f.write(">\n")
            self._ind()
            self._putDoc(param.doc)
            self._unind()
            self.f.write(self.indent + "</field>\n")

    def _putDoc(self,desc):
        if desc != None:
            self.f.write(self.indent + "<desc>" + desc + "</desc>\n")

    def _putController(self,opts):
        self.f.write(self.indent + "<controller ")
        for x in opts:
            self.f.write(x.option.value.translate(None, '"') + \
                         "=" + x.value.value)
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

    def _putConnection(self,src,dest):
        self.f.write(self.indent + "<connection src=\""    \
                   + self._showIdent(src) + "\" dest=\"" \
                   + self._showIdent(dest) + "\" />\n")

    def _putInstance(self,id,fun):
        self.f.write(self.indent + "<instance id=\""                \
                   + self._showIdent(id) + "\" function=\"" \
                   + self._showIdent(fun) + "\" />\n")

    def _showIdent(self,a):
        if type(a) == ast.This:
            return "self:ext_" + a.io + "." + a.ident.name
        elif type(a) == ast.Other:
            return a.component.name + ":" + a.io + "." + a.ident.name
        elif type(a) == ast.Comp:
            return a.component.ident.name + ":" + a.io + \
                                            "." + a.ident.name
        else:
            return a.name

    #-----------------------------------------------------------------
    # Build a cpc XML from abstract syntax tree
    #-----------------------------------------------------------------
    def generateXML(self,ast,context,file = "output.xml"):
        self.ctx = context
        self.f = open(file,"w")
        self._toXML(ast)

    def _toXML(self,t):
        #elif t[0] == 'IMPORT':
        #    putImport('.'.join(t[1]))

        if type(t) == ast.Program:
            self._init()
            map(self._toXML,t.imports)
            map(self._toXML,t.components)
            self._end()    

        elif type(t) == ast.Network:
            self._startNet()
            self._toXML(t.controller)
            map(self._toXML,t.body)
            self._endNet()

        elif type(t) == ast.Component:
            if type(t.body) == ast.Network:
                self._startFun(t.header.ident.name,"network")
            else:
                self._startFun(t.header.ident.name,t.body.type)
            self._putDoc(t.header.doc)
            self._startInput()
            map(self._putParam,t.header.inputs)
            self._endInput()
            self._startOutput()
            map(self._putParam,t.header.outputs)
            self._endOutput()
            self._toXML(t.body)
            self._endFun()

        elif type(t) == ast.Assignment:
            self._putInstance(t.ident,t.component.ident)
            args = copy.copy(self.ctx[t.component.ident.name]['in'])
            for x in t.component.inputs:
                y = args.pop(0)
                if type(x) == ast.ComponentStmt:
                    print "STMT"
                    if self.ctx.has_key("temp"+str(tempName)):
                        print "ZOMFG"
                    self._putConnection(x, ast.Other(y.ident \
                                                    ,'in'    \
                                                    ,"temp"+str(tempName)))
                else:
                    self._putConnection(x, ast.Other(y.ident \
                                                    ,'in'    \
                                                    ,t.component.ident))
            self.f.write("\n")
                
        elif type(t) == ast.Connection:
            self._putConnection(t.left,t.right)
            
        elif type(t) == ast.Atom:
            self._putController(t.options)
            
        #elif t[0] == 'CONTROLLER':
        #    putController(t[1])

        else:
            pass
