import typing
from BaseClasses import Region, Entrance

class RegionConnection(typing.NamedTuple):
    region_from: str
    region_to: str
    cond_elements: typing.List[str]
    cond_items: typing.List[typing.Tuple[str, int]]

region_list: typing.List[str] = [
	'2',
	'3',
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
]

region_connections: typing.List[RegionConnection] = [
	RegionConnection(region_from='2', region_to='3', cond_elements=[], cond_items=[('Green Leaf Shade', 1)]),
	RegionConnection(region_from='3', region_to='4', cond_elements=[], cond_items=[('Mine Pass', 1), ('Guild Pass', 1)]),
	RegionConnection(region_from='4', region_to='5', cond_elements=[], cond_items=[('Mine Key', 1)]),
	RegionConnection(region_from='5', region_to='6', cond_elements=[], cond_items=[('Mine Key', 2)]),
	RegionConnection(region_from='6', region_to='7', cond_elements=[], cond_items=[('Mine Key', 3)]),
	RegionConnection(region_from='7', region_to='8', cond_elements=[], cond_items=[('Mine Key', 6)]),
	RegionConnection(region_from='7', region_to='9', cond_elements=['Heat'], cond_items=[("Thief's Key", 1)]),
	RegionConnection(region_from='9', region_to='10', cond_elements=[], cond_items=[('Mine Key', 10)]),
	RegionConnection(region_from='10', region_to='11', cond_elements=[], cond_items=[('Mine Master Key', 1), ('Blue Ice Shade', 1)]),
	RegionConnection(region_from='11', region_to='12', cond_elements=[], cond_items=[('Maroon Cave Pass', 1)]),
	RegionConnection(region_from='12', region_to='13', cond_elements=['Heat'], cond_items=[('Yellow Sand Shade', 1)]),
	RegionConnection(region_from='13', region_to='14', cond_elements=[], cond_items=[("Faj'ro Key", 1)]),
	RegionConnection(region_from='14', region_to='15', cond_elements=[], cond_items=[("Faj'ro Key", 3)]),
	RegionConnection(region_from='15', region_to='16', cond_elements=[], cond_items=[("Faj'ro Key", 4)]),
	RegionConnection(region_from='16', region_to='17', cond_elements=['Cold'], cond_items=[]),
	RegionConnection(region_from='17', region_to='17.5', cond_elements=[], cond_items=[('White Key', 1)]),
	RegionConnection(region_from='17.5', region_to='18', cond_elements=[], cond_items=[("Faj'ro Key", 9)]),
	RegionConnection(region_from='17.5', region_to='19', cond_elements=[], cond_items=[("Faj'ro Master Key", 1)]),
	RegionConnection(region_from='19', region_to='20', cond_elements=[], cond_items=[('Red Flame Shade', 1)]),
	RegionConnection(region_from='20', region_to='21', cond_elements=[], cond_items=[('Green Seed Shade', 1)]),
	RegionConnection(region_from='21', region_to='23', cond_elements=[], cond_items=[]),
	RegionConnection(region_from='21', region_to='24', cond_elements=[], cond_items=[('Pond Slums Pass', 1)]),
	RegionConnection(region_from='23', region_to='25', cond_elements=[], cond_items=[("Zir'vitar Key", 2)]),
	RegionConnection(region_from='23', region_to='26', cond_elements=[], cond_items=[("So'najiz Key", 4)]),
	RegionConnection(region_from='26', region_to='27', cond_elements=[], cond_items=[('Radiant Key', 1), ("So'najiz Key", 5)]),
	RegionConnection(region_from='23', region_to='28', cond_elements=['Wave', 'Shock'], cond_items=[('Azure Drop Shade', 1), ('Purple Bolt Shade', 1)]),
	RegionConnection(region_from='28', region_to='29', cond_elements=[], cond_items=[("Krys'kajo Key", 2)]),
	RegionConnection(region_from='28', region_to='30', cond_elements=[], cond_items=[('Kajo Master Key', 1)]),
	RegionConnection(region_from='30', region_to='31', cond_elements=[], cond_items=[('Star Shade', 1)]),
	RegionConnection(region_from='31', region_to='32', cond_elements=[], cond_items=[('Old Dojo Key', 1)]),
	RegionConnection(region_from='32', region_to='33', cond_elements=[], cond_items=[('Meteor Shade', 1)])
]