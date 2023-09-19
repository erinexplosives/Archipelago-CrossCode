import typing
from BaseClasses import ItemClassification, Location, LocationProgressType, Region, Item
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule
from .Common import *
from .Items import CrossCodeItem, items_data, items_dict
from .Locations import CrossCodeLocation, locations_data
from .Logic import condition_satisfied, has_clearance
from .Options import Reachability, crosscode_options
from .Regions import RegionsData, region_packs, modes

class CrossCodeWebWorld(WebWorld):
    theme="ocean"

class CrossCodeWorld(World):
    """CrossCode is a retro-inspired 2D Action RPG set in the distant future,
    combining 16-bit SNES-style graphics with butter-smooth physics, a
    fast-paced combat system, and engaging puzzle mechanics, served with a
    gripping sci-fi story.
    """
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
    logic_mode: str
    region_pack: RegionsData

    def register_reachability(self, option: Reachability, items: typing.Iterable[str]):
        if option == Reachability.option_local:
            local_items = self.multiworld.local_items[self.player].value
            for item in items:
                local_items.add(item)
        elif option == Reachability.option_non_local:
            non_local_items = self.multiworld.non_local_items[self.player].value
            for item in items:
                non_local_items.add(item)
        
    def create_item(self, item: str) -> CrossCodeItem:
        return CrossCodeItem(self.player, items_dict[item])

    def generate_early(self):
        start_inventory = self.multiworld.start_inventory[self.player].value
        self.logic_mode = modes[self.multiworld.logic_mode[self.player].value]
        self.region_pack = region_packs[self.logic_mode]

        if self.multiworld.start_with_green_leaf_shade[self.player].value:
            start_inventory["Green Leaf Shade"] = 1

        shade_loc: Reachability = self.multiworld.shade_locations[self.player].value
        element_loc: Reachability = self.multiworld.element_locations[self.player].value

        self.register_reachability(
            shade_loc,
            (
                "Green Leaf Shade", "Yellow Sand Shade", "Blue Ice Shade",
                "Red Flame Shade", "Purple Bolt Shade", "Azure Drop Shade",
                "Green Seed Shade", "Star Shade", "Meteor Shade",
            )
        )

        self.register_reachability(element_loc, ("Heat", "Cold", "Shock", "Wave"))


    def create_regions(self):
        self.region_dict = {name: Region(name, self.player, self.multiworld) for name in self.region_pack.region_list}
        self.multiworld.regions.extend([val for val in self.region_dict.values()])

        for conn in self.region_pack.region_connections:
            self.region_dict[conn.region_from].add_exits(
                {conn.region_to: f"{conn.region_from} <-> {conn.region_to}"},
                {conn.region_to: condition_satisfied(self.player, conn.cond)},
            )

        menu_region = Region("Menu", self.player, self.multiworld)
        menu_region.add_exits({self.region_pack.starting_region: "login"})
        self.multiworld.regions.append(menu_region)

        for name, region in self.region_dict.items():
            region.locations = []
            for data in locations_data:
                if self.logic_mode in data.region and data.region[self.logic_mode] == name:
                    region.locations.append(CrossCodeLocation(self.player, data, self.logic_mode, self.region_dict))

            if name in self.region_pack.excluded_regions:
                for location in region.locations:
                    location.progress_type = LocationProgressType.EXCLUDED

        victory = Region("Floor ??", self.player, self.multiworld)
        self.multiworld.regions.append(victory)

        loc = Location(self.player, "The Creator", parent=victory)
        victory.locations = [loc]

        loc.place_locked_item(Item("Victory", ItemClassification.progression, None, self.player))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        self.region_dict[self.region_pack.goal_region].add_exits(["Floor ??"])

    def create_items(self):
        exclude = self.multiworld.precollected_items[self.player][:]

        for data in items_data:
            if self.logic_mode not in data.quantity:
                continue

            for _ in range(data.quantity[self.logic_mode]):
                item = CrossCodeItem(self.player, data)
                try:
                    idx = exclude.index(item)
                except ValueError:
                    self.multiworld.itempool.append(item)
                    continue

                exclude.pop(idx)
                self.multiworld.itempool.append(self.create_item("Chef Sandwich x2"))

    def set_rules(self):
        for _, region in self.region_dict.items():
            for loc in region.locations:
                add_rule(loc, condition_satisfied(self.player, loc.data.cond))
                if loc.data.clearance != "Default":
                    add_rule(loc, has_clearance(self.player, loc.data.clearance))

    def fill_slot_data(self):
        return {
            "mode": self.logic_mode,
            "options": {
                "vtShadeLock": self.multiworld.vt_shade_lock[self.player].value
            }
        }
