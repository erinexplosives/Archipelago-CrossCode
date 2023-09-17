import json
import os
import typing

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


def load_json_with_includes(filename: str) -> typing.Dict[str, typing.Any]:
    master = get_json_object(filename)
    dirname = os.path.dirname(filename)

    if not isinstance(master, dict):
        raise RuntimeError(f"error loading file '{filename}': root should be an object")
    if not "includes" in master:
        return master

    includes = master.pop("includes")
    for subfilename in includes:
        subfile = load_json_with_includes(f"{dirname}/{subfilename}")

        for key, value in subfile.items():
            if key in master:
                raise RuntimeError(f"error adding {subfilename}: cannot add key {key} to master")

            master[key] = value

    return master
