# ------------------------------------------------------------------
# Codspeech/codspeech/xml: cstoxml.py
#
# An xml generator for Codspeech
# ------------------------------------------------------------------


import copy

class XMLGenerator:
  def __init__(self,ind = 4):
    self.i = ind
    self.indent = ' '*ind
    self.ctx = None
    self.f = None

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
    self.f.write(self.indent + "<field type=\"" + param[0].lower() \
                             + "\" id=\"" + param[1][1] + "\"")
    if param[2] == []:
      self.f.write(" />\n")
    elif param[2] != 'OPTIONAL':
      self.f.write(">\n")
      self._ind()
      self._putDesc(param[2])
      self._unind()
      self.f.write(self.indent + "</field>\n")
    else:
      self.f.write(" opt=\"true\"")
      if param[3] == []:
        self.f.write(" />\n")
      else:
        self.f.write(">\n")
        self._ind()
        self._putDesc(param[3])
        self._unind()
        self.f.write(self.indent + "</field>\n")

  def _putDesc(self,desc):
    if desc != []:
      self.f.write(self.indent + "<desc>" + desc + "</desc>\n")

  def _putController(self,opts):
    self.f.write(self.indent + "<controller ")
    for x in opts:
      self.f.write(x[0][1].translate(None, '"') + "=" + x[1][1])
      if x == opts[-1]:
        self.f.write(" />\n")
      else:
        self.f.write("\n" + self.indent + "            ")

  def _putImport(self,module):
    self.f.write(self.indent + "<import name=\"" + module + "\" />\n")

  def _startNet(self):
    self.f.write(self.indent + "<network>\n")
    self._ind()

  def _endNet(self):
    self._unind()
    self.f.write(self.indent + "</network>\n")

  def _putConnection(self,src,dest):
    self.f.write(self.indent + "<connection src=\""  \
               + self._showIdent(src) + "\" dest=\"" \
               + self._showIdent(dest) + "\" />\n")

  def _putInstance(self,id,fun):
    self.f.write(self.indent + "<instance id=\""        \
               + self._showIdent(id) + "\" function=\"" \
               + self._showIdent(fun) + "\" />\n")

  def _showIdent(a):
    if a[0] == 'THIS':
      return "self:ext_" + a[1] + "." + a[2][1]
    elif a[0] == 'OTHER':
      return a[1][1] + ":" + a[2] + "." + a[3][1]
    elif a[0] == 'COMP':
      return a[1][0][1] + ":" + a[2] + "." + a[3][1]
    else:
      return a[1]

#---------------------------------------------------------------------
# Build a cpc XML from abstract syntax tree
#---------------------------------------------------------------------
  def generateXML(self,ast,context,file = "output.xml"):
    self.ctx = context
    self.f = open(file,"w")
    self._toXML(ast)

  def _toXML(self,t):
    if t == []:
      pass

    #elif t[0] == 'IMPORT':
    #  putImport('.'.join(t[1]))

    elif t[0] == 'PROGRAM':
      self._init()
      map(self._toXML,t[1])
      map(self._toXML,t[2])
      self._end()  

    elif t[0] == 'NETWORK':
      self._startNet()
      self._toXML(t[1])
      map(self._toXML,t[2])
      self._endNet()

    elif t[0] == 'COMPONENT':
      if t[5][0] == 'NETWORK':
        self._startFun(t[1][1],"network")
      else:
        self._startFun(t[1][1],t[5][1])
        self._putDesc(t[2])
        self._startInput()
        map(self._putParam,t[3])
        self._endInput()
        self._startOutput()
        map(self._putParam,t[4])
        self._endOutput()
        self._toXML(t[5])
        self._endFun()

    elif t[0] == 'ASSIGNMENT':
      self._putInstance(t[1],t[2][0])
      args = copy.copy(self.ctx[t[2][0][1]]['in'])
      for x in t[2][1]:
        y = args.pop(0)
        self._putConnection(x, ['OTHER',t[2][0],'in',y[1]])
        self._f.write("\n")
        
    elif t[0] == 'CONNECTION':
      self._putConnection(t[1],t[2])
      
    elif t[0] == 'ATOM':
      self._putController(t[2])
      
      #elif t[0] == 'CONTROLLER':
      #  putController(t[1])

    else:
      pass
