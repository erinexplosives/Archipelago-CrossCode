import typing
from BaseClasses import CollectionState
from .types.Locations import Condition, LocationData
from .types.Regions import RegionConnection

# this is uncharacteristic of me, but i'm hardcoding something here. weird.
clearance_items = {
    "Bronze": "Thief's Key",
    "Silver": "White Key",
    "Gold": "Radiant Key",
}

def condition_satisfied(player: int, mode: str, conditions: list[Condition]) -> typing.Callable[[CollectionState], bool]:
    def conditions_satisfied_internal(state: CollectionState) -> bool:
        return all([c.satisfied(state, player, mode) for c in conditions])

    return conditions_satisfied_internal

def has_clearance(player: int, clearance: str) -> typing.Callable[[CollectionState], bool]:
    return lambda state: state.has(clearance_items[clearance], player)
