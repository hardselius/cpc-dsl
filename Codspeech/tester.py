import sys
sys.path.insert(0,"../..")

import copy
import codspeech.parser.csparser as csparse

import codspeech.typechecker.cstypechecker_visitor as cstype
import codspeech.xml.cstoxml_visitor as xml


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
  ast = parser.parse(x)
  if ast != None:
    if past:
      print "Abstrac syntax tree:"
      print ast
      print ""
    try:
      env = tc.typecheck(ast)
    except cstype.TypeError as e:
      print "Type Error" + str(e)
    except cstype.ReferenceError as e:
      print "Reference Error" + str(e)
    else:
      if pctx:
        print "Context:"
        print env
      gXML = xml.XMLGenerator()
      gXML.generateXML(ast,env)
  else:
    print "No abstract syntax tree was generated."

test('examples/example3.cod')
