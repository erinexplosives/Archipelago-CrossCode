# This is the script that runs the code generation, producing:
# - `Locations.py' from `Locations.template.py'
# - `Items.py' from `Items.template.py'
#
# This process requires a few data files.
# Put the following files in the `data' directory:
# - `item-database.json' from your CrossCode installation
# - `data.json' from the CCItemRandomizer mod

import json
import jinja2
import ast
import typing

def get_json_object(filename: str):
    with open(filename, "r") as f:
        return json.load(f)

rando_data = get_json_object("data/data.json")
item_data = get_json_object("data/item-database.json")

BASE_ID = 300000

COND_ELEMENT = 1
COND_ITEM = 2

def parse_condition(cond: str) -> typing.Tuple[int, ast.expr]:
    if cond in {"heat", "cold", "shock", "wave"}:
        return (COND_ELEMENT, ast.Constant(f"{cond.title()}"))

    # This is the part of the code where I write a poor man's parser.
    # Because this data could be inputted by a user, I made it *EXTREMELY* fault-tolerant
    try:
        lhs, rhs = cond.split(">=")
    except ValueError:
        raise RuntimeError(f"Unrecognized condition format: `{cond}`")

    try:
        amount = int(rhs.strip())
    except ValueError:
        raise RuntimeError(f"Invalid count: `{rhs.strip()}`")

    try:
        word_item, number, word_amount = lhs.strip().split(".")
        if word_item != "item" and word_amount != "amount":
            raise RuntimeError(f"Need `item.{number}.amount`, not `{lhs}`")
    except ValueError:
        raise RuntimeError(f"Need three words separated by dots, not `{lhs}`")

    try:
        number = int(number)
    except ValueError:
        raise RuntimeError(f"Not an item ID: `{number}`")

    try:
        item_name = item_data["items"][number]["name"]["en_US"]
    except IndexError:
        raise RuntimeError(f"Item ID doesn't fit: `{number}`")

    return (COND_ITEM, ast.Tuple([ast.Constant(item_name), ast.Constant(amount)]))


def get_item_classification(item: dict) -> str:
    """Deduce the classification of an item based on its item-database entry"""
    if item["type"] == "CONS" or item["type"] == "TRADE":
        return "filler"
    elif item["type"] == "KEY":
        return "progression"
    elif item["type"] == "EQUIP":
        return "useful"
    elif item["type"] == "TOGGLE":
        if "Booster" in item["name"]["en_US"]:
            return "progression"
        else:
            return "filler"
    else:
        raise RuntimeError(f"I don't know how to classify this item: {item['name']}")

def create_ast_call_location(name: str, clearance: str, region: str, kind: str, conditions: typing.List[str]) -> ast.Call:
    cond_elements = ast.List([])
    cond_items = ast.List([])

    for cond in conditions:
        cond_type, tree = parse_condition(cond)

        if cond_type == COND_ELEMENT:
            cond_elements.elts.append(tree)
        elif cond_type == COND_ITEM:
            cond_items.elts.append(tree)

    ast_item = ast.Call(
        func=ast.Name("LocationData"),
        args=[],
        keywords=[
            ast.keyword(
                arg="name",
                value=ast.Constant(name)
            ),
            ast.keyword(
                arg="clearance",
                value=ast.Constant(clearance)
            ),
            ast.keyword(
                arg="region",
                value=ast.Constant(region)
            ),
            ast.keyword(
                arg="kind",
                value=ast.Name(f"CHECK_{kind}"),
            ),
            ast.keyword(
                arg="cond_elements",
                value=cond_elements
            ),
            ast.keyword(
                arg="cond_items",
                value=cond_items
            ),
        ]
    )
    ast.fix_missing_locations(ast_item)
    return ast_item

def create_ast_call_item(name: str, item_id: int, amount: int, combo_id: int, classification: str) -> ast.Call:
    ast_item = ast.Call(
        func=ast.Name("ItemData"),
        args=[],
        keywords=[
            ast.keyword(
                arg="name",
                value=ast.Constant(name)
            ),
            ast.keyword(
                arg="item_id",
                value=ast.Constant(item_id)
            ),
            ast.keyword(
                arg="amount",
                value=ast.Constant(amount)
            ),
            ast.keyword(
                arg="combo_id",
                value=ast.Constant(combo_id)
            ),
            ast.keyword(
                arg="classification",
                value=ast.Attribute(
                    value=ast.Name("ItemClassification"),
                    attr=classification,
                )
            ),
            ast.keyword(
                arg="quantity",
                value=ast.Constant(1)
            ),
        ]
    )
    ast.fix_missing_locations(ast_item)
    return ast_item

def generate_files() -> None:
    rando_items_dict = rando_data["items"]

    itemdb: typing.List = item_data["items"]

    num_items = len(itemdb)

    # stores a list of AST objects representing chests
    # no, I didn't make it store the list as an AST object
    # that just renders it as one long line, which is bad for debugging
    # so I do some steps manually
    ast_location_list: typing.List[ast.Call] = []

    # similar but for items
    # also, IDs are not contiguous so we store these as a dict
    found_items: typing.Dict[int, ast.Call] = {}

    # items_dict is a list containing objects representing maps and the Chests and Events found therein
    for dev_name, room in rando_items_dict.items():
        has_fancy_name = "name" in room
        room_name: str = room["name"] if has_fancy_name else dev_name
        chests = room["chests"]

        # stores a mapping of clearance values to [index of current chest of that clearance value, total chests of that clearance value]
        # helps generate semantic names for chests of same clearance value in the same room
        # so like "Bronze Chest 1" "Bronze Chest 2" etc
        chest_amounts: typing.Dict[str, typing.List[int]] = {}
        if len(chests) > 1:
            for level in ["Default", "Bronze", "Silver", "Gold"]:
                chest_amounts[level] = [0, len(list(filter(lambda c: c["type"] == level, dict.values(chests))))]

        # loop over the chests in the room
        for chest in dict.values(room["chests"]):
            # location stuff
            region = chest["condition"][0]
            clearance = chest["type"]
            chest_name = "Chest" if clearance == "Default" else f"{clearance} Chest"

            conditions = [x for x in chest["condition"][1:] if x != ""]

            if clearance in chest_amounts and chest_amounts[clearance][1] > 1:
                chest_amounts[clearance][0] += 1
                chest_name += f" {chest_amounts[clearance][0]}"

            location_full_name = f"{room_name} - {chest_name}"

            ast_location_list.append(create_ast_call_location(location_full_name, clearance, region, "CHEST", conditions))

            # item stuff
            item_id = chest["item"]
            item_amount = chest["amount"]

            item_info = itemdb[item_id]
            item_name = item_info["name"]["en_US"]

            item_full_name = item_name if item_amount == 1 else f"{item_name} x{item_amount}"

            combo_id = BASE_ID + num_items * (item_amount - 1) + item_id

            if combo_id in found_items:
                quantity = found_items[combo_id].keywords[-1]
                quantity.value.value += 1
                ast.fix_missing_locations(quantity)
            else:
                found_items[combo_id] = create_ast_call_item(item_full_name, item_id, item_amount, combo_id, get_item_classification(item_info))

        for events in dict.values(room["events"]):
            for event in events:
                region = event["condition"][0]
                event_name = itemdb[event["item"]]["name"]["en_US"]

                conditions = [x for x in event["condition"][1:] if x != ""]

                location_full_name = f"{room_name} - {event_name}"

                ast_location_list.append(create_ast_call_location(location_full_name, "Default", region, "EVENT", conditions))

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

    template = environment.get_template("Locations.template.py")

    code_location_list = ["\t" + ast.unparse(item) for item in ast_location_list]
    code = ",\n".join(code_location_list)
    locations_complete = template.render(locations_data=code)

    with open("Locations.py", "w") as f:
        f.write(locations_complete)

    template = environment.get_template("Items.template.py")

    found_item_keys = list(dict.keys(found_items))
    found_item_keys.sort()

    code_item_list = ["\t" + ast.unparse(found_items[k]) for k in found_item_keys]
    code = ",\n".join(code_item_list)
    items_complete = template.render(items_data=code)

    with open("Items.py", "w") as f:
        f.write(items_complete)

if __name__ == "__main__":
    generate_files()
