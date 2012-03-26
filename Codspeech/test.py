

import codspeech.parser.csparser  as parser
import codspeech.ast.csast as csast
import codspeech.typechecker.cstypechecker_visitor as cstv


# --------------------------------------------------------------
# test functions
# --------------------------------------------------------------
def test(filepath):
    p = parser.CodspeechParser()
    try:
        buffer = open(filepath)
    except IOError, e:
        raise e
    else:
        prog = buffer.read()
        return p.parse(prog, filepath)

ast = test('examples/example3.cod')
t = cstv.TypeChecker(debug=True)
#ctx = t.typecheck(ast)