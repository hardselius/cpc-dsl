

import codspeech.parser.csparser  as parser
import codspeech.ast.csast as csast
import codspeech.typechecker.cstypechecker as cstc


# --------------------------------------------------------------
# test functions
# --------------------------------------------------------------
def parse(filepath):
    p = parser.CodspeechParser()
    try:
        buffer = open(filepath)
    except IOError, e:
        raise e
    else:
        prog = buffer.read()
        return p.parse(prog, filepath)

def test():
    ast = parse('examples/example3.cod')
    t = cstc.TypeChecker(debug=True)
    return ast, t
