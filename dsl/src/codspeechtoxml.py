import copy

import sys
sys.path.insert(0,"../..")

from xml.dom.minidom import Document

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

def putParam(id,type,desc = None):
  if desc == None:
    f.write(indent + "<field type=\"" + type.lower() \
                   + "\" id=\"" + id + "\"/>\n")
  else:
    f.write(indent + "<field type=\"" + type.lower() \
                   + "\" id=\"" + id + "\">\n")
    ind()
    putDesc(desc)
    unind()
    f.write(indent + "</field>\n")

def putDesc(desc):
  f.write(indent + "<desc>" + desc + "</desc>\n")

def putController(module,fun):
  f.write(indent + "<controller function=\"cpc.lib." \
                                + module + "."       \
                                + fun + "\"\n"       \
        + indent + "            import=\"cpc.lib." + module + "\" />\n")

def putImport(module):
  f.write(indent + "<import name=\"" + module + "\" />\n")

def startNet():
  f.write(indent + "<network>\n")
  ind()

def endNet():
  unind()
  f.write(indent + "</network>\n")

def putConnection(src,dest):
  f.write(indent + "<connection src=\"" + src + "\" dest=\"" \
                                        + dest + "\" />\n")

def putInstance(id,fun):
  f.write(indent + "<instance id=\"" + id + "\" function=\"" \
                                     + fun + "\" />\n")

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
    map(lambda x:putParam(x[1][1],x[0]),t[3])
    endInput()
    startOutput()
    map(lambda x:putParam(x[1][1],x[0]),t[4])
    endOutput()
    toXML(t[5])
    endFun()

  elif t[0] == 'ASSIGNMENT':
    putInstance(showIdent([t[1]]),showIdent([t[2]]))
    for i in range(len(t[3])):
      putConnection(showIdent(t[3][i]) \
                   ,showIdent([['',t[2][1]],'in',ctx[t[2][1]]['in'][i]]))
    f.write("\n")

  elif t[0] == 'CONNECTION':
    putConnection(showIdent(t[1]),showIdent(t[2]))

  elif t[0] == 'ATOM':
    putController(t[1],showIdent([t[2]]))

  elif t[0] == 'CONTROLLER':
    pass

  else:
    pass


def showIdent(i):
  if len(i) == 1:
    return i[0][1]
  elif len(i) == 2:
    x = i.pop(0)
    return "self:ext_" + x + "." + showIdent(i)
  else:
    return i[0][1] + ":" + i[1] + "." + i[2][1]
