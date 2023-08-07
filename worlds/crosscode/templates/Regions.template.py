import typing
from BaseClasses import Region, Entrance

class RegionConnection(typing.NamedTuple):
    region_from: str
    region_to: str
    cond_elements: typing.List[str]
    cond_items: typing.List[typing.Tuple[str, int]]

region_list: typing.List[str] = [
{{region_list}}
]

region_connections: typing.List[RegionConnection] = [
{{region_connections}}
]
