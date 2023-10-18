import typing

from .util import get_json_object, load_json_with_includes, load_world_json


class Context:
    rando_data: dict[str, typing.Any]
    addons: dict[str, dict[str, typing.Any]]
    item_data: list[typing.Dict[str, typing.Any]]
    database: dict[str, typing.Any]
    num_items: int

    def __init__(self, rando_data, addons, item_data, database):
        self.rando_data = rando_data
        self.addons = addons
        self.item_data = item_data
        self.database = database
        self.num_items = len(self.item_data)


def make_context_from_directory(data_dir, with_assets=True) -> Context:
    master, addons = load_world_json(f"{data_dir}/in/master.json")
    if with_assets:
        return Context(
            master,
            addons,
            get_json_object(f"{data_dir}/assets/data/item-database.json")["items"],
            get_json_object(f"{data_dir}/assets/data/database.json")
        )
    else:
        return Context(
            master,
            addons,
            [],
            {}
        )
