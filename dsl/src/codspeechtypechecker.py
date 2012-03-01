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
  if   t    == []:
    pass
  elif t[0] == 'IMPORT':
    pass
  elif t[0] == 'PROGRAM':
    map(typecheck,t[1])
  elif t[0] == 'NETWORK':
    map(typecheck,t[1])
  elif t[0] == 'COMPONENT':
#    print('COMPONENT')
#    print(env)
    add(t[1],'Component')
    put()
    add(t[1],'Component')
    typecheck(t[3])
    typecheck(t[4])
    typecheck(t[5])
#    print(env)
    pop()
  elif t[0] == 'ATOM':
    pass
  elif t[0] == 'CONTROLLER':
    pass
  elif t[0] == 'CONNECT':
    pass
  elif t[0] == 'ASSIGN':
    add(t[1],'Component')
  elif t[0] == 'in':
    map(lambda x:add('in.'+x[1],x[0]),t[1])
  elif t[0] == 'out':
    map(lambda x:add('out.'+x[1],x[0]),t[1])
  else:
    pass

def test():
  t = codspeechparser.test()
  print(t)
  typecheck(t)
  print(env)

test()
