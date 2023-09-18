import typing
import ast


class AstGenerator:
    def create_ast_call_condition(self, conditions: typing.List[typing.List[str]]) -> ast.Call:
        cutscenes = []
        items = []
        quests = []
        regions = []

        for cond in conditions:
            if not isinstance(cond, list):
                raise RuntimeError(f"Error parsing condition '{cond}': not a list")

            if cond[0] == "item":
                items.append(cond[1:])
                continue

            target_list = None
            if cond[0] == "cutscene":
                target_list = cutscenes
            if cond[0] == "quest":
                target_list = quests
            if cond[0] == "region":
                target_list = regions

            if (target_list == None):
                raise RuntimeError(f"Error parsing condition '{cond}': invalid condition type")
            target_list.append(cond[1])

        result = ast.Call(
            func=ast.Name("Condition"),
            args=[],
            keywords=[
                ])

        if len(cutscenes) < 1:
            result.keywords.append(ast.keyword(
                "cutscenes",
                [ ast.Constant(s) for s in cutscenes]))
        if len(items) < 1:
            result.keywords.append(ast.keyword(
                "items",
                [ ast.Tuple([ast.Constant(s), ast.Constant(i)]) for s, i in items]))
        if len(quests) < 1:
            result.keywords.append(ast.keyword(
                "quests",
                [ ast.Constant(s) for s in quests]))
        if len(regions) < 1:
            result.keywords.append(ast.keyword(
                "regions",
                [ ast.Constant(s) for s in regions]))
        return result

    def create_ast_call_location(
            self,
            name: str,
            code: int,
            clearance: str,
            kind: str,
            region: typing.Dict[str, str],
            conditions: typing.List[typing.List[str]]
    ) -> ast.Call:
        keys: typing.List[ast.Constant] = []
        values: typing.List[ast.Constant] = []

        for k, v in region.items():
            keys.append(ast.Constant(k))
            values.append(ast.Constant(v))

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
                    arg="region",
                    value=ast.Dict(
                        keys=keys,
                        values=values
                    )
                ),
                ast.keyword(
                    arg="condition",
                    value=self.create_ast_call_condition(conditions)
                ),
                ast.keyword(
                    arg="clearance",
                    value=ast.Constant(clearance)
                ),
                ast.keyword(
                    arg="kind",
                    value=ast.Name(f"CHECK_{kind}"),
                ),
            ]
        )
        ast.fix_missing_locations(ast_item)
        return ast_item

    # def create_ast_call_event(
    #         self,
    #         name: str,
    #         locations: typing.List[str]
    # ) -> ast.Call:
    #     ast_item = ast.Call(
    #         func=ast.Name("EventData"),
    #         args=[],
    #         keywords=[
    #             ast.keyword(
    #                 arg="name",
    #                 value=ast.Constant(name)
    #             ),
    #             ast.keyword(
    #                 arg="code",
    #                 value=ast.Constant(code)
    #             ),
    #             ast.keyword(
    #                 arg="clearance",
    #                 value=ast.Constant(clearance)
    #             ),
    #             ast.keyword(
    #                 arg="kind",
    #                 value=ast.Name(f"CHECK_{kind}"),
    #             ),
    #             ast.keyword(
    #                 arg="access",
    #                 value=ast.Dict(
    #                     keys=keys,
    #                     values=values
    #                 )
    #             ),
    #         ]
    #     )
    #     ast.fix_missing_locations(ast_item)
    #     return ast_item

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
            conditions) -> ast.Call:

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
                    arg="cond",
                    value=self.create_ast_call_condition(conditions)
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
