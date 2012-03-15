import sys
sys.path.insert(0,"../..")

#---------------------------------------------------------------------
# Settings/Global variables
#---------------------------------------------------------------------

indent = "    "

def ind():
  global indent
  indent += "    "

def unind():
  global indent
  indent = indent[:len(indent)-4]

ctx = {}

f = None
file = "output.xml"

#---------------------------------------------------------------------
# Write XML functions
#---------------------------------------------------------------------

def init():
  global f
  f = open(file,"w")
  f.write("<?xml version=\"1.0\" ?>\n<cpc>\n")

def end():
  f.write("</cpc>\n")
  f.close()

def startFun(id,type):
  f.write(indent + "<function id=\"" + id + "\" type=\"" + type + "\">\n")
  ind()

def endFun():
  unind()
  f.write(indent + "</function>\n")

def startInput():
  f.write(indent + "<inputs>\n")
  ind()

def endInput():
  unind()
  f.write(indent + "</inputs>\n")

def startOutput():
  f.write(indent + "<outputs>\n")
  ind()

def endOutput():
  unind()
  f.write(indent + "</outputs>\n")

def putParam(param):
  if param[2] == []:
    f.write(indent + "<field type=\"" + param[0].lower() \
                   + "\" id=\"" + param[1][1] + "\"/>\n")
  else:
    f.write(indent + "<field type=\"" + param[0].lower() \
                   + "\" id=\"" + param[1][1] + "\">\n")
    ind()
    putDesc(param[2])
    unind()
    f.write(indent + "</field>\n")

def putDesc(desc):
  if desc != []:
    f.write(indent + "<desc>" + desc + "</desc>\n")

def putController(fun,module = None):
  if module == None:
    f.write(indent + "<controller function=\"" + showIdent(fun) + "\" />\n")
  else:
    f.write(indent + "<controller function=\"" + module \
                                  + "." + showIdent(fun) + "\"\n"  \
          + indent + "            import=\"" +  module + "\" />\n")

def putImport(module):
  f.write(indent + "<import name=\"" + module + "\" />\n")

def startNet():
  f.write(indent + "<network>\n")
  ind()

def endNet():
  unind()
  f.write(indent + "</network>\n")

def putConnection(src,dest):
  f.write(indent + "<connection src=\"" + showIdent(src) + "\" dest=\"" \
                                        + showIdent(dest) + "\" />\n")

def putInstance(id,fun):
  f.write(indent + "<instance id=\"" + showIdent(id) \
                 + "\" function=\"" + showIdent(fun) \
                 + "\" />\n")

def showIdent(i):
  if i[0] == 'IDENT':
    return i[1]
  elif len(i) == 1:
    return i[0][1]
  elif len(i) == 2:
    x = i.pop(0)
    return "self:ext_" + x + "." + showIdent(i)
  else:
    return i[0][1] + ":" + i[1] + "." + i[2][1]

#---------------------------------------------------------------------
# Build a cpc XML from abstract syntax tree
#---------------------------------------------------------------------

def toXML(t):
  if t == []:
    pass

  elif t[0] == 'IMPORT':
#    putImport('.'.join(t[1]))
    pass

  elif t[0] == 'PROGRAM':
    init()
    map(toXML,t[1])
    map(toXML,t[2])
    end()  

  elif t[0] == 'NETWORK':
    startNet()
    toXML(t[1])
    map(toXML,t[2])
    endNet()

  elif t[0] == 'COMPONENT':
    if t[5][0] == 'NETWORK':
      startFun(t[1][1],"network")
    else:
      startFun(t[1][1],"python-extended")
    putDesc(t[2])
    startInput()
    map(putParam,t[3])
    endInput()
    startOutput()
    map(putParam,t[4])
    endOutput()
    toXML(t[5])
    endFun()

  elif t[0] == 'ASSIGNMENT':
    putInstance(t[1],t[2])
    for i in range(len(t[3])):
      putConnection(t[3][i], [['',t[2][1]],'in',ctx[t[2][1]]['in'][i]])
    f.write("\n")

  elif t[0] == 'CONNECTION':
    putConnection(t[1],t[2])

  elif t[0] == 'ATOM':
    putController(t[2],t[1])

  elif t[0] == 'CONTROLLER':
    putController(t[1])

  else:
    pass
