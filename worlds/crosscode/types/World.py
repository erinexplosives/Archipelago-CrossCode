import typing

from .Items import ItemData
from .Locations import LocationData
from .Regions import RegionsData

class WorldInfo(typing.NamedTuple):
    region_packs: dict[str, RegionsData]

    locations_data: list[LocationData]
    events_data: list[LocationData]
    num_needed_items: dict[str, int]

    items_data: list[ItemData]
