import typing
from BaseClasses import CollectionState
from .Locations import LocationData
from .Regions import RegionConnection

def conditions_satisfied(player: int, data: LocationData | RegionConnection) -> typing.Callable[[CollectionState], bool]:
    def conditions_satisfied_internal(state: CollectionState) -> bool:
        if not state.has_all(set(data.cond_elements), player):
            return False
        if False in [state.count(item, player) >= amount for item, amount in data.cond_items]:
            return False
        return True

    return conditions_satisfied_internal
