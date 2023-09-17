import typing
from .ast import AstGenerator
from .condition import ConditionParser

from .util import get_json_object, load_json_with_includes


class Context:
    rando_data: typing.Dict[str, typing.Any]
    item_data: typing.List[typing.Dict[str, typing.Any]]
    database: typing.Dict[str, typing.Any]
    num_items: int

    condition_parser: ConditionParser
    ast_generator: AstGenerator

    def __init__(self, rando_data, item_data, database):
        self.rando_data = rando_data
        self.item_data = item_data
        self.database = database
        self.num_items = len(self.item_data)

        self.condition_parser = ConditionParser(self.item_data)
        self.ast_generator = AstGenerator(self.condition_parser)


def make_context_from_directory(data_dir) -> Context:
    return Context(
        load_json_with_includes(f"{data_dir}/in/master.json"),
        get_json_object(f"{data_dir}/assets/data/item-database.json")["items"],
        get_json_object(f"{data_dir}/assets/data/database.json"))
