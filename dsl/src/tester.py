import sys
sys.path.insert(0,"../..")

import codspeechlexer as cslex
import codspeechparser as csparse
import codspeechtypechecker as cstype
import codspeechtoxml as xml
import copy

example1 = '../examples/example1.cod'

past = False
pctx = False

args = copy.copy(sys.argv)
args.pop(0)

for arg in args:
  if arg == 'ast':
    past = True
  elif arg == 'ctx':
    pctx = True
  else:
    print arg + ": Unkown option will be ignored"


def test(testfile):
  global past
  global pctx
  f = open(testfile)
  x = f.read()
  cslex.lexer.lineno = 1
  ast = csparse.parse(x)
  csparse.parser.restart()
  if ast != None:
    if past:
      print "Abstrac syntax tree:"
      print ast
      print ""
    env = cstype.typecheck(ast)
    if env != None:
      if pctx:
        print "Context:"
        print env
      xml.generateXML(ast,env)
    else:
      print "No context was generated."
  else:
    print "No abstract syntax tree was generated."

test('../examples/example2.cod')
