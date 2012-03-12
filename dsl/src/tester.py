import sys
sys.path.insert(0,"../..")

import codspeechlexer as cslex
import codspeechparser as csparse
import codspeechtypechecker as cstype

example1 = '../examples/example1.cod'

#def tokenize(file):
#  f = open(file)
#  r = f.read()



def test(testfile):
  f = open(testfile)
  x = f.read()
  ast = csparse.parse(x)
  csparse.parser.restart()
  if ast != None:
    print "Abstrac syntax tree:"
    print ast
    print ""
    env = cstype.typecheck(ast)
    if env != None:
      print "Context:"
      print env
    else:
      print "No context was generated."
  else:
    print "No abstract syntax tree was generated."

test('../examples/example2.cod')
