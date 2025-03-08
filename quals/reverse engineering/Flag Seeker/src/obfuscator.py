#!/bin/env python3

import ast
import random
import string
import sys

builtins = [name for name, function in sorted(vars(__builtins__).items())] + ["__builtins__"]


class Obfuscator(ast.NodeTransformer):
    def __init__(self, letters=string.ascii_letters):
        self.letters = letters
        self.seen = {}
        self.constants = []
        self.imports = []

    def visit_FunctionDef(self, node):
        if not node.name.startswith("_"):
            node.name = self.assign_name(node.name)
        for a in node.args.args:
            a.arg = self.assign_name(a.arg)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        node.name = self.assign_name(node.name)
        return self.generic_visit(node)

    def visit_Name(self, node):
        if node.id not in builtins and node.id not in self.imports:
            node.id = self.assign_name(node.id)
        return self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        return self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            alias.asname = self.assign_name(alias.name)
        return self.generic_visit(node)

    def visit_Global(self, node):
        for i, name in enumerate(node.names):
            node.names[i] = self.assign_name(name)
        return self.generic_visit(node)

    # def get_variable_name(self, i):
    #     letter = self.letters[i % len(self.letters)]
    #     if i >= len(self.letters):
    #         return letter + self.get_variable_name(i // len(self.letters))
    #     else:
    #         return letter

    def assign_name(self, oldName):
        if oldName in self.seen:
            return self.seen[oldName]
        else:
            newName = "".join(random.sample(self.letters, k=10))
            while newName in self.seen.values():
                newName = "".join(random.sample(self.letters, k=10))
            self.seen[oldName] = newName
            return newName


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        tree = ast.parse(f.read())

    obfuscator = Obfuscator()
    obfuscator.visit(tree)

    random.seed("arkavidia9")
    shuffled = list(range(len(obfuscator.constants)))
    random.shuffle(shuffled)

    shuffled_constants = [
        obfuscator.constants[shuffled.index(i)] for i in range(len(obfuscator.constants))
    ]

    out = ast.unparse(tree)

    with open(sys.argv[2], "w") as f:
        f.write(out)
