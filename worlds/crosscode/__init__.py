import traceback
from copy import deepcopy
import sys
import typing
from BaseClasses import ItemClassification, Location, LocationProgressType, Region, Item
from worlds.AutoWorld import WebWorld, World
from worlds.crosscode.types.Condition import LocationCondition
from worlds.generic.Rules import add_rule, set_rule

from .codegen.context import Context, make_context_from_directory

from .Common import *
from .Logic import condition_satisfied, has_clearance

from .types.Items import CrossCodeItem
from .types.Locations import Condition, CrossCodeLocation
from .types.World import WorldData
from .types.Regions import RegionsData
from .Options import Reachability, crosscode_options, addon_options

loaded_correctly = True

try:
    from .Builder import WorldBuilder
    from .Items import items_by_full_name
    from .Locations import locations_data
    from .Regions import modes

except Exception as e:
    loaded_correctly = False
    print("Failed to import items, locations, or regions, probably due to faulty code generation.", file=sys.stderr)
    traceback.print_exception(*sys.exc_info())
    print(e, file=sys.stderr)
    single_items_data = []
    single_items_dict = []
    items_by_full_name = {}
    locations_data = []
    crosscode_options = {}

world_data_dict: dict[typing.Any, WorldData] = {}

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
        key: value.combo_id for key, value in items_by_full_name.items()
    }

    location_name_to_id = {
        location.name: location.code for location in locations_data if location.code is not None
    }

    region_dict: dict[str, Region]
    logic_mode: str
    region_pack: RegionsData

    location_events: dict[str, Location]

    world_data: WorldData

    addons: list[str]

    ctx: Context = make_context_from_directory("worlds/crosscode/data")

    def register_reachability(self, option: Reachability, items: typing.Iterable[str]):
        if option == Reachability.option_local:
            local_items = self.multiworld.local_items[self.player].value
            for item in items:
                local_items.add(item)
        elif option == Reachability.option_non_local:
            non_local_items = self.multiworld.non_local_items[self.player].value
            for item in items:
                non_local_items.add(item)

    def create_location(self, location: str, event_from_location=False) -> CrossCodeLocation:
        data, access = self.world_data.locations_data[location]
        return CrossCodeLocation(self.player, data, access, self.logic_mode, self.region_dict, event_from_location=event_from_location)

    def create_item(self, item: str) -> CrossCodeItem:
        return CrossCodeItem(self.player, items_by_full_name[item])

    def create_event_conditions(self, condition: typing.Optional[list[Condition]]):
        if condition is None:
            return

        for c in condition:
            if isinstance(c, LocationCondition):
                name = c.location_name
                location = self.create_location(name, event_from_location=True)
                self.location_events[name] = location
                self.region_dict[location.region].locations.append(location)
                location.place_locked_item(Item(location.name, ItemClassification.progression, None, self.player))

    def generate_early(self):
        if not loaded_correctly:
            raise RuntimeError("Attempting to generate a CrossCode World after unsuccessful code generation")

        self.addons = [name for name in addon_options if getattr(self.multiworld, name)[self.player]]

        addonTuple = tuple(self.addons)

        if addonTuple in world_data_dict:
            self.world_data = world_data_dict[addonTuple]
        else:
            self.world_data = WorldBuilder(deepcopy(self.ctx)).build(self.addons)
            world_data_dict[addonTuple] = self.world_data

        start_inventory = self.multiworld.start_inventory[self.player].value
        self.logic_mode = modes[self.multiworld.logic_mode[self.player].value]
        self.region_pack = self.world_data.region_packs[self.logic_mode]

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
        self.region_dict = {name: Region(name, self.player, self.multiworld) for name in self.region_pack.region_list if name not in self.region_pack.excluded_regions}
        print(self.region_pack.excluded_regions, self.region_dict)
        self.multiworld.regions.extend([val for val in self.region_dict.values()])
        self.location_events = {}

        for conn in self.region_pack.region_connections:
            self.region_dict[conn.region_from].connect(
                self.region_dict[conn.region_to],
                f"{conn.region_from} => {conn.region_to}",
                condition_satisfied(self.player, self.logic_mode, conn.cond) if conn.cond is not None else None
            )

            self.create_event_conditions(conn.cond)

            connection_event = Location(self.player, f"{conn.region_from} => {conn.region_to} (Event)", None, self.region_dict[conn.region_from])

            connection_event.place_locked_item(Item(f"{conn.region_to} (Event)", ItemClassification.progression, None, self.player))

            self.region_dict[conn.region_from].locations.append(connection_event)

        menu_region = Region("Menu", self.player, self.multiworld)
        menu_region.add_exits({self.region_pack.starting_region: "login"})
        self.multiworld.regions.append(menu_region)

        for name, region in self.region_dict.items():
            for data, access_info in self.world_data.locations_data.values():
                if self.logic_mode in access_info.region and access_info.region[self.logic_mode] == name:
                    location = CrossCodeLocation(self.player, data, access_info, self.logic_mode, self.region_dict)
                    region.locations.append(location)
                    self.create_event_conditions(access_info.cond)

            for data, access_info in self.world_data.events_data.values():
                if self.logic_mode in access_info.region and access_info.region[self.logic_mode] == name:
                    location = CrossCodeLocation(self.player, data, access_info, self.logic_mode, self.region_dict)
                    region.locations.append(location)
                    location.place_locked_item(Item(location.data.name, ItemClassification.progression, None, self.player))

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

        for (data, quantity) in self.world_data.items_dict.values():
            if self.logic_mode not in quantity:
                continue

            for _ in range(quantity[self.logic_mode]):
                item = CrossCodeItem(self.player, data)
                try:
                    idx = exclude.index(item)
                except ValueError:
                    self.multiworld.itempool.append(item)
                    continue

                exclude.pop(idx)
                self.multiworld.itempool.append(self.create_item("Sandwich x3"))

        for _ in range(self.world_data.num_needed_items[self.logic_mode]):
            self.multiworld.itempool.append(self.create_item("Sandwich x3"))

    def set_rules(self):
        for _, region in self.region_dict.items():
            for loc in region.locations:
                if not isinstance(loc, CrossCodeLocation):
                    continue
                if loc.access.cond is not None:
                    add_rule(loc, condition_satisfied(self.player, self.logic_mode, loc.access.cond))
                if loc.access.clearance != "Default":
                    add_rule(loc, has_clearance(self.player, loc.access.clearance))

    def fill_slot_data(self):
        return {
            "mode": self.logic_mode,
            "options": {
                "vtShadeLock": self.multiworld.vtShadeLock[self.player].value
            }
        }
