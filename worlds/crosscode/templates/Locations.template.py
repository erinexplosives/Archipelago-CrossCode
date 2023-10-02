{{generated_comment | indent("# ", True)}}

from .types.Locations import LocationData
from .types.Condition import *

needed_items = {{needed_items}}

locations_data = {{locations_data}}

locations_dict = { location.name: location for location in locations_data }

events_data = {{events_data}}
