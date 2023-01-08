import ast

class NameCollectingVisitor(ast.NodeVisitor):
    variable_names: dict
    function_names: dict
    arg_names: dict

    def __init__(self, node):
        self.function_names = dict()
        self.arg_names = dict()
        self.variable_names = dict()

        self.visit(node)
    
    def _update_names_container(self, node, names_container, names_label, attr_name):
        if (not (getattr(node, attr_name) in names_container)):
            names_container[getattr(node, attr_name)] = f"{names_label}_{len(names_container)}"
    
    # vars
    def visit_Assign(self, node):
        for target in node.targets:
            if (type(target) == ast.Name):
                self._update_names_container(target, self.variable_names, "var", "id")
        self.generic_visit(node)
        return node
    
    def visit_NamedExpr(self, node):
        if (type(node.target) == ast.Name):
            self._update_names_container(node.target, self.variable_names, "var", "id")
        self.generic_visit(node)
        return node
    
    def visit_AnnAssign(self, node):
        if (type(node.target) == ast.Name):
            self._update_names_container(node.target, self.variable_names, "var", "id")
        self.generic_visit(node)
        return node
    
    # funcs
    def visit_FunctionDef(self, node):
        self._update_names_container(node, self.function_names, "func", "name")
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node):
        self._update_names_container(node, self.function_names, "func", "name")
        self.generic_visit(node)
        return node
    
    # args
    def visit_arg(self, node):
        self._update_names_container(node, self.arg_names, "arg", "arg")
        self.generic_visit(node)
        return node

class UnificationTranformer(ast.NodeTransformer):
    def __init__(self, variable_names_: dict, arg_names_: dict, function_names_: dict):
        self.variable_names = variable_names_
        self.arg_names = arg_names_
        self.function_names = function_names_
        
        self.context: list(dict) = [dict()]

    def _tranform_node(self, node, names_container, attr_name):
        name = getattr(node, attr_name)
        new_name = name

        if (name in self.context[-1]):
            new_name = self.context[-1][name]
        elif (name in names_container):
            new_name = names_container[name]
        else:
            return node # don't want to make extra copy for no reason

        return type(node)(**{**node.__dict__, f"{attr_name}": new_name})

    # def _update_names_container(self, node, names_container, names_label, attr_name):
    #     if (not (getattr(node, attr_name) in names_container)):
    #         names_container[getattr(node, attr_name)] = f"{names_label}_{len(names_container)}"

    def _erase_docstring(self, node):
        if ast.get_docstring(node) != None and node.body and node.body[0]:
            # node.body[0].value = ast.Constant(value="")
            del node.body[0]

    def visit_Name(self, node):
        # self._update_names_container(node, self.variable_names, names_label="var", attr_name="id")
        self.generic_visit(node)
        return self._tranform_node(
            self._tranform_node(node, self.variable_names, attr_name="id"),
            self.function_names,
            attr_name="id"
        )

    def visit_arg(self, node):
        # self._update_names_container(node, self.arg_names, names_label="arg", attr_name="arg")
        self.generic_visit(node)
        return self._tranform_node(node, self.arg_names, attr_name="arg")
    
    def visit_FunctionDef(self, node):
        self._erase_docstring(node)
        # self._update_names_container(node, self.function_names, names_label="func", attr_name="name")
        
        self.context.append(self.arg_names)
        self.generic_visit(node)
        self.context.pop()

        return self._tranform_node(node, self.function_names, attr_name="name")

    def visit_AsyncFunctionDef(self, node):
        self._erase_docstring(node)
        
        self.context.append(self.arg_names)
        self.generic_visit(node)
        self.context.pop()
        
        return self._tranform_node(node, self.function_names, attr_name="name")




if __name__ == "__main__":
    code = """
from typer import Typer

from etna.commands import backtest
from etna.commands import forecast

app =       Typer()
app.command()     (forecast)
app.command()(backtest)

a = b = c = 1

def bar():
    foo(1, 2)

@decorator
def foo(a, b):
    ''' Hello from docstring '''
    c = a + b

def other_func(arg1, arg2):
    pass

async def afunc():
    await other_func(1, 2)


if __name__ == "__main__":
    app()
    d = a + b * c
    """
    tree = ast.parse(code)
    open("hello.txt", 'w').write(ast.dump(tree, indent = 2) + "\n")
    names: NameCollectingVisitor = NameCollectingVisitor(tree)
    print(f"Variables: {names.variable_names}")
    print(f"Arguments: {names.arg_names}")
    print(f"Functions: {names.function_names}")
    new_code = ast.unparse(UnificationTranformer(names.variable_names, names.arg_names, names.function_names).visit(tree))
    print(new_code)


# from typer import Typer

# from etna.commands import backtest
# from etna.commands import forecast

# app =       Typer()
# app.command()     (forecast)
# app.command()(backtest)

# a = b = c = 1

# def foo(a, b):
#     pass

# def bar(a1, a2):
#     elem = a1 + a2 + "elem" + ["elem", "a1", "a2"]
#     return elem

# class Test:
#     def __init__(self):
#         self.hello = 'world'

#     def test(self, test1, test2, test3):
#         return run_tests(test1, test2, test3)

# if __name__ == "__main__":
#     app()
#     d = a + b * c

