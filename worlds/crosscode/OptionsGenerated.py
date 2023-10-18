from Options import Choice

class LogicMode(Choice):
    """
    Logic mode; in other words, how is the player allowed to access items.
    [Linear] Progression follows the game's linear path, though sequence breaks are allowed and inevitably will still occur. Makes for a longer, more BK-heavy playthrough with fewer options at each point.
    [Open] (Default) Progression is based only on whether it is possible to reach area given the current list of received items.
    """
    display_name = "Logic Mode"
    option_linear = 0
    option_open = 1
    
    default = 1