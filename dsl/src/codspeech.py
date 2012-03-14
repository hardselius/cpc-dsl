import sys
sys.path.insert(0,"../..")

import codspeechlexer  as cslex
import codspeechparser as csparse

lexer  = cslex.lex.lex(module=cslex)
parser = csparse.yacc.yacc(module=csparse)

cslex.lex.


def read_input(filepath):
  f = open(filepath)
  s = f.read()
  return s

def get_tokens(code):
  lexer.
  lexer.lineno = 1
  lexer.input(code)
  while 1:
    t = lexer.token()
    if not t:
      break
      print '\t' + str(t)

def get_ast(code):
  lexer.lineno = 1
  parser.error = 0
  p = parser.parse(code)
  if parser.error:
    return None
  return p


import optparse

def main(*args):
  cmdparser = optparse.OptionParser(usage='%prog [options] <arg1>',
                                    prog = 'codspeech')
  cmdparser.add_option(
    '-t', '--tokens',
    action='store_true',
    dest='token',
    default=False
  )
  cmdparser.add_option(
    '-a', '--abstract-syntax-tree',
    action='store_true',
    dest='ast',
    default=False
  )

  options, args = cmdparser.parse_args(*args)
#  if not args:
#    cmdparser.parse_args(['--help'])
#    return None
#  else:
#    code = read_input(args[0])
#    print '\n\n' + 'CODSPEECH OUTPUT:' + '\n'
#    if options.token:
#      print '\n' + 'Tokens:' + '\n'
#      get_tokens(code)
#      if options.ast:
#        print '\n' + 'Abstract Syntax Tree:' + '\n'
#        print get_ast(code)
#        return None

if __name__ == '__main__':
  main()









args1 = ['-f','../examplesexample2.cod']
args2 = ['-a','-f','../examplesexample2.cod']
args3 = ['--tokens','--abstract-syntax-tree','-f','../examplesexample2.cod']
