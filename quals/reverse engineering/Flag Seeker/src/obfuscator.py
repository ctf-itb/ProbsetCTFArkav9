#!/bin/env python3

import argparse
import ast
import random
import string
import sys
from collections import defaultdict

builtins = set(dir(__builtins__)) | {"__builtins__"}


class Obfuscator(ast.NodeTransformer):
    def __init__(self, letters=string.ascii_letters):
        self.letters = letters
        self.seen = {}
        self.imported_items = defaultdict(dict)  # { module: { original_name: obfuscated_name } }
        self.name_replacements = {}
        self.module_ids = set()
        self.used_imports = {}

    @classmethod
    def obfuscate(cls, source_code: str) -> str:
        return cls()._obfuscate_code(source_code)

    def _obfuscate_code(self, source_code: str) -> str:
        tree = ast.parse(source_code)
        self.tree = tree

        obfuscated_tree = self.visit(tree)
        new_imports = self.generate_imports()
        obfuscated_tree.body = new_imports + obfuscated_tree.body

        return ast.unparse(obfuscated_tree)

    def visit_FunctionDef(self, node):
        if not node.name.startswith("_"):
            node.name = self.assign_name(node.name)
        for a in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
            a.arg = self.assign_name(a.arg)
        if a := node.args.vararg:
            a.arg = self.assign_name(a.arg)
        if a := node.args.kwarg:
            a.arg = self.assign_name(a.arg)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        node.name = self.assign_name(node.name)
        return self.generic_visit(node)

    def visit_Name(self, node):
        if node.id in self.name_replacements:
            return ast.Name(id=self.name_replacements[node.id], ctx=node.ctx)
        if node.id not in builtins and not node.id.startswith("_"):
            node.id = self.assign_name(node.id)
        return self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            module_name = alias.name
            self.collect_module_attributes(module_name)

        return []

    def visit_ImportFrom(self, node):
        module_name = node.module

        for alias in node.names:
            attr_name = alias.name
            obf_name = self.assign_name(attr_name)
            self.imported_items[module_name][attr_name] = obf_name
            self.name_replacements[f"{module_name}.{attr_name}"] = obf_name

        return []

    def visit_Attribute(self, node):
        full_attr_path = self.get_full_attribute_path(node)

        if "." in full_attr_path:
            base_object, attr_name = full_attr_path.rsplit(".", 1)
            if base_object in self.imported_items:
                if self.used_imports.get(base_object, None):
                    self.used_imports[base_object].add(attr_name)
                else:
                    self.used_imports[base_object] = {attr_name}

        if full_attr_path in self.name_replacements:
            return ast.Name(id=self.name_replacements[full_attr_path], ctx=node.ctx)

        return self.generic_visit(node)

    def visit_Global(self, node):
        for i, name in enumerate(node.names):
            node.names[i] = self.assign_name(name)
        return self.generic_visit(node)

    def assign_name(self, old_name):
        if old_name in self.seen:
            return self.seen[old_name]
        else:
            new_name = "".join(random.sample(self.letters, k=10))
            while new_name in self.seen.values():
                new_name = "".join(random.sample(self.letters, k=10))
            self.seen[old_name] = new_name
            return new_name

    def get_full_attribute_path(self, node):
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.append(node.id)
        return ".".join(reversed(parts))

    def collect_module_attributes(self, module_name, module=None):
        try:
            if module is None:
                module = __import__(module_name)
            if type(module).__name__ != "module":
                return
            self.module_ids.add(id(module))

            for attr in dir(module):
                obf_name = self.assign_name(attr)
                self.imported_items[module_name][attr] = obf_name
                self.name_replacements[f"{module_name}.{attr}"] = obf_name
                mod = getattr(module, attr)
                if id(mod) not in self.module_ids:
                    self.collect_module_attributes(
                        f"{module_name}.{attr}", module=getattr(module, attr)
                    )

        except (ImportError, ModuleNotFoundError, AttributeError):
            pass

    def generate_imports(self):
        imports = []
        for base_object, items in self.used_imports.items():
            names = []
            names = [
                ast.alias(name=orig, asname=obf)
                for orig, obf in self.imported_items[base_object].items()
                if orig in items
            ]
            if names:
                imports.append(ast.ImportFrom(module=base_object, names=names, level=0))
        return imports


def main():
    parser = argparse.ArgumentParser(description="Python Code Obfuscator")
    parser.add_argument("input_file", help="Path to the input Python file")
    parser.add_argument("output_file", help="Path to the output obfuscated Python file")
    parser.add_argument("--seed", help="Seed for randomization (default: None)", default=None)

    args = parser.parse_args()

    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    if args.seed:
        random.seed(args.seed.encode())

    obfuscated_code = Obfuscator.obfuscate(source_code)

    with open(args.output_file, "w", encoding="utf-8") as f:
        f.write(obfuscated_code)


if __name__ == "__main__":
    main()
