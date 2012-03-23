

import codspeech.parser.csparser  as parser
import codspeech.ast.csast as csast


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

t = test('examples/example3.cod')