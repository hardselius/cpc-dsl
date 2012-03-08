import copy

import sys
sys.path.insert(0,"../..")

#---------------------------------------------------------------------
# Environment
#---------------------------------------------------------------------

env = [{}]
error = 0

def pop():
  env.pop()

def put():
  env.append(copy.copy(env[len(env)-1]))

def add(ident,type):
  global error
  if varExist(ident[1]):
     print "%s REFERENCE ERROR[variable already exists]: %s" \
           % (ident[2],ident[1])
     error = 1
  else:
    env[len(env)-1][ident[1]] = type
    return False

def type(ident):
  global error
  try:
    return env[len(env)-1][ident[1]]
  except KeyError:
    print "%s REFERENCE ERROR[variable not found]: %s" \
          % (ident[2],ident[1])
    error = 1

def varExist(var):
  return env[len(env)-1].has_key(var)

#---------------------------------------------------------------------
# Type Check
#---------------------------------------------------------------------

def typecheck(t):
  global error

  # Nothing to check
  if t == []:
    pass

  # Program: check import, components
  elif t[0] == 'PROGRAM':
    map(typecheck,t[1])
    map(typecheck,t[2])
    if error == 0: return env

  # Network: check controller, network block
  elif t[0] == 'NETWORK':
    typecheck(t[1])
    map(typecheck,t[2])

  # Component: check paramaters, network/atom
  elif t[0] == 'COMPONENT':
    add(t[1],[t[3],t[4]])
    put()
    map(lambda x:add(x[1],x[0]),t[3]+t[4])
    typecheck(t[5])
    pop()

  # Assignment: check component, argument
  elif t[0] == 'ASSIGNMENT':
    add(t[1],type(t[2]))
    if error == 0:
      args = type(t[2])[0]
      for i in range(len(t[3])):
        if i < len(args):
          if type(t[3][i]) != args[i][0]:
            print "%s TYPE ERROR[assignment]: %s:%s, %s:%s" \
                  % (t[3][i][2],t[3][i][1],type(t[3][i])    \
                               ,args[i][1],args[i][0])
            error = 1
        else:
          print "%s REFERENCE ERROR[input out of bounds]: %s" \
                % (t[3][i][2],t[3][i][1])
          error = 1

  # Connection: check variables
  elif t[0] == 'CONNECTION':
    if type(t[1]) != type(t[2]):
      if error == 0:
        print "%s TYPE ERROR[connection]: %s:%s, %s:%s" \
              % (t[1][2],t[1][1],type(t[1]),t[2][1],type(t[2]))
        error = 1

  # Atom: check FUNCTION DEFINITION
  elif t[0] == 'ATOM':
    pass

  # Import: check path
  elif t[0] == 'IMPORT':
    pass

  # Controller: check variable, component
  elif t[0] == 'CONTROLLER':
    add(t[2],type(t[1]))

  # Something is missing
  else:
    pass
