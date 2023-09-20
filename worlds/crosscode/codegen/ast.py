import typing
import ast

from BaseClasses import ItemClassification

from ..types.Locations import Condition, LocationData
from ..types.Regions import RegionConnection
from ..types.Items import ItemData


class AstGenerator:
    def create_ast_call_condition(self, cond: Condition) -> ast.Call:
        result = ast.Call(
            func=ast.Name("Condition"),
            args=[],
            keywords=[])

        if len(cond.items) >= 1:
            result.keywords.append(ast.keyword(
                "items",
                ast.List([ ast.Tuple([ast.Constant(s), ast.Constant(i)]) for s, i in cond.items])))
        if len(cond.quests) >= 1:
            result.keywords.append(ast.keyword(
                "quests",
                ast.List([ast.Constant(s) for s in cond.quests])))
        if len(cond.locations) >= 1:
            result.keywords.append(ast.keyword(
                "locations",
                ast.List([ast.Constant(s) for s in cond.locations])))
        if len(cond.regions) >= 1:
            result.keywords.append(ast.keyword(
                "regions",
                ast.Dict(
                    keys=[ast.Constant(s) for s in cond.regions.keys()],
                    values=[ast.Constant(s) for s in cond.regions.values()]
                )
            ))
        return result

    def create_ast_call_location(self, data: LocationData) -> ast.Call:
        keys: typing.List[ast.Constant] = []
        values: typing.List[ast.Constant] = []

        for k, v in data.region.items():
            keys.append(ast.Constant(k))
            values.append(ast.Constant(v))

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
                ast.keyword(
                    arg="region",
                    value=ast.Dict(
                        keys=keys,
                        values=values
                    )
                ),
            ]
        )

        if len(data.cond) > 0:
            ast_item.keywords.append(ast.keyword(
                arg="cond",
                value=self.create_ast_call_condition(data.cond)
            ))

        if data.clearance != "Default":
            ast_item.keywords.append(ast.keyword(
                arg="clearance",
                value=ast.Constant(data.clearance)
            ))

        ast.fix_missing_locations(ast_item)
        return ast_item

    def create_ast_call_item(self, data: ItemData):
        classification_as_str = ""
        if data.classification == 0b0000:
            classification_as_str = "filler"
        if data.classification == 0b0001:
            classification_as_str = "progression"
        if data.classification == 0b0010:
            classification_as_str = "useful"
        if data.classification == 0b0100:
            classification_as_str = "trap"
        if data.classification == 0b1000:
            classification_as_str = "skip_balancing"
        if data.classification == 0b1001:
            classification_as_str = "progression_skip_balancing"

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
                        attr=classification_as_str
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
                    value=self.create_ast_call_condition(conn.cond)
                ),
            ]
        )

        ast.fix_missing_locations(ast_region)

        return ast_region

    def add_quantity(
            self,
            item: ast.Call,
            mode: str):
        quantity_keyword = item.keywords[-1]
        quantity = quantity_keyword.value

        assert (isinstance(quantity, ast.Dict))
        try:
            idx = list(map(lambda x: x.value, quantity.keys)).index(mode)
        except ValueError:
            quantity.keys.append(ast.Constant(mode))
            quantity.values.append(ast.Constant(1))
        else:
            number = quantity.values[idx]
            assert (isinstance(number, ast.Constant))
            number.value += 1

        ast.fix_missing_locations(quantity)
