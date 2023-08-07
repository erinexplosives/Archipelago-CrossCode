import typing
from BaseClasses import Location, Region

# Types of Check
CHECK_ELEMENT = 1
CHECK_CHEST = 2
CHECK_EVENT = 3
CHECK_SHOP = 4
CHECK_QUEST = 5

class LocationData(typing.NamedTuple):
    name: str
    code: int
    clearance: str
    region: str
    kind: int
    cond_elements: typing.List[str]
    cond_items: typing.List[typing.Tuple[str, int]]

class CrossCodeLocation(Location):
    game: str = "CrossCode"

    def __init__(self, player: int, data: LocationData, regionDict: dict[str, Region]):
        super(CrossCodeLocation, self).__init__(
            player,
            data.name,
            data.code,
            regionDict[data.region]
        )

        self.event = False

# GENERATED CODE
# DO NOT TOUCH
locations_data = [
{{locations_data}}
]
