{{generated_comment | indent("# ", True)}}

import typing
from BaseClasses import Region, Entrance

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

modes = [ {{ modes_string }} ]
default_mode = "{{ default_mode }}"

region_packs: typing.Dict[str, RegionsData] = {
    {% for r in region_packs -%}
    "{{r.name}}": RegionsData(
        starting_region = "{{r.starting_region}}",
        goal_region = "{{r.goal_region}}",
        excluded_regions = {{r.excluded_regions}},
        region_list = [
            {{r.region_list | indent(12)}}
        ],
        region_connections = [
            {{r.region_connections | indent(12)}}
        ]
    ),
    {% endfor %}
}
