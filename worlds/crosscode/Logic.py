import typing
from BaseClasses import CollectionState
from .Locations import LocationData
from .Regions import RegionConnection

# this is uncharacteristic of me, but i'm hardcoding something here. weird.
clearance_items = {
    "Bronze": "Thief's Key",
    "Silver": "White Key",
    "Gold": "Radiant Key",
}

def conditions_satisfied_location(player: int, mode: str, data: LocationData) -> typing.Callable[[CollectionState], bool]:
    def conditions_satisfied_internal(state: CollectionState) -> bool:
        if not state.has_all(set(data.access[mode].cond_elements), player):
            return False
        if False in [state.count(item, player) >= amount for item, amount in data.access[mode].cond_items]:
            return False
        if isinstance(data, LocationData) and data.clearance != "Default":
            if not state.has(clearance_items[data.clearance], player):
                return False
        return True

    return conditions_satisfied_internal

def conditions_satisfied_region(player: int, data: RegionConnection) -> typing.Callable[[CollectionState], bool]:
    def conditions_satisfied_internal(state: CollectionState) -> bool:
        if not state.has_all(set(data.cond_elements), player):
            return False
        if False in [state.count(item, player) >= amount for item, amount in data.cond_items]:
            return False
        return True

    return conditions_satisfied_internal
