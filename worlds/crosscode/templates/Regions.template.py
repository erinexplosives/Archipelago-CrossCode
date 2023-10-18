{{generated_comment | indent("# ", True)}}

import typing

from .types.Regions import RegionConnection, RegionsData
from .types.Condition import *

modes = [ {{ modes_string }} ]
default_mode = "{{ default_mode }}"

region_packs: typing.Dict[str, RegionsData] = {
    {% for mode, r in region_packs.items() -%}
    "{{mode}}": RegionsData(
        starting_region = "{{r.starting_region}}",
        goal_region = "{{r.goal_region}}",
        excluded_regions = {{r.excluded_regions}},
        region_list = {{region_lists[mode] | indent(8)}},
        region_connections = {{region_connections[mode] | indent(8)}}
    ),
    {% endfor %}
}
