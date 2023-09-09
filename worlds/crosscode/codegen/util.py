import json

BASE_ID = 300000

# I reserve some item IDs at the beginning of our slot for elements
# and other items that don't map to CrossCode items
RESERVED_ITEM_IDS = 100

CIRCUIT_OVERRIDE = 428

GENERATED_COMMENT = """WARNING: THIS FILE HAS BEEN GENERATED!
Modifications to this file will not be kept.
If you need to change something here, check out codegen.py and the templates directory.
"""


def get_json_object(filename: str):
    with open(filename, "r") as f:
        return json.load(f)
