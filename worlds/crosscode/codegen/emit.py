import ast
import typing

from ..types.World import WorldData

def emit_list(lst: list[ast.AST], indent: str = "    ") -> str:
    after = ",\n"

    return "[\n" + "".join([indent + ast.unparse(item) + after for item in lst]) + "]"
