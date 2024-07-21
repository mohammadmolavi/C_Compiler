class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {
            "global": {
                "functions": {},
                "variables": {}
            },
            "functions": {}
        }

    def analyze(self):
        self.visit(self.ast)

    def visit(self, node):
        try:
            method_name = 'visit_' + node['type']
        except:
            method_name = 'visit_' + node[0]['type']
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for item in node:
                self.visit(item)
        elif isinstance(node, dict):
            for key, value in node.items():
                self.visit(value)

    def visit_START(self, node):
        for func in node['body']:
            self.visit(func)

    def visit_FUNC(self, node):
        func_name = node['name']
        func_info = {
            "return_type": node['return_type'],
            "params": []
        }
        for param in node['params']:
            func_info["params"].append({
                "name": param['name'],
                "type": param['param_type']
            })
        self.symbol_table["global"]["functions"][func_name] = func_info
        self.symbol_table["functions"][func_name] = {
            "scope": "function",
            "variables": {}
        }
        for param in node['params']:
            self.symbol_table["functions"][func_name]["variables"][param['name']] = param['param_type']
        self.visit(node['body'])

    def visit_PARAM(self, node):
        pass

    def visit_EXP(self, node):
        for exp in node:
            self.visit(exp)

    def visit_binary_expression(self, node):
        left_type = self.visit(node['left'])
        right_type = self.visit(node['right'])
        if left_type != right_type:
            raise TypeError(f"Type mismatch: {left_type} and {right_type} in binary expression")
        return left_type

    def visit_operand(self, node):
        value = node['value']
        if isinstance(value, int):
            return 'int'
        elif isinstance(value, str):
            if value in self.current_scope()["variables"]:
                return self.current_scope()["variables"][value]
            elif value in self.symbol_table["global"]["variables"]:
                return self.symbol_table["global"]["variables"][value]
            else:
                raise NameError(f"Variable '{value}' is not defined")
        elif value in ['true', 'false']:
            return 'bool'

    def visit_call_func(self, node):
        func_name = node['name']
        if func_name not in self.symbol_table["global"]["functions"]:
            raise NameError(f"Function '{func_name}' is not defined")
        for param in node['parameters']:
            self.visit(param['expression'])
        return self.symbol_table["global"]["functions"][func_name]["return_type"]

    def visit_FOR(self, node):
        self.visit(node['def_for'])
        self.visit(node['body'])

    def visit_DEF_FOR(self, node):
        self.current_scope()["variables"][node['var']] = node['var_type']
        self.visit(node['var_value'])
        self.visit(node['relexp'])
        self.visit(node['exp1'])

    def visit_IF(self, node):
        self.visit(node['relexp'])
        self.visit(node['body'])
        if node['else']:
            self.visit(node['else']['body'])

    def visit_PRINT(self, node):
        self.visit(node['params'])

    def visit_RETURN(self, node):
        try:
            self.visit(node['operand'])
        except:
            self.visit(node[0]['operand'])

    def visit_COMMENT(self, node):
        pass

    def current_scope(self):
        return self.symbol_table["functions"].get(self.current_function, self.symbol_table["global"])

# Example usage
import json

with open("../parsing_tree.json") as tree_file:
    ast = json.load(tree_file)


semantic_analyzer = SemanticAnalyzer(ast)
# try:
semantic_analyzer.analyze()
print("Semantic analysis completed successfully.")
print(json.dumps(semantic_analyzer.symbol_table, indent=4))
# except (TypeError, NameError) as e:
#     print(f"Semantic error: {e}")
