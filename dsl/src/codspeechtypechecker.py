import copy

import sys
sys.path.insert(0,"../..")

import codspeechlexer
import codspeechparser
import ply.yacc as yacc

tokens = codspeechlexer.tokens

################################################################################
# Envorinment

env = [{}]

def pop():
  env.pop()

def put():
  env.append({})

def add(ident,type):
  env[len(env)-1][ident] = type

def type(ident):
  return env[len(env)-1][ident]

################################################################################

def typecheck(t):
  if t == []:
    pass

  elif t[0] == 'PROGRAM':
    map(typecheck,t[1])

  elif t[0] == 'NETWORK':
    map(typecheck,t[2])
    map(typecheck,t[3])

  elif t[0] == 'COMPONENT':
    add(t[1],[t[3][1],t[4][1]])
    put()
    add(t[1],[t[3][1],t[4][1]])
    typecheck(t[3])
    typecheck(t[4])
    typecheck(t[5])
    pop()

  elif t[0] == 'in':
    map(lambda x:add(x[1],x[0]),t[1])

  elif t[0] == 'out':
    map(lambda x:add(x[1],x[0]),t[1])

  elif t[0] == 'ASSIGN':
    try:
      add(t[1],type(t[2][0]))
      t[2].pop(0)
      args = type(t[1])[0]
      for i in range(len(t[2])):
        if type(t[2][i]) != args[i][0]:
          print "Type error: %s:%s , %s:%s" \
                % (t[2][i],type(t[2][i]),args[i][1],args[i][0])
    except KeyError:
      print "Variable not found: %s" % sys.exc_value

  elif t[0] == 'CONNECT':
    try:
      if type(t[1]) != type(t[2]):
        print("POOP")
    except KeyError:
      print "Variable not found: %s" % sys.exc_value

  elif t[0] == 'ATOM':
    pass

  elif t[0] == 'CONTROLLER':
    pass

  else:
    pass


def test():
  t = codspeechparser.test()
  print t
  print '\n'
  typecheck(t)
  print env

test()
