import typing

from .Locations import Condition

class RegionConnection(typing.NamedTuple):
    region_from: str
    region_to: str
    cond: Condition

class RegionsData(typing.NamedTuple):
    starting_region: str
    goal_region: str
    excluded_regions: typing.List[str]
    region_list: typing.List[str]
    region_connections: typing.List[RegionConnection]
