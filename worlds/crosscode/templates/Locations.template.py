{{generated_comment | indent("# ", True)}}

import typing
from BaseClasses import Location, Region

# Types of Check
CHECK_ELEMENT = 1
CHECK_CHEST = 2
CHECK_EVENT = 3
CHECK_SHOP = 4
CHECK_QUEST = 5

class Condition(typing.NamedTuple):
    cutscenes: typing.List[str] = []
    items: typing.List[typing.Tuple[str, int]] = []
    quests: typing.List[str] = []
    regions: typing.List[str] = []

class LocationData(typing.NamedTuple):
    name: str
    code: int
    region: typing.Dict[str, str]
    condition: Condition
    clearance: str = "Default"
    kind: int = CHECK_CHEST

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

# GENERATED CODE
# DO NOT TOUCH
locations_data = [
    {{locations_data | indent(4)}}
]
