from worlds.AutoWorld import World
from .Common import *
from .Locations import locations_data
from .Options import crosscode_options

class CrossCodeWorld(World):
    game = "CrossCode"
    option_definitions = crosscode_options
    topology_present = True

    # data_version is used to signal that items, locations or their names
    # changed. Set this to 0 during development so other games' clients do not
    # cache any texts, then increase by 1 for each release that makes changes.
    data_version = 0

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a propery.
    base_id = BASE_ID
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {
        item.item_name : BASE_ID + item.item_id for item in crosscode_items
    }

    location_name_to_id = {
        location.name: BASE_ID + idx for idx, location in enumerate(locations_data)
    }
