{{generated_comment | indent("# ", True)}}

from BaseClasses import ItemClassification
from .types.Items import ItemData, SingleItemData

num_items = {{num_items}}

single_items_dict: dict[str, SingleItemData] = {{single_items_dict}}

items_dict: dict[tuple[str, int], ItemData] = {{items_dict}}

item_data_by_name: dict[str, ItemData] = { f"{name} x{amount}" if amount > 1 else name: value for (name, amount), value in items_dict.items() }
