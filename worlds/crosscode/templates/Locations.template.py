{{generated_comment | indent("# ", True)}}

import typing
from BaseClasses import Location, Region

class Condition(typing.NamedTuple):
    items: typing.List[typing.Tuple[str, int]] = []
    locations: typing.List[str] = []
    regions: typing.List[str] = []

class LocationData(typing.NamedTuple):
    name: str
    code: int | None
    region: typing.Dict[str, str]
    cond: Condition = Condition()
    clearance: str = "Default"

class CrossCodeLocation(Location):
    game: str = "CrossCode"
    data: LocationData
    region: str

    def __init__(self, player: int, data: LocationData, mode, region_dict: dict[str, Region]):
        super(CrossCodeLocation, self).__init__(
            player,
            data.name,
            data.code,
            region_dict[data.region[mode]]
        )

        self.data = data
        self.event = False
        self.region = data.region[mode]

locations_data = [
    {{locations_data | indent(4)}}
]

events_data = [
    {{events_data | indent(4)}}
]
