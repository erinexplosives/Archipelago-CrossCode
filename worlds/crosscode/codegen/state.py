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

    def add_region_connection(self, ary):
        region_from, arrow, region_to, *conditions = ary

        self.regions_seen.add(region_from)
        self.regions_seen.add(region_to)

        if arrow != "<->":
            raise RuntimeError(f"Area connection malformed: {ary}")

        self.connections.append(self.ctx.ast_generator.create_ast_call_region_connection(
            region_from,
            region_to,
            conditions))


class GameState:
    ctx: Context
    current_code: int = BASE_ID

    # stores a list of AST objects representing chests
    # no, I didn't make it store the list as an AST object
    # that just renders it as one long line, which is bad for debugging
    # so I do some steps manually
    ast_location_list: typing.List[ast.Call]

    # similar but for items
    # also, IDs are not contiguous so we store these as a dict
    found_items: typing.Dict[int, ast.Call]

    # contains information all about a specific logic pack's regions
    region_maps: typing.Dict[str, RegionMap]

    # a list of *Archipelago* events (i.e. status markers)
    ast_reward_event_list: typing.List[ast.Call]

    def __init__(self, ctx: Context):
        # duplicating some attributes
        self.ctx = ctx

        self.ast_location_list = []
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

    def add_item(self, item_id: int, item_amount: int, mode: str):
        item_info = self.ctx.item_data[item_id]
        item_name = item_info["name"]["en_US"]

        item_full_name = item_name if item_amount == 1 else f"{item_name} x{item_amount}"

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

    def add_location(self, name: str, clearance: str, kind: str, check: typing.Dict[str, typing.Any]):
        if "reward" not in check:
            raise RuntimeError(f"Error adding location {name}: no rewards for location")
        if not isinstance(check["reward"], list):
            raise RuntimeError(f"Error adding location {name}: reward is not a list")

        check["mwid"] = []

        for idx, reward in enumerate(check["reward"]):
            full_name = name
            if kind == "QUEST":
                full_name += " - Reward"
            if len(check["reward"]) > 0:
                full_name += f" {idx + 1}"

            self.ast_location_list.append(self.ctx.ast_generator.create_ast_call_location(
                full_name,
                self.current_code,
                clearance,
                kind,
                check["region"],
                check["condition"]))

            check["mwid"].append(self.current_code)

            self.current_code += 1

    def add_chest(self, name: str, chest: typing.Dict[str, typing.Any]):
        clearance = chest["type"]

        self.add_location(
            name,
            clearance,
            "CHEST",
            chest)

        for mode, conditions in chest["condition"].items():
            if conditions[0] not in self.ctx.rando_data["softLockAreas"][mode]:
                self.add_item(chest["item"], chest["amount"], mode)

    def add_cutscene(self, name: str, cutscene: typing.Dict[str, typing.Any]):
        self.add_location(
            name,
            "Default",
            "EVENT",
            cutscene)

        for mode, conditions in cutscene["condition"].items():
            if conditions[0] not in self.ctx.rando_data["softLockAreas"][mode]:
                self.add_item(cutscene["item"], cutscene["amount"], mode)

    def add_element(self, name: str, element: typing.Dict[str, typing.Any]):
        self.add_location(
            name,
            "Default",
            "ELEMENT",
            element)

    def add_quest(self, dev_name: str, quest: typing.Dict[str, typing.Any]):
        data = self.ctx.database["quests"][dev_name]
        location_name = data["name"]["en_US"]

        self.add_location(
            location_name,
            "Default",
            "QUEST",
            quest)

        for mode, conditions in quest["condition"].items():
            if conditions[0] not in self.ctx.rando_data["softLockAreas"][mode]:
                self.add_item(quest["item"], quest["amount"], mode)

    def calculate_game_state(self):
        constants: typing.Dict[str, typing.Any] = {
            "BASE_ID": BASE_ID,
            "BASE_NORMAL_LOCATION_ID": BASE_ID + RESERVED_ITEM_IDS
        }

        self.ctx.rando_data["mwconstants"] = constants

        for idx, el in enumerate(["Heat", "Cold", "Shock", "Wave"]):
            item = self.ctx.ast_generator.create_ast_call_item(
                el, 0, 1, BASE_ID + idx, "progression")
            for mode in self.ctx.rando_data["modes"]:
                quantity = item.keywords[-1].value
                assert (isinstance(quantity, ast.Dict))
                quantity.keys.append(ast.Constant(mode))
                quantity.values.append(ast.Constant(1))

            self.found_items[BASE_ID + idx] = item

        for name, chest in self.ctx.rando_data["chests"].items():
            self.add_chest(name, chest)

        for name, cutscene in self.ctx.rando_data["cutscenes"].items():
            self.add_cutscene(name, cutscene)

        for name, element in self.ctx.rando_data["elements"].items():
            self.add_element(name, element)

        for dev_name, quest in dict.items(self.ctx.rando_data["quests"]):
            self.add_quest(dev_name, quest)

        for mode, regions in self.ctx.rando_data["areas"].items():
            region_map = RegionMap(mode, self.ctx)
            for connection in regions:
                region_map.add_region_connection(connection)

            self.region_maps[mode] = region_map
