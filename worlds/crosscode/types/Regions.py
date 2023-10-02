import typing

from .Condition import Condition

class RegionConnection(typing.NamedTuple):
    region_from: str
    region_to: str
    cond: typing.Optional[list[Condition]]

class RegionsData(typing.NamedTuple):
    starting_region: str
    goal_region: str
    excluded_regions: typing.List[str]
    region_list: typing.List[str]
    region_connections: typing.List[RegionConnection]
