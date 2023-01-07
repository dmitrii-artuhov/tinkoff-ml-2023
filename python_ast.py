import ast

class PythonAST:
    def __init__(self, filename):
        ''' Creates empty AST '''
        self.load(filename)

    def load(self, filename):
        ''' Loads AST from python file '''
        py_file = open(filename).read()
        self.ast = ast.parse(py_file)

    def parse(self, programm):
        ''' Generates AST from python programm text '''
        self.ast = ast.parse(programm)
    
    def get_ast(self):
        return self.ast
    
    def get_programm_text(self):
        return ast.unparse(self.ast)
    
    def stringify(self):
        return ast.dump(self.ast, indent = 4)