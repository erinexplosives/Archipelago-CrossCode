# WARNING: THIS FILE HAS BEEN GENERATED!
# Modifications to this file will not be kept.
# If you need to change something here, check out codegen.py and the templates directory.


import typing
from BaseClasses import Region, Entrance

from .Locations import Condition

class RegionConnection(typing.NamedTuple):
    region_from: str
    region_to: str
    cond: Condition

class RegionsData(typing.NamedTuple):
    starting_region: str
    goal_region: str
    excluded_regions: typing.List[str]
    region_list: typing.List[str]
    region_connections: typing.List[RegionConnection]

modes = [ "linear", "open" ]
default_mode = "open"

region_packs: typing.Dict[str, RegionsData] = {
    "linear": RegionsData(
        starting_region = "2",
        goal_region = "32",
        excluded_regions = ['linear', 'open'],
        region_list = [
            '2',
            '3',
            '3.1',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
            '11',
            '12',
            '13',
            '14',
            '15',
            '16',
            '17',
            '17.5',
            '18',
            '19',
            '20',
            '21',
            '22',
            '23',
            '24',
            '25',
            '26',
            '27',
            '28',
            '29',
            '30',
            '31',
            '32',
            '33'
        ],
        region_connections = [
            RegionConnection(region_from='2', region_to='3', cond=Condition(items=[('Green Leaf Shade', 1)])),
            RegionConnection(region_from='3', region_to='4', cond=Condition(items=[('Mine Pass', 1), ('Guild Pass', 1)])),
            RegionConnection(region_from='3', region_to='3.1', cond=Condition(items=[('Mine Pass', 1)])),
            RegionConnection(region_from='4', region_to='5', cond=Condition(items=[('Mine Key', 1)])),
            RegionConnection(region_from='5', region_to='6', cond=Condition(items=[('Mine Key', 2)])),
            RegionConnection(region_from='6', region_to='7', cond=Condition(items=[('Mine Key', 3)])),
            RegionConnection(region_from='7', region_to='8', cond=Condition(items=[('Mine Key', 6)])),
            RegionConnection(region_from='7', region_to='9', cond=Condition(items=[("Thief's Key", 1), ('Heat', 1)])),
            RegionConnection(region_from='9', region_to='10', cond=Condition(items=[('Mine Key', 10)])),
            RegionConnection(region_from='10', region_to='11', cond=Condition(items=[('Mine Master Key', 1), ('Blue Ice Shade', 1)])),
            RegionConnection(region_from='11', region_to='12', cond=Condition(items=[('Maroon Cave Pass', 1)])),
            RegionConnection(region_from='12', region_to='13', cond=Condition(items=[('Yellow Sand Shade', 1), ('Heat', 1)])),
            RegionConnection(region_from='13', region_to='14', cond=Condition(items=[("Faj'ro Key", 1)])),
            RegionConnection(region_from='14', region_to='15', cond=Condition(items=[("Faj'ro Key", 3)])),
            RegionConnection(region_from='15', region_to='16', cond=Condition(items=[("Faj'ro Key", 4)])),
            RegionConnection(region_from='16', region_to='17', cond=Condition(items=[('Cold', 1)])),
            RegionConnection(region_from='17', region_to='17.5', cond=Condition(items=[('White Key', 1)])),
            RegionConnection(region_from='17.5', region_to='18', cond=Condition(items=[("Faj'ro Key", 9)])),
            RegionConnection(region_from='17.5', region_to='19', cond=Condition(items=[("Faj'ro Master Key", 1)])),
            RegionConnection(region_from='19', region_to='20', cond=Condition(items=[('Red Flame Shade', 1)])),
            RegionConnection(region_from='20', region_to='21', cond=Condition(items=[('Green Seed Shade', 1)])),
            RegionConnection(region_from='21', region_to='23', cond=Condition()),
            RegionConnection(region_from='21', region_to='24', cond=Condition(items=[('Pond Slums Pass', 1)])),
            RegionConnection(region_from='23', region_to='25', cond=Condition(items=[("Zir'vitar Key", 2)])),
            RegionConnection(region_from='23', region_to='26', cond=Condition(items=[("So'najiz Key", 4)])),
            RegionConnection(region_from='26', region_to='27', cond=Condition(items=[('Radiant Key', 1), ("So'najiz Key", 5)])),
            RegionConnection(region_from='23', region_to='28', cond=Condition(items=[('Azure Drop Shade', 1), ('Purple Bolt Shade', 1), ('Wave', 1), ('Shock', 1)])),
            RegionConnection(region_from='28', region_to='29', cond=Condition(items=[("Krys'kajo Key", 2)])),
            RegionConnection(region_from='28', region_to='30', cond=Condition(items=[('Kajo Master Key', 1)])),
            RegionConnection(region_from='30', region_to='31', cond=Condition(items=[('Star Shade', 1)])),
            RegionConnection(region_from='31', region_to='32', cond=Condition(items=[('Old Dojo Key', 1)])),
            RegionConnection(region_from='32', region_to='33', cond=Condition(items=[('Meteor Shade', 1)])),
            RegionConnection(region_from='31', region_to='22', cond=Condition())
        ]
    ),
    "open": RegionsData(
        starting_region = "open2",
        goal_region = "open19",
        excluded_regions = ['linear', 'open'],
        region_list = [
            'open2',
            'open3',
            'open3.1',
            'open4.1',
            'open4.2',
            'open4.3',
            'open4.4',
            'open4.5',
            'open4.6',
            'open4.7',
            'open4.8',
            'open5',
            'open6',
            'open7.1',
            'open7.2',
            'open7.3',
            'open7.4',
            'open7.5',
            'open7.6',
            'open7.7',
            'open7.8',
            'open8',
            'open9',
            'open9.1',
            'open10',
            'open11',
            'open12',
            'open13.1',
            'open13.2',
            'open14.1',
            'open14.2',
            'open14.3',
            'open15.1',
            'open15.2',
            'open15.3',
            'open16',
            'open16.1',
            'open17',
            'open18',
            'open19',
            'open20'
        ],
        region_connections = [
            RegionConnection(region_from='open2', region_to='open3', cond=Condition(items=[('Green Leaf Shade', 1)])),
            RegionConnection(region_from='open3', region_to='open4.1', cond=Condition(items=[('Mine Pass', 1)])),
            RegionConnection(region_from='open3', region_to='open3.1', cond=Condition(items=[('Mine Pass', 1)])),
            RegionConnection(region_from='open4.1', region_to='open4.2', cond=Condition(items=[('Mine Key', 1)])),
            RegionConnection(region_from='open4.2', region_to='open4.3', cond=Condition(items=[('Mine Key', 2)])),
            RegionConnection(region_from='open4.3', region_to='open4.4', cond=Condition(items=[('Mine Key', 3)])),
            RegionConnection(region_from='open4.4', region_to='open4.5', cond=Condition(items=[('Mine Key', 6)])),
            RegionConnection(region_from='open4.3', region_to='open4.6', cond=Condition(items=[('Heat', 1)])),
            RegionConnection(region_from='open4.6', region_to='open4.7', cond=Condition(items=[('Mine Key', 10)])),
            RegionConnection(region_from='open4.1', region_to='open4.8', cond=Condition(items=[('Mine Master Key', 1)])),
            RegionConnection(region_from='open3', region_to='open5', cond=Condition(items=[('Blue Ice Shade', 1)])),
            RegionConnection(region_from='open5', region_to='open6', cond=Condition(items=[('Maroon Cave Pass', 1)])),
            RegionConnection(region_from='open5', region_to='open7.1', cond=Condition(items=[('Yellow Sand Shade', 1), ('Heat', 1)])),
            RegionConnection(region_from='open7.1', region_to='open7.2', cond=Condition(items=[("Faj'ro Key", 1)])),
            RegionConnection(region_from='open7.2', region_to='open7.3', cond=Condition(items=[("Faj'ro Key", 3)])),
            RegionConnection(region_from='open7.3', region_to='open7.4', cond=Condition(items=[("Faj'ro Key", 4)])),
            RegionConnection(region_from='open7.4', region_to='open7.5', cond=Condition(items=[('Cold', 1)])),
            RegionConnection(region_from='open7.5', region_to='open7.6', cond=Condition(items=[('White Key', 1)])),
            RegionConnection(region_from='open7.6', region_to='open7.7', cond=Condition(items=[("Faj'ro Key", 9)])),
            RegionConnection(region_from='open7.6', region_to='open7.8', cond=Condition(items=[("Faj'ro Master Key", 1)])),
            RegionConnection(region_from='open2', region_to='open8', cond=Condition(items=[('Red Flame Shade', 1)])),
            RegionConnection(region_from='open2', region_to='open9', cond=Condition(items=[('Red Flame Shade', 1)])),
            RegionConnection(region_from='open2', region_to='open20', cond=Condition(items=[('Meteor Shade', 1)])),
            RegionConnection(region_from='open9', region_to='open9.1', cond=Condition(items=[('Green Seed Shade', 1)])),
            RegionConnection(region_from='open9', region_to='open10', cond=Condition(items=[('Green Seed Shade', 1)])),
            RegionConnection(region_from='open10', region_to='open11', cond=Condition(items=[('Pond Slums Pass', 1)])),
            RegionConnection(region_from='open10', region_to='open12', cond=Condition(items=[('Heat', 1), ('Cold', 1)])),
            RegionConnection(region_from='open12', region_to='open13.1', cond=Condition(items=[("Zir'vitar Key", 2)])),
            RegionConnection(region_from='open13.1', region_to='open13.2', cond=Condition(items=[('Wave', 1)])),
            RegionConnection(region_from='open12', region_to='open14.1', cond=Condition(items=[("So'najiz Key", 4)])),
            RegionConnection(region_from='open14.1', region_to='open14.2', cond=Condition(items=[("So'najiz Key", 5)])),
            RegionConnection(region_from='open14.2', region_to='open14.3', cond=Condition(items=[('Shock', 1)])),
            RegionConnection(region_from='open12', region_to='open15.1', cond=Condition(items=[('Azure Drop Shade', 1), ('Purple Bolt Shade', 1), ('Wave', 1), ('Shock', 1)])),
            RegionConnection(region_from='open15.1', region_to='open15.2', cond=Condition(items=[("Krys'kajo Key", 2)])),
            RegionConnection(region_from='open15.2', region_to='open15.3', cond=Condition(items=[('Kajo Master Key', 1)])),
            RegionConnection(region_from='open9', region_to='open16', cond=Condition(items=[('Star Shade', 1)])),
            RegionConnection(region_from='open16', region_to='open17', cond=Condition(items=[('Old Dojo Key', 1)])),
            RegionConnection(region_from='open16', region_to='open16.1', cond=Condition(items=[('Meteor Shade', 1), ('Shock', 1)])),
            RegionConnection(region_from='open16', region_to='open18', cond=Condition()),
            RegionConnection(region_from='open16.1', region_to='open19', cond=Condition(cutscenes=['Temple Mine Shade Statue', "Faj'ro Shade Statue", "Zir'vitar Shade Statue", "So'najiz Mine Shade Statue"], items=[('Heat', 1), ('Cold', 1), ('Shock', 1), ('Wave', 1)]))
        ]
    ),
    
}