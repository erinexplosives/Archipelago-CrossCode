import typing
import ast
import string
import os
import json

import jinja2

from .ast import AstGenerator
from .context import Context, make_context_from_directory
from .emit import emit_list
from .util import GENERATED_COMMENT
from .world_builder import WorldBuilder


class FileGenerator:
    environment: jinja2.Environment
    ctx: Context
    common_args: typing.Dict[str, typing.Any]
    builder: WorldBuilder
    world_dir: str
    data_out_dir: str

    ast_generator: AstGenerator

    def __init__(self, world_dir: str):
        data_dir = os.path.join(world_dir, "data")
        data_out_dir = os.path.join(world_dir, "data", "out")
        template_dir = os.path.join(world_dir, "templates")

        self.ctx = make_context_from_directory(data_dir)
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir))
        self.world_builder = WorldBuilder(self.ctx)

        self.world_dir = world_dir
        self.data_out_dir = data_out_dir

        self.ast_generator = AstGenerator()

        self.common_args = {
            "generated_comment": GENERATED_COMMENT,
            "modes": self.ctx.rando_data["modes"],
            "default_mode": self.ctx.rando_data["defaultMode"],
        }

    def generate_files(self) -> None:
        world = self.world_builder.build()

        # LOCATIONS
        template = self.environment.get_template("Locations.template.py")

        code_locations_data = emit_list([self.ast_generator.create_ast_call_location(loc) for loc in world.locations_data])
        code_events_data =  emit_list([self.ast_generator.create_ast_call_location(loc) for loc in world.events_data])

        locations_complete = template.render(
            locations_data=code_locations_data, events_data=code_events_data, 
            needed_items=world.num_needed_items, **self.common_args)

        with open(os.path.join(self.world_dir, "Locations.py"), "w") as f:
            f.write(locations_complete)

        # ITEMS
        template = self.environment.get_template("Items.template.py")

        sorted_item_data = [(data.combo_id, data) for data in world.items_dict.values()]
        sorted_item_data.sort()

        code_item_list = [ast.unparse(self.ast_generator.create_ast_call_item(v)) for _, v in sorted_item_data]
        code = ",\n".join(code_item_list)
        items_complete = template.render(items_data=code, **self.common_args)

        with open(os.path.join(self.world_dir, "Items.py"), "w") as f:
            f.write(items_complete)

        # # REGIONS
        # template = self.environment.get_template("Regions.template.py")

        # code_region_pack_list = []

        # for mode, region_map in self.state.region_maps.items():
        #     regions_seen_keys = list(region_map.regions_seen)
        #     regions_seen_keys.sort(key=lambda x: float(
        #         x.strip(string.ascii_letters)))

        #     code_region_list = [
        #         f'{ast.unparse(ast.Constant(k))}' for k in regions_seen_keys]
        #     code_region_list = ",\n".join(code_region_list)

        #     code_region_connections = [ast.unparse(
        #         item) for item in region_map.connections]
        #     code_region_connections = ",\n".join(code_region_connections)

        #     code_excluded_regions = ast.unparse(
        #         ast.List([ast.Constant(x) for x in self.ctx.rando_data["excludedRegions"][mode]]))

        #     code_region_pack_list.append({
        #         "name": mode,
        #         "region_list": code_region_list,
        #         "region_connections": code_region_connections,
        #         "starting_region": self.ctx.rando_data["startingRegion"][mode],
        #         "goal_region": self.ctx.rando_data["goalRegion"][mode],
        #         "excluded_regions": code_excluded_regions
        #     })

        # regions_complete = template.render(
        #     region_packs=code_region_pack_list,
        #     modes_string=", ".join(
        #         [f'"{m}"' for m in self.ctx.rando_data["modes"]]),
        #     **self.common_args
        # )

        # with open("Regions.py", "w") as f:
        #     f.write(regions_complete)

        template = self.environment.get_template("OptionsGenerated.template.py")

        options_complete = template.render(
            mode_index=self.ctx.rando_data["modes"].index(
                self.ctx.rando_data["defaultMode"]),
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "OptionsGenerated.py"), "w") as f:
            f.write(options_complete)

        try:
            os.mkdir(self.data_out_dir)
        except FileExistsError:
            pass

        with open(os.path.join(self.data_out_dir, "data.json"), "w") as f:
            json.dump(self.ctx.rando_data, f, indent='\t')
