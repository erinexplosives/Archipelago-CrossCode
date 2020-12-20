from test.inverted_minor_glitches.TestInvertedMinor import TestInvertedMinor


class TestEntrances(TestInvertedMinor):

    def testDungeonEntrances(self):
        self.run_entrance_tests([
            ["Hyrule Castle Entrance (South)", False, []],
            ["Hyrule Castle Entrance (South)", False, [], ["Beat Agahnim 1", "Moon Pearl"]],
            ["Hyrule Castle Entrance (South)", False, [], ["Beat Agahnim 1", "Progressive Glove"]],
            ["Hyrule Castle Entrance (South)", False, ["Progressive Glove"], ["Beat Agahnim 1", "Hammer", "Progressive Glove"]],
            ["Hyrule Castle Entrance (South)", True, ["Beat Agahnim 1"]],
            ["Hyrule Castle Entrance (South)", True, ["Moon Pearl", "Hammer", "Progressive Glove"]],
            ["Hyrule Castle Entrance (South)", True, ["Moon Pearl", "Progressive Glove", "Progressive Glove"]],

            ["Eastern Palace", False, []],
            ["Eastern Palace", False, [], ["Beat Agahnim 1", "Moon Pearl"]],
            ["Eastern Palace", False, [], ["Beat Agahnim 1", "Progressive Glove"]],
            ["Eastern Palace", False, ["Progressive Glove"], ["Beat Agahnim 1", "Hammer", "Progressive Glove"]],
            ["Eastern Palace", True, ["Beat Agahnim 1"]],
            ["Eastern Palace", True, ["Moon Pearl", "Hammer", "Progressive Glove"]],
            ["Eastern Palace", True, ["Moon Pearl", "Progressive Glove", "Progressive Glove"]],

            ["Desert Palace Entrance (South)", False, []],
            ["Desert Palace Entrance (South)", False, [], ["Book of Mudora"]],
            ["Desert Palace Entrance (South)", False, [], ["Beat Agahnim 1", "Moon Pearl"]],
            ["Desert Palace Entrance (South)", False, [], ["Beat Agahnim 1", "Progressive Glove"]],
            ["Desert Palace Entrance (South)", False, ["Progressive Glove"], ["Beat Agahnim 1", "Hammer", "Progressive Glove"]],
            ["Desert Palace Entrance (South)", True, ["Book of Mudora", "Beat Agahnim 1"]],
            ["Desert Palace Entrance (South)", True, ["Book of Mudora", "Moon Pearl", "Hammer", "Progressive Glove"]],
            ["Desert Palace Entrance (South)", True, ["Book of Mudora", "Moon Pearl", "Progressive Glove", "Progressive Glove"]],
            ["Desert Palace Entrance (North)", False, []],
            ["Desert Palace Entrance (North)", False, [], ["Book of Mudora"]],
            ["Desert Palace Entrance (North)", False, [], ["Progressive Glove"]],
            ["Desert Palace Entrance (North)", False, [], ["Moon Pearl"]],
            ["Desert Palace Entrance (North)", False, ["Progressive Glove"], ["Beat Agahnim 1", "Hammer", "Progressive Glove"]],
            ["Desert Palace Entrance (North)", True, ["Moon Pearl", "Book of Mudora", "Progressive Glove", "Hammer"]],
            ["Desert Palace Entrance (North)", True, ["Moon Pearl", "Book of Mudora", "Progressive Glove", "Progressive Glove"]],
            ["Desert Palace Entrance (North)", True, ["Moon Pearl", "Book of Mudora", "Progressive Glove", "Beat Agahnim 1"]],

            ["Tower of Hera", False, []],
            ["Tower of Hera", False, [], ["Moon Pearl"]],
            ["Tower of Hera", False, [], ["Hammer"]],
            ["Tower of Hera", False, ["Progressive Glove"], ["Hookshot", "Progressive Glove"]],
            ["Tower of Hera", False, [], ["Flute", "Lamp"]],
            ["Tower of Hera", False, [], ["Flute", "Progressive Glove"]],
            ["Tower of Hera", True, ["Moon Pearl", "Hammer", "Progressive Glove", "Progressive Glove", "Lamp"]],
            ["Tower of Hera", True, ["Moon Pearl", "Hammer", "Hookshot", "Progressive Glove", "Lamp"]],
            ["Tower of Hera", True, ["Moon Pearl", "Hammer", "Hookshot", "Progressive Glove", "Flute"]],
            ["Tower of Hera", True, ["Moon Pearl", "Hammer", "Beat Agahnim 1", "Flute", "Hookshot"]],

            ["Inverted Agahnims Tower", False, []],
            ["Inverted Agahnims Tower", False, [], ["Flute", "Lamp"]],
            ["Inverted Agahnims Tower", False, [], ["Flute", "Progressive Glove"]],
            ["Inverted Agahnims Tower", False, [], ["Moon Pearl", "Lamp"]],
            ["Inverted Agahnims Tower", False, [], ["Moon Pearl", "Progressive Glove"]],
            ["Inverted Agahnims Tower", True, ["Lamp", "Progressive Glove"]],
            ["Inverted Agahnims Tower", True, ["Flute", "Beat Agahnim 1", "Moon Pearl"]],
            ["Inverted Agahnims Tower", True, ["Flute", "Progressive Glove", "Progressive Glove", "Moon Pearl"]],
            ["Inverted Agahnims Tower", True, ["Flute", "Progressive Glove", "Hammer", "Moon Pearl"]],

            ["Palace of Darkness", True, []],

            ["Swamp Palace", True, []],

            ["Thieves Town", True, []],

            ["Skull Woods First Section Door", True, []],

            ["Skull Woods Final Section", False, []],
            ["Skull Woods Final Section", False, [], ["Fire Rod"]],
            ["Skull Woods Final Section", True, ["Fire Rod"]],

            ["Ice Palace", True, []],

            ["Misery Mire", False, []],
            ["Misery Mire", False, [], ["Flute", "Magic Mirror"]],
            ["Misery Mire", False, [], ["Moon Pearl", "Magic Mirror"]],
            ["Misery Mire", False, [], ["Ether"]],
            ["Misery Mire", False, [], ["Progressive Sword"]],
            ["Misery Mire", True, ["Progressive Sword", "Ether", "Beat Agahnim 1", "Magic Mirror"]],
            ["Misery Mire", True, ["Progressive Sword", "Ether", "Beat Agahnim 1", "Moon Pearl", "Flute"]],
            ["Misery Mire", True, ["Progressive Sword", "Ether", "Moon Pearl", "Hammer", "Progressive Glove", "Magic Mirror"]],
            ["Misery Mire", True, ["Progressive Sword", "Ether", "Moon Pearl", "Hammer", "Progressive Glove", "Flute"]],
            ["Misery Mire", True, ["Progressive Sword", "Ether", "Moon Pearl", "Progressive Glove", "Progressive Glove", "Magic Mirror"]],
            ["Misery Mire", True, ["Progressive Sword", "Ether", "Moon Pearl", "Progressive Glove", "Progressive Glove", "Flute"]],

            ["Turtle Rock", False, []],
            ["Turtle Rock", False, [], ["Quake"]],
            ["Turtle Rock", False, [], ["Progressive Sword"]],
            ["Turtle Rock", False, [], ["Lamp", "Flute"]],
            ["Turtle Rock", False, [], ["Progressive Glove", "Flute"]],
            ["Turtle Rock", True, ["Quake", "Progressive Sword", "Progressive Glove", "Lamp"]],
            ["Turtle Rock", True, ["Quake", "Progressive Sword", "Progressive Glove", "Progressive Glove", "Moon Pearl", "Flute"]],
            ["Turtle Rock", True, ["Quake", "Progressive Sword", "Progressive Glove", "Hammer", "Moon Pearl", "Flute"]],
            ["Turtle Rock", True, ["Quake", "Progressive Sword", "Beat Agahnim 1", "Moon Pearl", "Flute"]],

            ["Inverted Ganons Tower", False, []],
            ["Inverted Ganons Tower", False, [], ["Crystal 1"]],
            ["Inverted Ganons Tower", False, [], ["Crystal 2"]],
            ["Inverted Ganons Tower", False, [], ["Crystal 3"]],
            ["Inverted Ganons Tower", False, [], ["Crystal 4"]],
            ["Inverted Ganons Tower", False, [], ["Crystal 5"]],
            ["Inverted Ganons Tower", False, [], ["Crystal 6"]],
            ["Inverted Ganons Tower", False, [], ["Crystal 7"]],
            ["Inverted Ganons Tower", True, ["Beat Agahnim 1", "Crystal 1", "Crystal 2", "Crystal 3", "Crystal 4", "Crystal 5", "Crystal 6", "Crystal 7"]],
            ["Inverted Ganons Tower", True, ["Moon Pearl", "Progressive Glove", "Progressive Glove", "Crystal 1", "Crystal 2", "Crystal 3", "Crystal 4", "Crystal 5", "Crystal 6", "Crystal 7"]],
        ])