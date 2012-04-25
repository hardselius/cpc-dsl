import sys
sys.path.insert(0,"../..")

import copy
import codspeech.parser.csparser as csparse

import codspeech.typechecker.cstypechecker as cstype
import codspeech.xml.cstoxml as xml


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
  tc = cstype.TypeChecker()
  parser = csparse.CodspeechParser()
  ast = parser.parse(x,testfile)
  if ast != None:
    if past:
      print "Abstrac syntax tree:"
      ast.show()
      print ""
    try:
      tc.typecheck(ast)
      env = tc.getEnv()
      arrays = tc.arrays
      newtypes = tc.newtypes
    except cstype.TypeError as e:
      print str(e)
    except cstype.ReferenceError as e:
      print str(e)
    else:
      if pctx:
        print "Context:"
        print env
      gXML = xml.XMLGenerator()
      gXML.generateXML(ast,env,newtypes,arrays)
  else:
    print "No abstract syntax tree was generated."

test('examples/addmul.cod')
