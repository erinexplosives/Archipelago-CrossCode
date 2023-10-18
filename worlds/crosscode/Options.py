from Options import AssembleOptions, Choice, DefaultOnToggle, Toggle
import typing

class VTShadeLock(DefaultOnToggle):
    """
    If enabled, adds a locked gate before the final dungeon that only opens when all four shades are collected and all four bosses are beaten.
    """
    display_name = "Vermillion Tower Shade Lock"

class QuestRando(Toggle):
    """
    If enabled, all quests will be randomized along with chests and cutscene locations.
    """
    display_name = "Quest Randomization"

class VTSkip(DefaultOnToggle):
    """
    If enabled, Vermillion Tower will not need to be completed; instead, the player will skip through it to the final boss.
    """
    display_name = "Skip Vermillion Tower"

class StartWithGreenLeafShade(DefaultOnToggle):
    """
    If enabled, the player will start with the green leaf shade, unlocking Autumn's Fall. This makes the early game far more open.
    """
    display_name = "Start with Green Leaf Shade"

class StartWithChestDetector(DefaultOnToggle):
    """
    If enabled, the player will start with the chest detector item, which will notify them of the chests in the room.
    """
    display_name = "Start with Chest Detector"

class Reachability(Choice):
    option_own_world = 0
    option_different_world = 1
    option_any_world = 2

    default = 2

class ShadeLocations(Reachability):
    """
    Where shades will appear.
    """

    display_name = "Shade Locations"

class ElementLocations(Reachability):
    """
    Where elements will appear.
    """

    display_name = "Element Locations"

crosscode_options_pairs = [
    ("vt_shade_lock", VTShadeLock),
    ("quest_rando", QuestRando),
    ("vt_skip", VTSkip),
    ("start_with_green_leaf_shade", StartWithGreenLeafShade),
    ("start_with_chest_detector", StartWithChestDetector),
    ("shade_locations", ShadeLocations),
    ("element_locations", ElementLocations),
]

addon_options = ["vt_shade_lock", "quest_rando"]

try:
    from .OptionsGenerated import LogicMode
    crosscode_options_pairs.insert(0, ("logic_mode", LogicMode))
except ImportError:
    pass

crosscode_options: typing.Dict[str, AssembleOptions] = dict(crosscode_options_pairs)
