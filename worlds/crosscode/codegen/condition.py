import typing
import ast

COND_ELEMENT = 1
COND_ITEM = 2


class ConditionParser:
    item_data: typing.List[typing.Dict[str, typing.Any]]

    def __init__(self, item_data):
        self.item_data = item_data

    def parse_condition(self, cond: str) -> ast.Tuple:
        if cond in {"heat", "cold", "shock", "wave"}:
            return ast.Tuple([ast.Constant(f"{cond.title()}"), ast.Constant(1)])

        # This is the part of the code where I write a poor man's parser.
        # Because this data could be inputted by a user, I made it *EXTREMELY* fault-tolerant
        try:
            lhs, rhs = cond.split(">=")
        except ValueError:
            raise RuntimeError(f"Unrecognized condition format: `{cond}`")

        try:
            amount = int(rhs.strip())
        except ValueError:
            raise RuntimeError(f"Invalid count: `{rhs.strip()}`")

        try:
            word_item, number, word_amount = lhs.strip().split(".")
            if word_item != "item" and word_amount != "amount":
                raise RuntimeError(f"Need `item.{number}.amount`, not `{lhs}`")
        except ValueError:
            raise RuntimeError(
                f"Need three words separated by dots, not `{lhs}`")

        try:
            number = int(number)
        except ValueError:
            raise RuntimeError(f"Not an item ID: `{number}`")

        try:
            item_name = self.item_data[number]["name"]["en_US"]
        except IndexError:
            raise RuntimeError(f"Item ID doesn't fit: `{number}`")

        return ast.Tuple([ast.Constant(item_name), ast.Constant(amount)])

    def parse_condition_list(self, conditions: typing.List[str], includes_region=True) -> tuple[ast.List, str | None]:
        conds = ast.List([])

        start_index = 1 if includes_region else 0

        for cond in [x for x in conditions[start_index:] if x != ""]:
            tree = self.parse_condition(cond)
            ast.fix_missing_locations(tree)
            conds.elts.append(tree)

        return conds, conditions[0] if includes_region else None
