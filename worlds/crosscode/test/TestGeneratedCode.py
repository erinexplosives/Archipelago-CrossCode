from functools import reduce
from test.TestBase import WorldTestBase
from . import CrossCodeTestBase
from ..Items import items_data, items_dict
from ..Locations import locations_data, events_data, needed_items
from ..Regions import modes, region_packs

class TestLocationAttributes(CrossCodeTestBase):
    def test_regions_exist(self):
        for mode in modes:
            all_regions = set()
            all_regions |= set(region_packs[mode].region_list)
            all_regions |= set(region_packs[mode].excluded_regions)
            for data in locations_data:
                assert(data.region[mode] in all_regions)

class TestConditionsValid(CrossCodeTestBase):
    auto_construct = False
    locations_dict = {location.name: location for location in [*locations_data, *events_data]}

    def test_item_conditions_on_locations_exist(self):
        for data in locations_data:
            for item, amount in data.cond.items:
                item_name = item if amount == 1 else f"{item} x{amount}"
                assert(item_name in items_dict)

    def test_location_conditions_on_locations_exist(self):
        for data in locations_data:
            for location in data.cond.locations:
                assert(location in self.locations_dict)

    def test_region_conditions_on_locations_exist(self):
        for data in locations_data:
            for mode, regions in data.cond.regions.items():
                for region in regions:
                    assert(region in region_packs[mode].region_list)

    def test_item_conditions_on_regions_exist(self):
        for mode in modes:
            for connection in region_packs[mode].region_connections:
                for item, _ in connection.cond.items:
                    assert(item in items_dict)

    def test_location_conditions_on_regions_exist(self):
        for mode in modes:
            for connection in region_packs[mode].region_connections:
                for location in connection.cond.locations:
                    assert(location in self.locations_dict)

    def test_region_conditions_on_regions_exist(self):
        for mode in modes:
            for connection in region_packs[mode].region_connections:
                if mode not in connection.cond.regions:
                    continue
                for region in connection.cond.regions[mode]:
                    assert(region in region_packs[mode].region_list)


class TestItemQuantities(CrossCodeTestBase):
    auto_construct = False

    def test_item_quantities_equal_to_locations(self):
        for mode in modes:
            number_of_locations = 0
            for data in locations_data:
                if mode in data.region and data.region[mode] not in region_packs[mode].excluded_regions:
                    number_of_locations += 1

            items_from_locations = 0
            for item in items_data:
                if mode in item.quantity:
                    items_from_locations += item.quantity[mode]

            items_to_generate = needed_items[mode]

            total_items = items_from_locations + items_to_generate
            assert(total_items == number_of_locations)
