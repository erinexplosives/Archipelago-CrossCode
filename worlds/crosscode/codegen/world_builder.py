import typing

from .context import Context
from .util import BASE_ID, RESERVED_ITEM_IDS
from ..types.Items import ItemData
from ..types.Locations import LocationData
from ..types.Regions import RegionsData
from ..types.World import WorldInfo

class WorldBuilder:
    ctx: Context
    current_code: int = BASE_ID

    region_packs: dict[str, RegionsData]

    locations_data: list[LocationData]
    events_data: list[LocationData]
    num_needed_items: dict[str,int]
    
    items_data: dict[tuple[str, int], ItemData]

    def __init__(self, ctx: Context):
        self.ctx = ctx

        self.region_packs = {}

        self.locations_data = []
        self.events_data = []

        self.items_data = {}

    def __add_location_list(self, loc_list: dict[str, dict[str, typing.Any]]):
        for name, raw_loc in loc_list.items():
            loc = self.ctx.json_parser.parse_location(name, raw_loc, self.current_code)
            self.current_code += 1

            self.locations_data.append(loc)

            if "reward" not in raw_loc or len(raw_loc["reward"]) == 0:
                for mode in loc.region.keys():
                    if not mode in self.num_needed_items:
                        self.num_needed_items[mode] = 1
                    else:
                        self.num_needed_items[mode] += 1
                continue

            for reward in raw_loc["reward"]:
                item = self.ctx.json_parser.parse_reward(reward) 
                key = (item.name, item.amount)
                if key in self.items_data:
                    item = self.items_data[key]
                else:
                    self.items_data[key] = item

                for mode in loc.region.keys():
                    if not mode in item.quantity:
                        item.quantity[mode] = 1
                    else:
                        item.quantity[mode] += 1

    def build(self) -> WorldInfo:
        self.__add_location_list(self.ctx.rando_data["chests"])
        self.__add_location_list(self.ctx.rando_data["cutscenes"])
        self.__add_location_list(self.ctx.rando_data["elements"])
        self.__add_location_list(self.ctx.rando_data["quests"])

        self.region_packs = self.ctx.json_parser.parse_regions_data_list(self.ctx.rando_data["regions"])

        return WorldInfo(
            region_packs=self.region_packs,
            locations_data=self.locations_data,
            events_data=self.events_data,
            num_needed_items=self.num_needed_items,
            items_data=self.items_data
        )
