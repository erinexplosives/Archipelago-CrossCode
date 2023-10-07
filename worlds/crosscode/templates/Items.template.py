{{generated_comment | indent("# ", True)}}

from BaseClasses import ItemClassification
from .types.Items import SingleItemData

num_types = {{num_items}}

items_data: list[SingleItemData] = [
    {{items_data | indent(4)}}
]

items_dict = {data.name: data for data in items_data}
