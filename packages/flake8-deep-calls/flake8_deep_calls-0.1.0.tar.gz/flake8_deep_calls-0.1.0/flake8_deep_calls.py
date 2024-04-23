from ast import AST, NodeVisitor, Call, FunctionDef, Name
from typing import Generator, Any, Tuple, Type

import importlib.metadata as importlib_metadata


class FunctionDefCollector(NodeVisitor):
    def __init__(self):
        self.functions = {}

    def visit_FunctionDef(self, node: FunctionDef):
        self.functions[node.name] = {
            'line': node.lineno,
            'col': node.col_offset,
            'calls': []}


class Visitor(NodeVisitor):
    def __init__(self, functions: dict):
        self.functions: dict = functions
        self.current_function: str = ''
        self.errors = {}

    def visit_FunctionDef(self, node: FunctionDef):
        self.current_function = node.name
        self.generic_visit(node)

    def visit_Call(self, node: Call):
        if isinstance(node.func, Name) and node.func.id in self.functions:
            self.functions[self.current_function]['calls'].append(node.func.id)


class Plugin:
    name = 'deep_call_checker'
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: AST) -> None:
        self.tree = tree

    def get_max_depth(self, function, func_calls, visited):
        if function in visited:  # Avoid infinite recursion due to cycles
            return 0
        visited.add(function)

        max_depth = 0
        for called_func in func_calls.get(function, {}).get('calls', []):
            current_depth = 1 + self.get_max_depth(called_func, func_calls, visited.copy())
            max_depth = max(max_depth, current_depth)
        return max_depth

    def calculate_nesting_depths(self, func_calls):
        nesting_depths = {}
        for function, details in func_calls.items():
            depth = self.get_max_depth(function, func_calls, set())
            nesting_depths[function] = {
                'line': details['line'],
                'col': details['col'],
                'nesting_depth': depth
            }
        return nesting_depths

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        collector = FunctionDefCollector()
        collector.visit(self.tree)

        visitor = Visitor(functions=collector.functions)
        visitor.visit(self.tree)

        results = self.calculate_nesting_depths(visitor.functions)
        filtered_results = [
            (
                results[x].get('line'),
                results[x].get('col'),
                f'FDC100 function {x} calls local functions {results[x].get("nesting_depth")} levels deep')
            for x in results if results[x].get('nesting_depth') > 1]
        for error in filtered_results:
            yield error + (type(self),)
