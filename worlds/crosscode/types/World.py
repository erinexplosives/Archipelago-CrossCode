from dataclasses import dataclass
import typing

from .Items import ItemData
from .Locations import AccessInfo, LocationData
from .Regions import RegionsData

@dataclass
class WorldData:
    region_packs: dict[str, RegionsData]

    locations_data: dict[str, tuple[LocationData, AccessInfo]]
    events_data: dict[str, tuple[LocationData, AccessInfo]]
    num_needed_items: dict[str, int]

    items_dict: dict[tuple[str, int], tuple[ItemData, dict[str, int]]]
