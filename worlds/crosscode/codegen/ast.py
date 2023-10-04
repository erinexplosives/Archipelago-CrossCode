import typing
import ast

from ..types.Condition import Condition
from ..types.Locations import LocationData
from ..types.Regions import RegionConnection
from ..types.Items import ItemData


class AstGenerator:
    def create_ast_call_condition(self, condition: Condition) -> ast.Call:
        result = ast.Call(
            func=ast.Name(condition.__class__.__name__),
            args=[],
            keywords=[ast.keyword(arg=key, value=ast.Constant(value)) for key, value in condition.__dict__.items()],
        )
        ast.fix_missing_locations(result)

        return result

    def create_ast_call_condition_list(self, conditions: typing.Optional[list[Condition]]) -> ast.expr:
        if conditions is None:
            return ast.Constant(None)
        result = ast.List(elts=[])

        for condition in conditions:
            result.elts.append(self.create_ast_call_condition(condition))

        ast.fix_missing_locations(result)
        return result

    def create_ast_call_location(self, data: LocationData) -> ast.Call:
        ast_item = ast.Call(
            func=ast.Name("LocationData"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="name",
                    value=ast.Constant(data.name)
                ),
                ast.keyword(
                    arg="code",
                    value=ast.Constant(data.code)
                ),
            ]
        )

        ast.fix_missing_locations(ast_item)
        return ast_item

    def create_ast_call_item(self, data: ItemData):
        ast_item = ast.Call(
            func=ast.Name("ItemData"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="name",
                    value=ast.Constant(data.name)
                ),
                ast.keyword(
                    arg="item_id",
                    value=ast.Constant(data.item_id)
                ),
                ast.keyword(
                    arg="amount",
                    value=ast.Constant(data.amount)
                ),
                ast.keyword(
                    arg="combo_id",
                    value=ast.Constant(data.combo_id)
                ),
                ast.keyword(
                    arg="classification",
                    value=ast.Attribute(
                        value=ast.Name("ItemClassification"),
                        attr=data.classification.name
                    )
                ),
            ]
        )
        ast.fix_missing_locations(ast_item)
        return ast_item

    def create_ast_call_region_connection(self, conn: RegionConnection):
        ast_region = ast.Call(
            func=ast.Name("RegionConnection"),
            args=[],
            keywords=[
                ast.keyword(
                    arg="region_from",
                    value=ast.Constant(conn.region_from)
                ),
                ast.keyword(
                    arg="region_to",
                    value=ast.Constant(conn.region_to)
                ),
                ast.keyword(
                    arg="cond",
                    value=self.create_ast_call_condition_list(conn.cond)
                ),
            ]
        )

        ast.fix_missing_locations(ast_region)

        return ast_region
