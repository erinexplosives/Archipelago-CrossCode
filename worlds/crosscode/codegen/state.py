import typing
import ast

from .ast import AstGenerator
from .condition import ConditionParser
from .context import Context
from .util import *


class RoomInfo:
    has_fancy_name: bool
    room_name: str
    chests: typing.List
    circuit_override_number: int

    # stores a mapping of clearance values to [index of current chest of that clearance value, total chests of that clearance value]
    # helps generate semantic names for chests of same clearance value in the same room
    # so like "Bronze Chest 1" "Bronze Chest 2" etc
    chest_amounts: typing.Dict[str, typing.List[int]]

    def __init__(self, dev_name: str, room: typing.Dict[str, typing.Any]):
        self.has_fancy_name = "name" in room
        self.room_name: str = room["name"] if self.has_fancy_name else dev_name
        self.chests = room["chests"]
        self.chest_amounts = {}
        self.circuit_override_number = 1

        if len(self.chests) > 1:
            for level in ["Default", "Bronze", "Silver", "Gold"]:
                self.chest_amounts[level] = [
                    0,
                    len(list(
                        filter(lambda c: c["type"] == level, dict.values(self.chests))))
                ]


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

    region_maps: typing.Dict[str, RegionMap]

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
        self.ast_location_list.append(self.ctx.ast_generator.create_ast_call_location(
            name,
            self.current_code,
            clearance,
            kind,
            check["condition"]))

        check["mwid"] = self.current_code

        self.current_code += 1

    def add_chest(self, chest: typing.Dict[str, typing.Any], room_info: RoomInfo):
        clearance = chest["type"]

        # this occasionally shows up.
        # it does represent a different type of chest but you don't need anything to open it
        if clearance == "MasterKey":
            clearance = "Default"
        chest_name = "Chest" if clearance == "Default" else f"{clearance} Chest"

        if clearance in room_info.chest_amounts and room_info.chest_amounts[clearance][1] > 1:
            room_info.chest_amounts[clearance][0] += 1
            chest_name += f" {room_info.chest_amounts[clearance][0]}"

        location_full_name = f"{room_info.room_name} - {chest_name}"

        self.add_location(
            location_full_name,
            clearance,
            "CHEST",
            chest)

        for mode, conditions in chest["condition"].items():
            if conditions[0] not in self.ctx.rando_data["softLockAreas"][mode]:
                self.add_item(chest["item"], chest["amount"], mode)

    def add_event(self, event: typing.Dict[str, typing.Any], room_info: RoomInfo):
        event_name = self.ctx.item_data[event["item"]]["name"]["en_US"]

        location_full_name = f"{room_info.room_name} - {event_name}"
        if event["item"] == CIRCUIT_OVERRIDE:
            location_full_name += f" {room_info.circuit_override_number}"
            room_info.circuit_override_number += 1

        self.add_location(
            location_full_name,
            "Default",
            "EVENT",
            event)

        for mode, conditions in event["condition"].items():
            if conditions[0] not in self.ctx.rando_data["softLockAreas"][mode]:
                self.add_item(event["item"], event["amount"], mode)

    def add_element(self, element: typing.Dict[str, typing.Any], room_info: RoomInfo):
        element_name = element["item"].title()

        location_full_name = f"{room_info.room_name} - {element_name}"

        self.add_location(
            location_full_name,
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
        rando_items_dict = self.ctx.rando_data["items"]

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

        # items_dict is a list containing objects representing maps and the Chests and Events found therein
        for dev_name, room in rando_items_dict.items():
            room_info = RoomInfo(dev_name, room)
            # loop over the chests in the room
            for chest in dict.values(room["chests"]):
                self.add_chest(chest, room_info)

            for events in dict.values(room["events"]):
                for event in events:
                    self.add_event(event, room_info)

            if "elements" in room:
                for element in dict.values(room["elements"]):
                    self.add_element(element, room_info)

        for dev_name, quest in dict.items(self.ctx.rando_data["quests"]):
            self.add_quest(dev_name, quest)

        for mode, regions in self.ctx.rando_data["areas"].items():
            region_map = RegionMap(mode, self.ctx)
            for connection in regions:
                region_map.add_region_connection(connection)

            self.region_maps[mode] = region_map
