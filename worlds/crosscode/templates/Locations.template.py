import typing
from BaseClasses import Location

# Types of Check
CHECK_ELEMENT = 1
CHECK_CHEST = 2
CHECK_EVENT = 3
CHECK_SHOP = 4
CHECK_QUEST = 5

class CrossCodeLocation(Location):
    game: str = "CrossCode"

    def __init__(self, player: int, name = "", code = None, parent = None):
        super(CrossCodeLocation, self).__init__(player, name, code, parent)
        self.event = code is None

class LocationData(typing.NamedTuple):
    name: str
    clearance: str
    region: str
    kind: int
    cond_elements: typing.List[str]
    cond_items: typing.List[typing.Tuple[str, int]]

# GENERATED CODE
# DO NOT TOUCH
locations_data = [
{{locations_data}}
]
