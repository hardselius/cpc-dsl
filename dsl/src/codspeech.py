#!/usr/bin/python
# ------------------------------------------------------------------
# codspeech: codspeech.py
#
# This is the command line tool for using Codspeech.
#
# Copyright (C) 2012, Martin Hardselius, Viktor Almqvist
# License:
# ------------------------------------------------------------------

import sys
import os
import optparse

from codspeechparser import CodspeechParser

import codspeechtypechecker as cstype
import codspeechtoxml       as csxml


def parse_file(filename):
    """Parse a Codspeech file using codspeechparser.

    Keyword arguments:
    filename -- Name of the file to parse.

    When successful, an AST is returned. ParseError can be thrown if
    the file does not parse successfully.

    """
    text = open(filename, 'rU').read()
    parser = CodspeechParser()
    return parser.parse(text, filename)
    

# ------------------------------------------------------------------
# Codspeech main program
# ------------------------------------------------------------------
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

    query_options   = optparse.OptionGroup(
        cmdparser, 'Query Options',
        'These options control the query mode.'
    )
    query_options.add_option(
        '-l', '--lex',
        action   = 'store_true',
        dest     = 'lex',
        default  = False,
        help     = 'Print the output from the tokenized file <arg1>.'
    )
    query_options.add_option(
        '-a', '--ast',
        action   = 'store_true',
        dest     = 'ast',
        default  = False,
        help     = 'Print the Abstract Syntax Tree.'
    )
    cmdparser.add_option_group(query_options)

    compile_options = optparse.OptionGroup(
        cmdparser, 'Compile Options',
        'These options control compilation'
    )
    compile_options.add_option(
        '-t', '--typecheck',
        action   = 'store_true',
        dest     = 'typecheck',
        default  = False,
        help     = 'Check the program for type errors.'        
    )
    compile_options.add_option(
        '--xml',
        action   = 'store_true',
        dest     = 'xml',
        default  = 'False',
        #metavar  = 'FILE.xml',
        help     = 'Generate an xml representation of the program.'
    )
    cmdparser.add_option_group(compile_options)
    
    options, arguments = cmdparser.parse_args(*args)
    filePath  = None # /path/to/file.ext
    fileName  = None # /path/to/file
    fileExt   = None # .ext
    program   = None # Contents of read file
    ast       = None # Abstract Syntax Tree
    ctx       = None # Context after typechecking
    
    if len(arguments) != 1:
        print "Program called with no arguments or flags.\n"
        cmdparser.print_help()
        return None
    else:
        filePath = arguments[0]
        fileName, fileExt = os.path.splitext(filePath)
        if fileExt != '.cod':
            print filePath + " is not a .cod-file"
            pass
        try:
            buffer = open(filePath)
        except IOError:
            print "Error: No such file or directory: '%s'" % filePath, "\n"
            cmdparser.print_help()
        else:
            program = buffer.read()

    if options.lex:
        print_header('Tokens',filePath)
        get_tokens(program)
        
    if options.ast:
        print_header('Abstract Syntax Tree',filePath)
        ast = get_ast(program)
        print ast

    if options.typecheck:
        if not ast: ast = get_ast(program)
        ctx = cstype.typecheck(ast)
        print_header('Typecheck',filePath)
        if not ctx:
            print "Typechecking failed!"
        else:
            print ctx
            print "Typechecking passed. Everything correct."

    if options.xml:
        if not ast: ast = get_ast(program)
        if not ctx: ctx = cstype.typecheck(ast)
        print_header('Generate XML',filePath)
        csxml.generateXML(ast,ctx,(fileName + '.xml'))
        print "... Wrote %s" % (fileName + '.xml')

    pass
        
def print_header(s,f):
    print "\n\t{1} - {0}:\n".format(s,f)

        
if __name__ == '__main__':
    main()
