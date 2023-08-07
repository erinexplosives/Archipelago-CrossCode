from typing import NamedTuple
from BaseClasses import Item, ItemClassification

class CrossCodeItem(Item):
    game: str = "CrossCode"

class ItemData(NamedTuple):
    name: str
    item_id: int
    amount: int
    combo_id: int
    classification: ItemClassification
    quantity: int

    def __hash__(self):
        return hash((self.item_id, self.amount))

    def __eq__(self, other):
        return self.item_id == other.item_id and self.amount == other.amount

items_data = [
{{items_data}}
]
