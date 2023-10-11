import typing

from .codegen.ast import AstGenerator
from .codegen.lists import ListInfo
from .codegen.parse import JsonParser
from .codegen.context import Context
from .codegen.util import BASE_ID
from .codegen.merge import merge

from .types.Items import ItemData
from .types.Locations import AccessInfo, LocationData
from .types.Regions import RegionsData
from .types.World import WorldData

from .Items import single_items_dict
from .Locations import locations_dict, events_dict
from .Regions import modes

class WorldBuilder:
    ctx: Context
    ast_generator: AstGenerator
    json_parser: JsonParser
    current_location_code: int

    lists: ListInfo

    region_packs: dict[str, RegionsData]
    locations_access: dict[str, tuple[LocationData, AccessInfo]]
    events_access: dict[str, tuple[LocationData, AccessInfo]]
    items_dict: dict[tuple[str, int], tuple[ItemData, dict[str, int]]]

    num_needed_items: dict[str,int]

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.ast_generator = AstGenerator()
        self.json_parser = JsonParser(self.ctx)
        self.current_location_code = BASE_ID

        self.lists = ListInfo(self.ctx)
        self.lists.events_data = events_dict
        self.lists.locations_data = locations_dict
        self.lists.single_items_dict = single_items_dict

        self.json_parser.single_items_dict = single_items_dict

        self.region_packs = {}
        self.locations_access = {}
        self.events_access = {}
        self.items_dict = {}

        self.num_needed_items = {mode: 0 for mode in modes}

    def __add_location(self, name: str, raw_loc: dict[str, typing.Any], create_event=False):
        num_rewards = 1
        if "reward" in raw_loc:
            if len(raw_loc["reward"]) == 0:
                raise RuntimeError(f"Error while adding location {name}: need one or more rewards (get rid of the entry if there are no rewards)")
            num_rewards = len(raw_loc["reward"])

        access_info = None

        for idx in range(num_rewards):
            full_name = name
            if num_rewards > 1:
                full_name = full_name + f" - Reward {idx + 1}"

            access_info = self.json_parser.parse_location_access_info(raw_loc)
            self.locations_access[name] = (locations_dict[name], access_info)
            self.current_location_code += 1

        if access_info is not None and (num_rewards > 1 or create_event):
            event = events_dict[f"{name} (Event)"]
            self.events_access[name] = (event, access_info)

        if "reward" not in raw_loc or len(raw_loc["reward"]) == 0:
            for mode in raw_loc["region"].keys():
                self.num_needed_items[mode] += 1
            return

        for reward in raw_loc["reward"]:
            item = self.json_parser.parse_reward(reward) 
            key = (item.name, item.amount)
            if key in self.items_dict:
                item, quantity = self.items_dict[key]
            else:
                quantity = {}
                self.items_dict[key] = (item, quantity)

            for mode in raw_loc["region"].keys():
                if access_info is not None and \
                        access_info.region[mode] in self.region_packs[mode].excluded_regions:
                    continue

                if not mode in quantity:
                    quantity[mode] = 1
                else:
                    quantity[mode] += 1

    def __add_location_list(self, loc_list: dict[str, dict[str, typing.Any]], create_events=False):
        for name, raw_loc in loc_list.items():
            self.__add_location(name, raw_loc, create_events)

    def build(self, addons: list[str]) -> WorldData:
        for name in addons:
            self.ctx.rando_data = merge(self.ctx.rando_data, self.ctx.addons[name])

        self.region_packs = self.json_parser.parse_regions_data_list(self.ctx.rando_data["regions"])

        self.__add_location_list(self.ctx.rando_data["chests"])
        self.__add_location_list(self.ctx.rando_data["cutscenes"])
        self.__add_location_list(self.ctx.rando_data["elements"])
        self.__add_location_list(self.ctx.rando_data["quests"], True)

        return WorldData(
            region_packs=self.region_packs,
            locations_data=self.locations_access,
            events_data=self.events_access,
            num_needed_items=self.num_needed_items,
            items_dict=self.items_dict,
        )
