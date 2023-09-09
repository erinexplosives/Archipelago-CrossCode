# This is the entry point of the codegen module, a script that runs the code generation, producing:
# - `Locations.py' from `Locations.template.py'
# - `Items.py' from `Items.template.py'
#
# This process requires a few data files.
# Put the following files in the `data' directory:
# - `assets' from your CrossCode installation
# - `data-in.json' from the CCMultiworldRandomizer mod
#
# This script also produces a copy of `data-in.json` with additional metadata for the mod, called `data.json`
# Copy `data/out/data.json` into `CCMultiworldRandomizer/data`
#
# To run it for yourself, navigate to the directory containing `codegen` and run `python -m codegen`

from .gen import FileGenerator

fg = FileGenerator("data", "data/out")

fg.generate_files()
