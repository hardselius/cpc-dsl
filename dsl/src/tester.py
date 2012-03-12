import sys
sys.path.insert(0,"../..")

import codspeechparser as parser
import codspeechtypechecker as tc

def test(testfile):
  f = open(testfile)
  x = f.read()
  ast = parser.parse(x)
  parser.parser.restart()
  if ast != None:
    print "Abstrac syntax tree:"
    print ast
    print ""
    env = tc.typecheck(ast)
    if env != None:
      print "Context:"
      print env
    else:
      print "No context was generated."
  else:
    print "No abstract syntax tree was generated."

test('../examples/example2.cod')
