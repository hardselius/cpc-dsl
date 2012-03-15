import copy

import sys
sys.path.insert(0,"../..")

#---------------------------------------------------------------------
# Environment
#---------------------------------------------------------------------

env = [{}]
error = 0

# Close scope
def pop():
  env.pop()

# Open new scope
def put():
  env.append(copy.copy(env[len(env)-1]))

# Add (Iden,Type) to the environment
def add(ident,type):
  global error
  if varExist(ident[1]):
     print "%s REFERENCE ERROR[variable already exists]: %s" \
           % (ident[2],ident[1])
     error = 1
  else:
    env[len(env)-1][ident[1]] = type

# Return the type of an Ident
def type(ident):
  global error
  try:
    if len(ident) == 1:
      return env[len(env)-1][ident[0][1]]
    elif len(ident) == 2:
      return env[len(env)-1][ident[0]][ident[1][1]]
    else:
      return typeParams(env[len(env)-1][ident[0][1]][ident[1]] \
                       ,ident[2][1])
  except KeyError:
    print "%s REFERENCE ERROR[variable not found]: %s" \
          % (ident[len(ident)-1][2],ident[len(ident)-1][1])
    error = 1

# Returns type of a parameter 'p' from a list of parameters
def typeParams(params,p):
  for x in params:
    if x[1] == p: return x[0]

# Returns if variable exists in environment
def varExist(var):
  return env[len(env)-1].has_key(var)

# Add parameter to input/output record
def addParam(io,param):
  global error
  if env[len(env)-1][io].has_key(param[1][1]):
    print "%s REFERENCE ERROR[variable already exists]: %s" \
          % (param[1][2],param[1][1])
    error = 1
  else:
    env[len(env)-1][io][param[1][1]] = param[0]

#---------------------------------------------------------------------
# Type Check
#---------------------------------------------------------------------

def typecheck(t):
  global error
  global env

  # Nothing to check
  if t == []:
    pass

  # Program: check import, components
  elif t[0] == 'PROGRAM':
    map(typecheck,t[1])
    map(typecheck,t[2])
    ctx = copy.copy(env)
    env = [{}]
    if error == 0: return ctx

  # Network: check controller, network block
  elif t[0] == 'NETWORK':
    typecheck(t[1])
    map(typecheck,t[2])

  # Component: check paramaters, network/atom
  elif t[0] == 'COMPONENT':
    pType = lambda x: [x[0],x[1][1]]
    add(t[1],{'in':map(pType,t[3]),'out':map(pType,t[4])})
    put()
    add(['IDENT','in'],{})
    add(['IDENT','out'],{})
    map(lambda x:addParam('in',x),t[3])
    map(lambda x:addParam('out',x),t[4])
    typecheck(t[5])
    pop()

  # Assignment: check component, argument
  elif t[0] == 'ASSIGNMENT':
    add(t[1],type([t[2]]))
    if error == 0:
      args = type([t[2]])['in']
      for i in range(len(t[3])):
        if i < len(args):
          if type(t[3][i]) != args[i][0]:
            print "%s TYPE ERROR[assignment]: %s:%s, %s:%s" \
                  % (t[3][i][len(t[3][i])-1][2] \
                    ,t[3][i][len(t[3][i])-1][1] \
                    ,type(t[3][i]) \
                    ,args[i][1][1],args[i][0])
            error = 1
        else:
          print "%s REFERENCE ERROR[input out of bounds]: %s" \
                % (t[3][i][len(t[3][i])-1][2] \
                  ,t[3][i][len(t[3][i])-1][1])
          error = 1

  # Connection: check variables
  elif t[0] == 'CONNECTION':
    if type(t[1]) != type(t[2]):
      if error == 0:
        print "%s TYPE ERROR[connection]: %s:%s, %s:%s" \
              % (t[2][len(t[2])-1][2]                   \
                ,t[1][len(t[1])-1][1],type(t[1])     \
                ,t[2][len(t[2])-1][1],type(t[2]))
        error = 1

  # Atom: check FUNCTION DEFINITION
  elif t[0] == 'ATOM':
    pass

  # Controller: check variable, component
  elif t[0] == 'CONTROLLER':
    add(t[2],type([t[1]]))

  # Something is missing
  else:
    pass
