from BaseClasses import Region
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import set_rule
from .Common import *
from .Items import CrossCodeItem, items_data, items_dict
from .Locations import CrossCodeLocation, locations_data
from .Logic import conditions_satisfied
from .Options import crosscode_options
from .Regions import region_list, region_connections, starting_region

class CrossCodeWebWorld(WebWorld):
    theme="ocean"

class CrossCodeWorld(World):
    game = NAME
    web = CrossCodeWebWorld()

    option_definitions = crosscode_options
    topology_present = True

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a propery.
    base_id = BASE_ID
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {
        item.name : item.combo_id for item in items_data
    }

    location_name_to_id = {
        location.name: location.code for location in locations_data
    }

    region_dict: dict[str, Region]

    def create_item(self, item: str) -> CrossCodeItem:
        return CrossCodeItem(self.player, items_dict[item])

    def create_regions(self):
        self.region_dict = {name: Region(name, self.player, self.multiworld) for name in region_list}
        self.multiworld.regions.extend([val for val in self.region_dict.values()])

        for conn in region_connections:
            self.region_dict[conn.region_from].add_exits(
                {conn.region_to: f"{conn.region_from} <-> {conn.region_to}"},
                {conn.region_to: conditions_satisfied(self.player, conn)},
            )

        menu_region = Region("Menu", self.player, self.multiworld)
        menu_region.add_exits({starting_region: "login"})
        self.multiworld.regions.append(menu_region)

        for name, region in self.region_dict.items():
            region.locations = \
                [CrossCodeLocation(self.player, data, self.region_dict) for data in locations_data if data.region == name]

    def create_items(self):
        for data in items_data:
            for _ in range(data.quantity):
                item = CrossCodeItem(self.player, data)
                self.multiworld.itempool.append(item)

    def set_rules(self):
        for name, region in self.region_dict.items():
            for loc in region.locations:
                set_rule(loc, conditions_satisfied(self.player, loc.data))
