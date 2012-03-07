import copy

import sys
sys.path.insert(0,"../..")

import codspeechlexer
import codspeechparser
import ply.yacc as yacc

tokens = codspeechlexer.tokens

#-------------------------------------------------------------------------------
# Envorinment
#-------------------------------------------------------------------------------

env = [{}]
error = 0

def pop():
  env.pop()

def put():
  env.append(copy.copy(env[len(env)-1]))

def add(ident,type):
  if varExist(ident):
     return True
  else:
    env[len(env)-1][ident] = type
    return False

def type(ident):
  return env[len(env)-1][ident]

def varExist(var):
  return env[len(env)-1].has_key(var)

#-------------------------------------------------------------------------------
# Type Check
#-------------------------------------------------------------------------------

def addArg(arg):
  if add(arg[1],arg[0]):
    print "REFERENCE ERROR[variable already exists] at line %s: %s" \
          % (arg[2],arg[1])
    error = 1

def typecheck(t):
  global error
  if t == []:
    pass

  elif t[0] == 'PROGRAM':
#    map(typecheck,t[1])
    map(typecheck,t[2])

  elif t[0] == 'NETWORK':
    typecheck(t[1])
    map(typecheck,t[2])

  elif t[0] == 'COMPONENT':
    add(t[1],[t[3],t[4]])
    put()
    map(addArg,t[3])
    map(addArg,t[4])
    typecheck(t[5])
    pop()

  elif t[0] == 'ASSIGNMENT':
    try:
      if add(t[1],type(t[2])):
         print "REFERENCE ERROR[variable already exists] at line %s: %s" \
               % (t[4],t[1])
         error = 1
      args = type(t[1])[0]
      for i in range(len(t[3])):
        if i < len(args):
          if type(t[3][i][1]) != args[i][0]:
            print "TYPE ERROR[assignment] at line %s: %s:%s, %s:%s" \
                  % (t[4],t[3][i][1],type(t[3][i][1]),args[i][1],args[i][0])
            error = 1
        else:
          print "REFERENCE ERROR[input out of bounds] at line ?: %s" \
                % t[3][i][1]
          error = 1
    except KeyError:
      print "REFERENCE ERROR[variable not found] at line %s: %s" \
            % (t[3],sys.exc_value)
      error = 1

  elif t[0] == 'CONNECT':
    try:
      if type(t[1]) != type(t[2]):
        print "TYPE ERROR[connection] at line %s: %s:%s, %s:%s" \
              % (t[3],t[1],type(t[1]),t[2],type(t[2]))
        error = 1
    except KeyError:
      print "REFERENCE ERROR[variable not found] at line %s: %s" \
            % (t[3],sys.exc_value)
      error = 1

  elif t[0] == 'ATOM':
    pass

  elif t[0] == 'CONTROLLER':
    try:
      add(t[2],type(t[1]))
    except KeyError:
      print "REFERENCE ERROR[variable not found] at line %s: %s" \
            % (t[3],sys.exc_value)
      error = 1

  else:
    pass


def test():
  t = codspeechparser.test()
  print t
  print ""
  if t != None:
    typecheck(t)
    if error == 0: print env

test()
