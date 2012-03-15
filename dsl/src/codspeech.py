#!/usr/bin/python

import sys
sys.path.insert(0,"../..")

import os
import codspeechlexer  as cslex
import codspeechparser as csparse

lexer  = cslex.lex.lex(module=cslex)
parser = csparse.yacc.yacc(module=csparse)


def get_tokens(code):
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


args1 = ['-f','../examplesexample2.cod']
args2 = ['-a','-f','../examplesexample2.cod']
args3 = ['--tokens','--abstract-syntax-tree','-f','../examplesexample2.cod']





# ------------------------------------------------------------------
# Codspeech main program
# ------------------------------------------------------------------

import optparse

desc = """This is a description of %prog, the amazing compiler for the
Domain Specific Language \'CODSPEECH\'.

"""
def main(*args):
    cmdparser    = optparse.OptionParser(
        description = desc,
        usage    = '%prog [options] <arg1>',
        prog     = 'codspeech'
    )
    cmdparser.add_option(
        '-q',
        action   = 'store_const',
        const    = 'query',
        dest     = 'mode',
        help     = 'Query'
    )
    cmdparser.add_option(
        '-c',
        action   = 'store_const',
        const    = 'compile',
        dest     = 'mode',
        help     = 'Compile'
    )

    query_opts   = optparse.OptionGroup(
        cmdparser, 'Query Options',
        'These options control the query mode.'
    )
    query_opts.add_option(
        '-l', '--lex',
        action   = 'store_true',
        dest     = 'lex',
        default  = False,
        help     = 'Print the output from the tokenized file <arg1>.'
    )
    query_opts.add_option(
        '-a', '--ast',
        action   = 'store_true',
        dest     = 'ast',
        default  = False,
        help     = 'Print the Abstract Syntax Tree.'
    )
    cmdparser.add_option_group(query_opts)

    compile_opts = optparse.OptionGroup(
        cmdparser, 'Compile Options',
        'These options control compilation'
    )
    compile_opts.add_option(
        '-t', '--typecheck',
        action   = 'store_true',
        dest     = 'typecheck',
        default  = False,
        help     = 'Check the program for type errors.'        
    )
    compile_opts.add_option(
        '--xml',
        action   = 'store',
        dest     = 'xml',
        default  = 'lol',
        metavar  = 'FILE.xml',
        help     = 'Generate an xml representation of the program.'
    )
    cmdparser.add_option_group(compile_opts)

    opts, args = cmdparser.parse_args(*args)
    program = ''
    
    if len(args) != 1:
        cmdparser.print_help()
    else:
        try:
            buffer = open(args[0])            
        except IOError:
            print "Error: No such file or directory: '%s'" % args[0], "\n"
            cmdparser.print_help()
        else:
            program = buffer.read()

    if opts.lex:
        print_header('Tokens',args[0])
        get_tokens(program)
        print '-' * 68 + '\n'
        
    if opts.ast:
        print_header('Abstract Syntax Tree',args[0])
        print get_ast(program)
        print '-' * 68 + '\n'
        
        
def print_header(s,f):
    print '-' * 68
    print "\t{1}: {0}".format(s,f)
    print '-' * 68 + '\n'

        
if __name__ == '__main__':
    main()
