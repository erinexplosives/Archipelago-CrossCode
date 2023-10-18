import abc
from dataclasses import dataclass

from BaseClasses import CollectionState

class Condition(abc.ABC):
    @abc.abstractmethod
    def satisfied(self, state: CollectionState, player: int, mode: str) -> bool:
        pass

@dataclass
class ItemCondition(Condition):
    item_name: str
    amount: int = 1

    def satisfied(self, state: CollectionState, player: int, _: str) -> bool:
        return state.has(self.item_name, player, self.amount)

@dataclass
class QuestCondition(Condition):
    quest_name: str

    def satisfied(self, state: CollectionState, player: int, _: str) -> bool:
        return state.has(f"{self.quest_name} (Event)", player)

@dataclass
class LocationCondition(Condition):
    location_name: str

    def satisfied(self, state: CollectionState, player: int, _: str) -> bool:
        return state.has(f"{self.location_name} (Event)", player)

@dataclass
class RegionCondition(Condition):
    target_mode: str
    region_name: str

    def satisfied(self, state: CollectionState, player: int, mode: str) -> bool:
        return mode != self.target_mode or state.has(f"{self.region_name} (Event)", player)
