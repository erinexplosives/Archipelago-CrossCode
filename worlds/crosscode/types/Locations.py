import typing
from BaseClasses import Location, Region

class Condition(typing.NamedTuple):
    items: list[typing.Tuple[str, int]] = []
    quests: list[str] = []
    locations: list[str] = []
    regions: dict[str, typing.List[str]] = {}

    def is_empty(self) -> bool:
        return len(self.items) == 0 \
                and len(self.quests) == 0 \
                and len(self.locations) == 0 \
                and len(self.regions) == 0

def empty_condition():
    return Condition([], [], [], {})

class LocationData(typing.NamedTuple):
    name: str
    code: typing.Optional[int]
    region: typing.Dict[str, str]
    cond: typing.Optional[Condition] = None
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
