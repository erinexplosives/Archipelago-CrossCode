import typing

from .ast import AstGenerator
from .parse import JsonParser
from .context import Context
from .util import BASE_ID, RESERVED_ITEM_IDS

from ..types.Items import ItemData
from ..types.Locations import LocationData
from ..types.Regions import RegionsData
from ..types.World import WorldInfo

class WorldBuilder:
    ctx: Context
    ast_generator: AstGenerator
    json_parser: JsonParser
    current_code: int = BASE_ID

    region_packs: dict[str, RegionsData]

    locations_data: list[LocationData]
    events_data: list[LocationData]
    num_needed_items: dict[str,int]
    
    items_dict: dict[tuple[str, int], ItemData]

    def __init__(self, ctx: Context):
        self.ctx = ctx

        self.ast_generator = AstGenerator()
        self.json_parser = JsonParser(self.ctx)

        self.region_packs = {}

        self.locations_data = []
        self.events_data = []
        self.num_needed_items = {}

        self.items_dict = {}

    def __add_location(self, name: str, raw_loc: dict[str, typing.Any], create_event=False):
        num_rewards = 1
        if "reward" in raw_loc:
            if len(raw_loc["reward"]) == 0:
                raise RuntimeError(f"Error while adding location {name}: need one or more rewards (get rid of the entry if there are no rewards)")
            num_rewards = len(raw_loc["reward"])
        
        location_names: list[str] = []

        for idx in range(num_rewards):
            full_name = name
            if num_rewards > 1:
                full_name = full_name + f" - Reward {idx + 1}"

            location_names.append(full_name)

            loc = self.json_parser.parse_location(full_name, raw_loc, self.current_code)
            self.current_code += 1

            self.locations_data.append(loc)

        if num_rewards > 1 or create_event:
            prev_loc = self.locations_data[-1]
            event = LocationData(
                name=f"{name} (Event)",
                code=None,
                region=prev_loc.region,
                cond=prev_loc.cond)
            self.events_data.append(event)

        if "reward" not in raw_loc or len(raw_loc["reward"]) == 0:
            for mode in raw_loc["region"].keys():
                if not mode in self.num_needed_items:
                    self.num_needed_items[mode] = 1
                else:
                    self.num_needed_items[mode] += 1
            return

        for reward in raw_loc["reward"]:
            item = self.json_parser.parse_reward(reward) 
            key = (item.name, item.amount)
            if key in self.items_dict:
                item = self.items_dict[key]
            else:
                self.items_dict[key] = item

            for mode in raw_loc["region"].keys():
                if not mode in item.quantity:
                    item.quantity[mode] = 1
                else:
                    item.quantity[mode] += 1

    def __add_location_list(self, loc_list: dict[str, dict[str, typing.Any]], create_events=False):
        for name, raw_loc in loc_list.items():
            self.__add_location(name, raw_loc, create_events)

    def build(self) -> WorldInfo:
        self.__add_location_list(self.ctx.rando_data["chests"])
        self.__add_location_list(self.ctx.rando_data["cutscenes"])
        self.__add_location_list(self.ctx.rando_data["elements"])
        self.__add_location_list(self.ctx.rando_data["quests"], True)

        self.region_packs = self.json_parser.parse_regions_data_list(self.ctx.rando_data["regions"])

        items_data = [item for item in self.items_dict.values()]
        items_data.sort()

        return WorldInfo(
            region_packs=self.region_packs,
            locations_data=self.locations_data,
            events_data=self.events_data,
            num_needed_items=self.num_needed_items,
            items_data=items_data
        )
