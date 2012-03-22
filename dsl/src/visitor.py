import codspeechparser_alt as cspa
from codspeech_ast import NodeVisitor

class TypeChecker(NodeVisitor):
    def __init__(self):
        self.components = [{}]
        self.temp = None


    def visit_Component(self, node):
        self.components[-1][node.name.id] = {
            'in'  : [{}],
            'out' : [{}]
        }
        self.temp = node.name.id
        visit(node.in_params)

    def visit_InParam(self, node):
        self.components[-1][self.temp]['in'][-1][node.name.id] = node.type.type

    def visit_OutParam(self, node):
        pass
      

ast = cspa.test('../examples/example3.cod')
tc = TypeChecker()
