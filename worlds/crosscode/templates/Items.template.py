{{generated_comment | indent("# ", True)}}

from BaseClasses import ItemClassification
from .types.Items import ItemData

items_data = [
    {{items_data | indent(4)}}
]

items_dict = {data.name: data for data in items_data}
