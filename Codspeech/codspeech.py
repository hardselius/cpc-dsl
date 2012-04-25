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

from codspeech.parser.csparser import CodspeechParser

from codspeech.typechecker.cstypechecker import TypeChecker
from codspeech.xml.cstoxml import XMLGenerator



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
        '-o',
        nargs  = 1,
        type   = argparse.FileType('wt'),
        action = 'store',
        dest   = 'xml',
        help   = 'output XML to this file')
    parser.add_argument(
        '-f',
        nargs=1,
        type = file,
        dest = 'file',
        help = 'input Codspeech file')

    args = parser.parse_args()

    if (args.file):
        cs_file = CodspeechFile(
            file         = args.file[0],
            print_ast    = args.ast,
            do_typecheck = True,
            gen_xml      = args.xml)
    else:
        parser.print_help()


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
#    parser.print_help()

    
def print_header(s,f):
    print "\n\t{1} - {0}:\n".format(s,f)


class CodspeechFile(object):
    def __init__(
        self,
        file,
        print_ast = False,
        do_typecheck = False,
        gen_xml = None):

        self.file    = file
        self.ast     = None
        self.text    = None
        self.context = None
        self.newtype = None
        self.arrays  = None

        if not self.file.name.endswith('.cod'):
            raise IOError('%s is not a Codspeech file.' % file.name)
        else:
            self.text = self.file.read()
        
        self._parse_file()
        if print_ast: self.ast.show()
        if do_typecheck: self._typecheck_ast()
        if gen_xml: self._generate_xml(gen_xml[0])

    def _parse_file(self):
        """Parse a Codspeech file using csparser.

        When successful, an AST is set. ParseError can be thrown if
        the file does not parse successfully.

        """
        parser   = CodspeechParser()
        self.ast = parser.parse(self.text, self.file.name)


    def _typecheck_ast(self):
        """Type check an abstract syntax tree using cstypechecker.

        When successful, a context, new types set,
        and an new array list is set.
        TypeError and RefError can be thrown if the ast does not
        typecheck successfully.

        """
        tc = TypeChecker()
        tc.typecheck(self.ast)
        self.context  = tc.getEnv()
        self.newtypes = tc.newtypes
        self.arrays   = tc.arrays


    def _generate_xml(self,file):
        """Type check an abstract syntax tree using cstypechecker.

        Keyword arguments:
        'file' is where the XML code will be written

        """
        xmlgen = XMLGenerator()
        xmlgen.generateXML(
            ast    = self.ast,
            ctx    = self.context,
            types  = self.newtypes,
            arrays = self.arrays,
            file   = file)


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
