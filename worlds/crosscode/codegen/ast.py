import typing
import ast

from .condition import ConditionParser

class AstGenerator:
    condition_parser: ConditionParser
    def __init__(self, condition_parser: ConditionParser):
        self.condition_parser = condition_parser

    def create_ast_call_location(
            self,
            name: str, 
            code: int,
            clearance: str,
            kind: str,
            condition_lists: typing.Dict[str, typing.List[str]]
    ) -> ast.Call:
        keys: typing.List[ast.Constant] = []
        values: typing.List[ast.Call] = []

        for key, conditions in condition_lists.items():
            cond_elements, cond_items, region = self.condition_parser.parse_condition_list(conditions)
            
            # working inside out here, we have to start with region.
            # then we add cond_elements and cond_items only if they are relevant
            access_info_keywords = [
                ast.keyword(
                    arg="region",
                    value=ast.Constant(region)
                ),
            ]

            if cond_elements.elts != []:
                access_info_keywords.append(
                    ast.keyword(
                        arg="cond_elements",
                        value=cond_elements
                    )
                )

            if cond_items.elts != []:
                access_info_keywords.append(
                    ast.keyword(
                        arg="cond_items",
                        value=cond_items
                    )
                )

            access_info = ast.Call(
                func=ast.Name("AccessInformation"),
                args=[],
                keywords=access_info_keywords,
            )

            keys.append(ast.Constant(key))
            values.append(access_info)

        ast_item = ast.Call(
            func=ast.Name("LocationData"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="name",
                    value=ast.Constant(name)
                ),
                ast.keyword(
                    arg="code",
                    value=ast.Constant(code)
                ),
                ast.keyword(
                    arg="clearance",
                    value=ast.Constant(clearance)
                ),
                ast.keyword(
                    arg="kind",
                    value=ast.Name(f"CHECK_{kind}"),
                ),
                ast.keyword(
                    arg="access",
                    value=ast.Dict(
                        keys=keys,
                        values=values
                    )
                ),
            ]
        )
        ast.fix_missing_locations(ast_item)
        return ast_item

    def create_ast_call_item(
            self,
            name: str,
            item_id: int,
            amount: int,
            combo_id: int,
            classification: str) -> ast.Call:
        ast_item = ast.Call(
            func=ast.Name("ItemData"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="name",
                    value=ast.Constant(name)
                ),
                ast.keyword(
                    arg="item_id",
                    value=ast.Constant(item_id)
                ),
                ast.keyword(
                    arg="amount",
                    value=ast.Constant(amount)
                ),
                ast.keyword(
                    arg="combo_id",
                    value=ast.Constant(combo_id)
                ),
                ast.keyword(
                    arg="classification",
                    value=ast.Attribute(
                        value=ast.Name("ItemClassification"),
                        attr=classification,
                    )
                ),
                ast.keyword(
                    arg="quantity",
                    value=ast.Dict(keys=[], values=[])
                ),
            ]
        )
        ast.fix_missing_locations(ast_item)
        return ast_item

    def create_ast_call_region_connection(
            self,
            region_from: str,
            region_to: str,
            cond_elements,
            cond_items) -> ast.Call:
        ast_item = ast.Call(
            func=ast.Name("RegionConnection"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="region_from",
                    value=ast.Constant(region_from)
                ),
                ast.keyword(
                    arg="region_to",
                    value=ast.Constant(region_to)
                ),
                ast.keyword(
                    arg="cond_elements",
                    value=cond_elements
                ),
                ast.keyword(
                    arg="cond_items",
                    value=cond_items
                ),
            ]
        )

        ast.fix_missing_locations(ast_item)

        return ast_item

    def add_quantity(
            self,
            item: ast.Call,
            mode: str):
        quantity_keyword = item.keywords[-1]
        quantity = quantity_keyword.value

        assert(isinstance(quantity, ast.Dict))
        try:
            idx = list(map(lambda x: x.value, quantity.keys)).index(mode)
        except ValueError:
            quantity.keys.append(ast.Constant(mode))
            quantity.values.append(ast.Constant(1))
        else:
            number = quantity.values[idx]
            assert(isinstance(number, ast.Constant))
            number.value += 1

        ast.fix_missing_locations(quantity)
