import copy
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

ctx = None

f = None

#---------------------------------------------------------------------
# Write XML functions
#---------------------------------------------------------------------

def init():
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
  f.write(indent + "<field type=\"" + param[0].lower() \
                 + "\" id=\"" + param[1][1] + "\"")
  if param[2] == []:
    f.write(" />\n")
  elif param[2] != 'OPTIONAL':
    f.write(">\n")
    ind()
    putDesc(param[2])
    unind()
    f.write(indent + "</field>\n")
  else:
    f.write(" opt=\"true\"")
    if param[3] == []:
      f.write(" />\n")
    else:
      f.write(">\n")
      ind()
      putDesc(param[3])
      unind()
      f.write(indent + "</field>\n")

def putDesc(desc):
  if desc != []:
    f.write(indent + "<desc>" + desc + "</desc>\n")

def putController(opts):
  f.write(indent + "<controller ")
  for x in opts:
    f.write(x[0][1].translate(None, '"') + "=" + x[1][1])
    if x == opts[-1]:
      f.write(" />\n")
    else:
      f.write("\n" + indent + "            ")

def putImport(module):
  f.write(indent + "<import name=\"" + module + "\" />\n")

def startNet():
  f.write(indent + "<network>\n")
  ind()

def endNet():
  unind()
  f.write(indent + "</network>\n")

def putConnection(src,dest):
  print dest
  f.write(indent + "<connection src=\"" + showIdent(src) + "\" dest=\"" \
                                        + showIdent(dest) + "\" />\n")

def putInstance(id,fun):
  f.write(indent + "<instance id=\"" + showIdent(id) \
                 + "\" function=\"" + showIdent(fun) \
                 + "\" />\n")

def showIdent(a):
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
def generateXML(ast,context,file = "output.xml"):
  global ctx
  global f
  ctx = context
  f = open(file,"w")
  toXML(ast)

def toXML(t):
  if t == []:
    pass

#  elif t[0] == 'IMPORT':
#    putImport('.'.join(t[1]))

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
      startFun(t[1][1],t[5][1])
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
    putInstance(t[1],t[2][0])
    args = copy.copy(ctx[t[2][0][1]]['in'])
    for x in t[2][1]:
      y = args.pop(0)
      putConnection(x, ['OTHER',t[2][0],'in',y[1]])
    f.write("\n")

  elif t[0] == 'CONNECTION':
    putConnection(t[1],t[2])

  elif t[0] == 'ATOM':
    putController(t[2])

#  elif t[0] == 'CONTROLLER':
#    putController(t[1])

  else:
    pass
