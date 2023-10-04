import typing
import ast
import os
import json

import jinja2

from .ast import AstGenerator
from .context import Context, make_context_from_directory
from .emit import emit_list
from .util import GENERATED_COMMENT
from .lists import ListInfo


class FileGenerator:
    environment: jinja2.Environment
    ctx: Context
    common_args: typing.Dict[str, typing.Any]
    lists: ListInfo
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
        self.lists = ListInfo(self.ctx)

        self.world_dir = world_dir
        self.data_out_dir = data_out_dir

        self.ast_generator = AstGenerator()

        self.common_args = {
            "generated_comment": GENERATED_COMMENT,
            "modes": self.ctx.rando_data["modes"],
            "default_mode": self.ctx.rando_data["defaultMode"],
        }

    def generate_files(self) -> None:
        # LOCATIONS
        template = self.environment.get_template("Locations.template.py")

        code_locations_data = emit_list([self.ast_generator.create_ast_call_location(loc) for loc in self.lists.locations_data.values()])
        code_events_data =  emit_list([self.ast_generator.create_ast_call_location(loc) for loc in self.lists.events_data.values()])

        locations_complete = template.render(locations_data=code_locations_data, events_data=code_events_data, **self.common_args)

        with open(os.path.join(self.world_dir, "Locations.py"), "w") as f:
            f.write(locations_complete)

        # ITEMS
        template = self.environment.get_template("Items.template.py")

        sorted_item_data = [(data.combo_id, data) for data in self.lists.items_dict.values()]
        sorted_item_data.sort()

        code_item_list = [ast.unparse(self.ast_generator.create_ast_call_item(v)) for _, v in sorted_item_data]
        code = ",\n".join(code_item_list)
        items_complete = template.render(items_data=code, **self.common_args)

        with open(os.path.join(self.world_dir, "Items.py"), "w") as f:
            f.write(items_complete)

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
