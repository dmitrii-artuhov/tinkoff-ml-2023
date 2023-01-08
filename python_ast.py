import ast
from ast_transformer import UnificationTranformer, NameCollectingVisitor

class PythonAST:
    def __init__(self, filename):
        ''' Creates empty AST '''
        self.load(filename)

    def load(self, filename):
        ''' Loads AST from python file '''
        print(f"Opening file {filename!r}")
        py_file = open(filename).read()
        self.ast = ast.parse(py_file)

    def parse(self, programm):
        ''' Generates AST from python programm text '''
        self.ast = ast.parse(programm)
    
    def get_ast(self):
        return self.ast
    
    def unify_ast(self):
        names: NameCollectingVisitor = NameCollectingVisitor(self.ast)
        self.ast: ast = UnificationTranformer(names.variable_names, names.arg_names, names.function_names).visit(self.ast)

    
    def get_programm_text(self):
        return ast.unparse(self.ast)
    
    def stringify(self):
        return ast.dump(self.ast, indent = 4)