import typing
import ast
import string
import os
import json

import jinja2

from .context import Context, make_context_from_directory
from .state import GameState
from .util import GENERATED_COMMENT

class FileGenerator:
    environment: jinja2.Environment
    ctx: Context
    common_args: typing.Dict[str, typing.Any]
    state: GameState
    data_out_dir: str

    def __init__(self, data_dir: str, data_out_dir: str):
        self.ctx = make_context_from_directory(data_dir)
        self.environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
        self.state = GameState(self.ctx)
        self.data_out_dir = data_out_dir

        self.common_args = {
            "generated_comment": GENERATED_COMMENT,
            "modes": self.ctx.rando_data["modes"],
            "default_mode": self.ctx.rando_data["defaultMode"],
        }

    def generate_files(self) -> None:
        self.state.calculate_game_state()

        ### LOCATIONS
        template = self.environment.get_template("Locations.template.py")

        code_location_list = [ast.unparse(item) for item in self.state.ast_location_list]
        code = ",\n".join(code_location_list)
        locations_complete = template.render(locations_data=code, **self.common_args)

        with open("Locations.py", "w") as f:
            f.write(locations_complete)

        ### ITEMS
        template = self.environment.get_template("Items.template.py")

        found_item_keys = list(dict.keys(self.state.found_items))
        found_item_keys.sort()

        code_item_list = [ast.unparse(self.state.found_items[k]) for k in found_item_keys]
        code = ",\n".join(code_item_list)
        items_complete = template.render(items_data=code, **self.common_args)

        with open("Items.py", "w") as f:
            f.write(items_complete)

        ### REGIONS
        template = self.environment.get_template("Regions.template.py")
        
        code_region_pack_list = []

        for mode, region_map in self.state.region_maps.items():
            regions_seen_keys = list(region_map.regions_seen)
            regions_seen_keys.sort(key=lambda x: float(x.strip(string.ascii_letters)))

            code_region_list = [f'{ast.unparse(ast.Constant(k))}' for k in regions_seen_keys]
            code_region_list = ",\n".join(code_region_list)

            code_region_connections = [ast.unparse(item) for item in region_map.connections]
            code_region_connections = ",\n".join(code_region_connections)

            code_excluded_regions = ast.unparse(ast.List([ast.Constant(x) for x in self.ctx.rando_data["softLockAreas"]]))

            code_region_pack_list.append({
                "name": mode,
                "region_list": code_region_list,
                "region_connections": code_region_connections,
                "starting_region": self.ctx.rando_data["startingArea"][mode],
                "goal_region": self.ctx.rando_data["goalArea"][mode],
                "excluded_regions": code_excluded_regions
            })

        regions_complete = template.render(
                region_packs=code_region_pack_list,
                modes_string=", ".join([f'"{m}"' for m in self.ctx.rando_data["modes"]]),
                **self.common_args
        )

        with open("Regions.py", "w") as f:
            f.write(regions_complete)

        template = self.environment.get_template("Options.template.py")
        
        options_complete = template.render(
            mode_index=self.ctx.rando_data["modes"].index(self.ctx.rando_data["defaultMode"]),
            **self.common_args
        )

        with open("Options.py", "w") as f:
            f.write(options_complete)

        try:
            os.mkdir(self.data_out_dir)
        except FileExistsError:
            pass

        with open(f"{self.data_out_dir}/data.json", "w") as f:
            json.dump(self.ctx.rando_data, f, indent='\t')
