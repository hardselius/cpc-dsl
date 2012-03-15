#!/usr/bin/python

import sys
sys.path.insert(0,"../..")

import os
import codspeechlexer       as cslex
import codspeechparser      as csparse
import codspeechtypechecker as cstype
import codspeechtoxml       as csxml

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
        action   = 'store_true',
        dest     = 'xml',
        default  = 'False',
        #metavar  = 'FILE.xml',
        help     = 'Generate an xml representation of the program.'
    )
    cmdparser.add_option_group(compile_opts)

    opts, args = cmdparser.parse_args(*args)
    filePath   = None # /path/to/file.ext
    fileName   = None # /path/to/file
    fileExt    = None # .ext
    program    = None # Contents of read file
    ast        = None # Abstract Syntax Tree
    ctx        = None # Context after typechecking
    
    if len(args) != 1:
        cmdparser.print_help()
    else:
        filePath = args[0]
        fileName, fileExt = os.path.splitext(filePath)
        if fileExt != '.cod':
            print filePath + " is not a .cod-file"
            pass
        try:
            buffer = open(filePath)
            program = buffer.read()
            buffer.close()
        except IOError:
            print "Error: No such file or directory: '%s'" % filePath, "\n"
            cmdparser.print_help()
            

    if opts.lex:
        print_header('Tokens',filePath)
        get_tokens(program)
        
    if opts.ast:
        print_header('Abstract Syntax Tree',filePath)
        ast = get_ast(program)
        print ast

    if opts.typecheck:
        if not ast: ast = get_ast(program)
        ctx = cstype.typecheck(ast)
        print_header('Typecheck',filePath)
        if not ctx:
            print "Typechecking failed"
        else:
            print ctx
            print "Typechecking passed. Everything correct."

    if opts.xml:
        if not ast: ast = get_ast(program)
        if not ctx: ctx = cstype.typecheck(ast)
        print_header('Generate XML',filePath)
        csxml.generateXML(ast,ctx,(fileName + '.xml'))
        print "... Wrote %s" % (fileName + '.xml')
        
def print_header(s,f):
    print "\n\t{1} - {0}:\n".format(s,f)

        
if __name__ == '__main__':
    main()
