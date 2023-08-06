# This is the script that runs the code generation, producing:
# - `Locations.py' from `Locations.template.py'
# - `Items.py' from `Items.template.py'
#
# This process requires a few data files.
# Put the following files in the `data' directory:
# - `item-database.json' from your CrossCode installation
# - `data.json' from the CCItemRandomizer mod
#
# You can either run this as a script or by calling functions
# `__init__.py' is planned to run this script when it cannot find the files in question

import json
import jinja2
import ast

def get_json_object(filename: str):
    with open(filename, "r") as f:
        return json.load(f)

def generate_locations(rando_data):
    items_dict = rando_data["items"]

    ast_item_list = []

    offset: int = 0

    # items_dict is a list containing objects representing maps and the Chests and Events found therein
    for dev_name, room in items_dict.items():
        room_name: str = room["name"] if "name" in room else dev_name
        chests = room["chests"]

        chest_amounts = {}

        if len(chests) > 1:
            for level in ["Default", "Bronze", "Silver", "Gold"]:
                chest_amounts[level] = [0, len(list(filter(lambda c: c["type"] == level, dict.values(chests))))]

        for chest in dict.values(room["chests"]):
            region = chest["condition"][0]
            clearance = chest["type"]
            chest_name = "Chest" if clearance == "Default" else f"{clearance} Chest"

            if clearance in chest_amounts and chest_amounts[clearance][1] > 1:
                chest_amounts[clearance][0] += 1
                chest_name += f" {chest_amounts[clearance][0]}"

            full_name = f"{room_name} - {chest_name}"

            ast_item = ast.Call(
                    func=ast.Name("LocationData"),
                    args=[],
                    keywords=[
                        ast.keyword(
                            arg="name",
                            value=ast.Constant(full_name)
                        ),
                        ast.keyword(
                            arg="offset",
                            value=ast.Constant(offset)
                        ),
                        ast.keyword(
                            arg="clearance",
                            value=ast.Constant(clearance)
                        ),
                        ast.keyword(
                            arg="region",
                            value=ast.Constant(region)
                        ),
                    ]
            )
            ast.fix_missing_locations(ast_item)
            ast_item_list.append(ast_item)

            offset += 1

    code_item_list = ["\t" + ast.unparse(item) for item in ast_item_list]
    code = ",\n".join(code_item_list)

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    template = environment.get_template("Locations.template.py")
    locations_complete = template.render(locations_data=code)

    with open("Locations.py", "w") as f:
        f.write(locations_complete)

if __name__ == "__main__":
    rando_data = get_json_object("data/data.json")
    generate_locations(rando_data)
