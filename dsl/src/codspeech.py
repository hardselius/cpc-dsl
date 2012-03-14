import sys
sys.path.insert(0,"../..")

import codspeechlexer  as cslex
import codspeechparser as csparse

lexer  = cslex.lex.lex(module=cslex)
parser = csparse.yacc.yacc(module=csparse)

def read_input(filepath):
  f = open(path)
  s = f.read()
  return s

def get_tokens(code):
    lexer.lineno = 1
    lexer.input(s)
    while 1:
        t = lexer.token()
        if not t:
            break
        print t

def get_ast(code):
    lexer.lineno = 1
    parser.error = 0
    p = parser.parse(s)
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
  cmdparser.add_option(
    '-f', '--filename',
    metavar='FILE',
    help='input FILE'
  )

  options, args = cmdparser.parse_args(*args)

  print '\n\n Codspeech output:\n'
  print options.token
  print options.ast
  print options.filename
  print args
  
  

if __name__ == '__main__':
  main()









args1 = ['-f','../examplesexample2.cod']
args2 = ['-a','-f','../examplesexample2.cod']
args3 = ['--tokens','--abstract-syntax-tree','-f','../examplesexample2.cod']