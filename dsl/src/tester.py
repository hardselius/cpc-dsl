import sys
sys.path.insert(0,"../..")

import codspeechparser as parser
import codspeechtypechecker as tc

def test(testfile):
  f = open(testfile)
  x = f.read()
  ast = parser.parse(x)
  parser.parser.restart()
  print ast
  print ""
  if ast != None:
    env = tc.typecheck(ast)
    if env != None: print env

test('../examples/example1.cod')
