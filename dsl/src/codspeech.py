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
import argparse
import textwrap

from codspeechparser import CodspeechParser

import codspeechtypechecker as cstype
import codspeechtoxml       as csxml



def main(*args):
    parser = argparse.ArgumentParser(
        prog        = 'codspeech',
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent(_DESCRIPTION),
        epilog = textwrap.dedent(_PLY_COPYRIGHT_NOTICE))
    parser.add_argument(
        '-a', '--ast',
        action      = 'store_true',
        dest        = 'ast',
        default     = False,
        help        = 'print the abstract syntax tree of FILE')
    parser.add_argument(
        '-f',
        nargs=1,
        type = file,
        dest = 'file',
        help = 'input Codspeech file')
#    )
#    cmdparser.add_option(
#        '-t','--typecheck',
#        action      = 'store_true',
#        dest        = 'typecheck',
#        default     = False,
#        help        = 'run <arg1> through the typechecker')

#    options, arguments = cmdparser.parse_args(*args)
#    
#    if len(arguments) != 1:
#        print "Program called with no arguments.\n"
#        cmdparser.print_help()
#        return None
#
#    cs_file = CodspeechFile(
#        file         = arguments[0],
#        build_ast    = options.ast,
#        do_typecheck = options.typecheck)
#
#    return None
    parser.print_help()
    
def print_header(s,f):
    print "\n\t{1} - {0}:\n".format(s,f)


class CodspeechFile(object):
    def __init__(
        self,
        filename,
        build_ast=False,
        do_typecheck=False):

        self.filename       = filename
        self.file           = None
        self.ext            = None
        self.ast            = None
        self.file, self.ext = os.path.splitext(filename)
        
        if ext != '.cod':
            raise IOError('%s is not a Codspeech file.')
        else:
            self._read_file()
        
        if build_ast: self.ast = self._parse_file
        if do_typecheck:
            if not self.ast: self.ast = self._parse_file
            pass

    def _read_file():
        self.text = open(this.filename, 'rU').read()


    def _parse_file():
        """Parse a Codspeech file using codspeechparser.

        Keyword arguments:
        filename -- Name of the file to parse.

        When successful, an AST is returned. ParseError can be thrown if
        the file does not parse successfully.

        """
        self.parser = CodspeechParser()
        self.ast    = parser.parse(text, filename)


_DESCRIPTION = \
'''
description:
This is a description of %prog, the amazing compiler for the Domain
Specific Language \'CODSPEECH\'.
'''

_PLY_COPYRIGHT_NOTICE = \
'''
notice:
The parser was built using PLY(Python Lex-Yacc)
Copyright (C)
2001-2011,
David M. Beazley (Dabeaz LLC) All rights reserved.
'''

if __name__ == '__main__':
    main()
