from typing import NamedTuple
from BaseClasses import Item

class CrossCodeItem(Item):
    game: str = "CrossCode"

class ItemData(NamedTuple):
    item_id: int
    amount: int
    name: str

    def __hash__(self):
        return hash((self.item_id, self.amount))

    def __eq__(self, other):
        return self.item_id == other.item_id and self.amount == other.amount

#items_data = [
#{{items_data}}
#]
