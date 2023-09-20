import typing
from BaseClasses import CollectionState
from .Locations import Condition, LocationData
from .Regions import RegionConnection

# this is uncharacteristic of me, but i'm hardcoding something here. weird.
clearance_items = {
    "Bronze": "Thief's Key",
    "Silver": "White Key",
    "Gold": "Radiant Key",
}

def condition_satisfied(player: int, mode: str, condition: Condition) -> typing.Callable[[CollectionState], bool]:
    def conditions_satisfied_internal(state: CollectionState) -> bool:
        if not all([state.count(item, player) >= amount for item, amount in condition.items]):
            return False
        if not all([state.has(f"{quest} (Event)", player) for quest in condition.quests]):
            return False
        if not all([state.has(f"{location} (Event)", player) for location in condition.locations]):
            return False
        if mode in condition.regions and not all([state.has(f"{region} (Event)", player) for region in condition.regions[mode]]):
            return False
        return True

    return conditions_satisfied_internal

def has_clearance(player: int, clearance: str) -> typing.Callable[[CollectionState], bool]:
    return lambda state: state.has(clearance_items[clearance], player)
