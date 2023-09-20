import typing
import ast

from .ast import AstGenerator
from .context import Context
from .util import *

class RegionMap:
    ctx: Context

    regions_seen: typing.Set[str]
    connections: typing.List[ast.Call]
    mode: str

    def __init__(self, mode, ctx: Context):
        self.ctx = ctx
        self.mode = mode
        self.regions_seen = set()
        self.connections = []

    def add_region_connection(self, conn: typing.Dict[str, typing.Any]):
        self.regions_seen.add(conn["from"])
        self.regions_seen.add(conn["to"])

        self.connections.append(self.ctx.ast_generator.create_ast_call_region_connection(
            conn["from"],
            conn["to"],
            conn["condition"] if "condition" in conn else []))


class GameState:
    ctx: Context
    current_code: int = BASE_ID

    # stores a list of AST objects representing chests
    # no, I didn't make it store the list as an AST object
    # that just renders it as one long line, which is bad for debugging
    # so I do some steps manually
    ast_location_list: typing.List[ast.Call]

    # same thing as ast_location_list except it's just for events
    # events are automatically created for quests with multiple rewards
    # this is so that they can have an easily-named location to call
    ast_event_list: typing.List[ast.Call]

    # similar but for items
    # also, IDs are not contiguous so we store these as a dict
    found_items: typing.Dict[int, ast.Call]

    # contains information all about a specific logic pack's regions
    region_maps: typing.Dict[str, RegionMap]

    # The number of items needed
    # Incremented when there's a location with no reward
    needed_items: typing.Dict[str, int] = {}

    def __init__(self, ctx: Context):
        # duplicating some attributes
        self.ctx = ctx

        self.ast_location_list = []
        self.ast_event_list = []
        self.found_items = {}
        self.region_maps = {}

    def get_item_classification(self, item: dict) -> str:
        """Deduce the classification of an item based on its item-database entry"""
        if item["type"] == "CONS" or item["type"] == "TRADE":
            return "filler"
        elif item["type"] == "KEY":
            return "progression"
        elif item["type"] == "EQUIP":
            return "useful"
        elif item["type"] == "TOGGLE":
            if "Booster" in item["name"]["en_US"]:
                return "progression"
            else:
                return "filler"
        else:
            raise RuntimeError(
                f"I don't know how to classify this item: {item['name']}")

    def add_item(self, item_name: str, item_amount: int, mode: str):
        item_full_name = item_name if item_amount == 1 else f"{item_name} x{item_amount}"
        item_id = self.ctx.rando_data["items"][item_name]["id"]

        item_info = self.ctx.item_data[item_id]

        combo_id = BASE_ID + RESERVED_ITEM_IDS + \
            self.ctx.num_items * (item_amount - 1) + item_id

        if combo_id not in self.found_items:
            self.found_items[combo_id] = self.ctx.ast_generator.create_ast_call_item(
                item_full_name,
                item_id,
                item_amount,
                combo_id,
                self.get_item_classification(item_info))

        self.ctx.ast_generator.add_quantity(self.found_items[combo_id], mode)

    def add_element_item(self, el: str, mode: str):
        try:
            idx = ["Heat", "Cold", "Shock", "Wave"].index(el)
        except:
            raise RuntimeError("Error adding element: {el} not an element")

        item = self.ctx.ast_generator.create_ast_call_item(
            el, 0, 1, BASE_ID + idx, "progression")
        for mode in self.ctx.rando_data["modes"]:
            quantity = item.keywords[-1].value
            assert (isinstance(quantity, ast.Dict))
            quantity.keys.append(ast.Constant(mode))
            quantity.values.append(ast.Constant(1))

        self.found_items[BASE_ID + idx] = item

    def add_reward(self, ary: typing.List, mode: str):
        kind, *info = ary

        if kind == "item":
            if len(info) == 1:
                self.add_item(info[0], 1, mode)
            elif len(info) == 2:
                self.add_item(info[0], info[1], mode)
            else:
                raise RuntimeError(f"Error parsing reward {ary}: expected one or two elements")
        elif kind == "element":
            if len(info) == 1:
                self.add_element_item(info[0], mode)
            else:
                raise RuntimeError(f"Error parsing reward {ary}: expected one element")
        else:
            raise RuntimeError(f"Error parsing reward {ary}: unrecognized type")

    def add_location(self, name: str, clearance: str, check: typing.Dict[str, typing.Any]):
        check["mwid"] = []

        num_rewards = 1
        if "reward" in check:
            if len(check["reward"]) == 0:
                raise RuntimeError(f"Error while location {name}: need one or more rewards (get rid of the entry if there are no rewards)")
            num_rewards = max(num_rewards, len(check["reward"]))

        location_names = []

        for idx in range(num_rewards):
            full_name = name
            if num_rewards > 1:
                full_name += f" - Reward {idx + 1}"

            self.ast_location_list.append(self.ctx.ast_generator.create_ast_call_location(
                full_name,
                self.current_code,
                clearance,
                check["region"],
                check["condition"] if "condition" in check else []))

            check["mwid"].append(self.current_code)

            self.current_code += 1
            location_names.append(full_name)

        if num_rewards > 1:
            self.ast_event_list.append(self.ctx.ast_generator.create_ast_call_location(
                name,
                None,
                "Default",
                check["region"],
                [["quest", name] for name in location_names]
            ))

        if "reward" not in check:
            for mode in check["region"]:
                if check["region"][mode] in self.ctx.rando_data["excludedRegions"][mode]:
                    print(f"skipping reward for {name}")
                    continue
                if mode not in self.needed_items:
                    self.needed_items[mode] = 1
                else:
                    self.needed_items[mode] += 1
            return

        if not isinstance(check["reward"], list):
            raise RuntimeError(f"Error adding rewards for location {name}: reward is not a list")

        for mode in check["region"]:
            if check["region"][mode] in self.ctx.rando_data["excludedRegions"][mode]:
                continue
            for reward in check["reward"]:
                self.add_reward(reward, mode)

    def add_chest(self, name: str, chest: typing.Dict[str, typing.Any]):
        clearance = chest["clearance"]

        self.add_location(
            name,
            clearance,
            chest)

    def add_cutscene(self, name: str, cutscene: typing.Dict[str, typing.Any]):
        self.add_location(
            name,
            "Default",
            cutscene)

    def add_element_location(self, name: str, element: typing.Dict[str, typing.Any]):
        self.add_location(
            name,
            "Default",
            element)

    def add_quest(self, name: str, quest: typing.Dict[str, typing.Any]):
        self.add_location(
            name,
            "Default",
            quest)

    def calculate_game_state(self):
        constants: typing.Dict[str, typing.Any] = {
            "BASE_ID": BASE_ID,
            "BASE_NORMAL_LOCATION_ID": BASE_ID + RESERVED_ITEM_IDS
        }

        self.ctx.rando_data["mwconstants"] = constants

        for name, chest in self.ctx.rando_data["chests"].items():
            self.add_chest(name, chest)

        for name, cutscene in self.ctx.rando_data["cutscenes"].items():
            self.add_cutscene(name, cutscene)

        for name, element in self.ctx.rando_data["elements"].items():
            self.add_element_location(name, element)

        for dev_name, quest in dict.items(self.ctx.rando_data["quests"]):
            self.add_quest(dev_name, quest)

        for mode, regions in self.ctx.rando_data["regions"].items():
            region_map = RegionMap(mode, self.ctx)
            for connection in regions:
                region_map.add_region_connection(connection)

            self.region_maps[mode] = region_map
