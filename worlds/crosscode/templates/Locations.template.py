{{generated_comment | indent("# ", True)}}

import typing
from BaseClasses import Location, Region

class Condition(typing.NamedTuple):
    items: typing.List[typing.Tuple[str, int]] = []
    quests: typing.List[str] = []
    locations: typing.List[str] = []
    regions: typing.Dict[str, typing.List[str]] = {}

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

    def __init__(self, player: int, data: LocationData, mode, region_dict: dict[str, Region], event_from_location=False):
        event_from_location = event_from_location and data.code is not None

        super(CrossCodeLocation, self).__init__(
            player,
            data.name if not event_from_location else data.name + " (Event)",
            data.code if not event_from_location else None,
            region_dict[data.region[mode]]
        )

        self.data = data
        self.event = False
        self.region = data.region[mode]

needed_items = {{needed_items}}

locations_data = [
    {{locations_data | indent(4)}}
]

locations_dict = { location.name: location for location in locations_data }

events_data = [
    {{events_data | indent(4)}}
]
