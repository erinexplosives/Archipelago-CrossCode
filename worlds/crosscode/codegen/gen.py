import typing
import ast
import os
import json

import jinja2

from .ast import AstGenerator
from .context import Context, make_context_from_directory
from .emit import emit_dict, emit_list
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
        self.lists.build()

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

        sorted_single_item_data = [(value.item_id, key, value) for key, value in self.lists.single_items_dict.items()]
        sorted_single_item_data.sort()

        code_single_item_dict = emit_dict([(ast.Constant(key), self.ast_generator.create_ast_call_single_item(value)) for _, key, value in sorted_single_item_data])

        sorted_item_data = [(value.combo_id, key, value) for key, value in self.lists.items_dict.items()]
        sorted_item_data.sort()

        item_dict_items = []
        for _, key, value in sorted_item_data:
            key = ast.Tuple(elts=[ast.Constant(x) for x in key])
            ast.fix_missing_locations(key)
            value = self.ast_generator.create_ast_call_item(value)
            item_dict_items.append((key, value))

        code_item_dict = emit_dict(item_dict_items)

        items_complete = template.render(
            single_items_dict=code_single_item_dict,
            items_dict=code_item_dict,
            num_items=self.ctx.num_items,
            **self.common_args
        )

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
