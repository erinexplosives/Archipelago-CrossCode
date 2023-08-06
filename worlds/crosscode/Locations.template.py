from typing import NamedTuple
from BaseClasses import Location

class CrossCodeLocation(Location):
    game: str = "CrossCode"

    def __init__(self, player: int, name = "", code = None, parent = None):
        super(CrossCodeLocation, self).__init__(player, name, code, parent)
        self.event = code is None

class LocationData(NamedTuple):
    name: str
    offset: int
    clearance: str
    region: str

locations_data = [
{{locations_data}}
]
