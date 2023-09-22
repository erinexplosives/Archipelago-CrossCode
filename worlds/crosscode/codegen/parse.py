import string
import typing

from BaseClasses import ItemClassification

from .context import Context
from .util import BASE_ID, RESERVED_ITEM_IDS, get_item_classification

from ..types.Items import ItemData
from ..types.Locations import Condition, LocationData, empty_condition
from ..types.Regions import RegionConnection, RegionsData

class JsonParserError(Exception):
    subject: typing.Any
    problem_item: typing.Any
    message: str

    def __init__(self, subject: typing.Any, problem_item: typing.Any, kind: str, message: str):
        self.subject = subject
        self.problem_item = problem_item
        self.message = f"Error parsing {kind}: {message}"
        super().__init__(subject, problem_item, message)

class JsonParser:
    ctx: Context

    def __init__(self, ctx: Context):
        self.ctx = ctx

    def parse_condition(self, raw: list[typing.Any]) -> typing.Optional[Condition]:
        result: Condition = empty_condition()

        for cond in raw:
            if not isinstance(cond, list):
                raise JsonParserError(raw, cond, "condition", "condition not a list")
            
            num_args = len(cond) - 1
            if cond[0] == "item":
                if num_args == 1:
                    result.items.append((cond[1], 1))
                elif num_args == 2:
                    result.items.append((cond[1], cond[2]))
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "item condition",
                        f"expected 1 or 2 argument, not {num_args}"
                    )

            elif cond[0] == "quest":
                if num_args == 1:
                    result.quests.append(cond[1])
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "quest condition",
                        f"expected 1 argument, not {num_args}"
                    )

            elif cond[0] in ["cutscene", "location"]:
                if num_args == 1:
                    result.locations.append(cond[1])
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "location condition",
                        f"expected 1 argument, not {num_args}"
                    )
            elif cond[0] == "region":
                if num_args == 2:
                    mode, region = cond[1:]
                    if mode not in result.regions:
                        result.regions[mode] = []
                    result.regions[mode].append(region)
                else:
                    raise JsonParserError(
                        raw,
                        cond,
                        "region condition",
                        f"expected 2 arguments, not {num_args}"
                    )
            else:
                raise JsonParserError(raw, cond, "condition", f"unknown type {cond[0]}")

        # Return None if there are no conditions
        return result if not result.is_empty() else None

    def parse_location(self, name, raw: dict[str, typing.Any], code: typing.Optional[int]) -> LocationData:
        region = {}
        if "region" in raw:
            region = raw["region"]

            if not isinstance(region, dict):
                raise JsonParserError(raw, raw["region"], "location", "region must be a dict")

            for region_name in region.values():
                if not isinstance(region_name, str):
                    raise JsonParserError(raw, region_name, "location", "region name must be a string")

        clearance = "Default"
        if "clearance" in raw:
            clearance = raw["clearance"]
            if not isinstance(clearance, str):
                raise JsonParserError(raw, clearance, "location", "clearance must be a string")

        condition = None
        if "condition" in raw:
            condition = self.parse_condition(raw["condition"])

        return LocationData(name, code, region, condition, clearance)

    def parse_item(self, raw: list[typing.Any]) -> ItemData:
        name = ""
        amount = 0

        if len(raw) == 1:
            name = raw[0]
            amount = 1
        elif len(raw) == 2:
            name = raw[0]
            amount = raw[1]
        else:
            raise JsonParserError(raw, raw, "item reward", "expected one or two elements")

        if name not in self.ctx.rando_data["items"]:
            raise JsonParserError(raw, name, "item reward", "item does not exist in randomizer data")
        item_overrides = self.ctx.rando_data["items"][name]
        item_id = item_overrides["id"]

        db_entry = self.ctx.item_data[item_id]

        combo_id = BASE_ID + RESERVED_ITEM_IDS + \
            self.ctx.num_items * (amount - 1) + item_id

        cls = get_item_classification(db_entry)

        if "classification" in item_overrides:
            cls_str = item_overrides["classification"]
            if not hasattr(ItemClassification, cls_str):
                raise JsonParserError(item_overrides, cls_str, "item reward", "invalid classification")
            cls = getattr(ItemClassification, cls_str)

        return ItemData(
            name=name,
            item_id=item_overrides["id"],
            amount=amount,
            combo_id=combo_id,
            classification=cls,
            quantity={}
        )

    def parse_element_item(self, raw: list[typing.Any]) -> ItemData:
        el = ""
        combo_id = BASE_ID

        if len(raw) == 1:
            el = raw[0]
        else:
            raise JsonParserError(raw, raw, "element reward", "expected one string")

        try:
            idx = ["Heat", "Cold", "Shock", "Wave"].index(el)
            combo_id += idx
        except:
            raise RuntimeError("Error adding element: {el} not an element")

        return ItemData(
            name=el,
            item_id=0,
            amount=1,
            combo_id=combo_id,
            classification=ItemClassification.progression,
            quantity={}
        )

    def parse_reward(self, raw: list[typing.Any]) -> ItemData:
        kind, *info = raw

        if kind == "item":
            return self.parse_item(info)
        elif kind == "element":
            return self.parse_element_item(info)
        else:
            raise RuntimeError(f"Error parsing reward {raw}: unrecognized type")

    def parse_region_connection(self, raw: dict[str, typing.Any]) -> RegionConnection:
        if "from" not in raw:
            raise JsonParserError(raw, None, "connection", "region from not found")
        region_from = raw["from"]

        if not isinstance(region_from, str):
            raise JsonParserError(raw, region_from, "connection", "region must be str")

        if "to" not in raw:
            raise JsonParserError(raw, None, "connection", "region to not found")
        region_to = raw["to"]

        if not isinstance(region_to, str):
            raise JsonParserError(raw, region_to, "connection", "region must be str")

        condition = None
        if "condition" in raw:
            condition = self.parse_condition(raw["condition"])

        return RegionConnection(region_from, region_to, condition)

    def parse_regions_data(self, raw: dict[str, typing.Any]) -> RegionsData:
        if "start" not in raw:
            raise JsonParserError(raw, None, "regions data", "must have starting region")
        start = raw["start"]

        if not isinstance(start, str):
            raise JsonParserError(raw, start, "regions data", "starting region must be a string")

        if "goal" not in raw:
            raise JsonParserError(raw, None, "regions data", "must have goal region")
        goal = raw["goal"]

        if not isinstance(goal, str):
            raise JsonParserError(raw, goal, "regions data", "goal region must be a string")

        exclude = []
        if "exclude" in raw:
            exclude = raw["exclude"]
            if not isinstance(exclude, list) or not all([isinstance(region, str) for region in exclude]):
                raise JsonParserError(raw, exclude, "regions data", "excluded regions must be strings")

        if "connections" not in raw:
            raise JsonParserError(raw, None, "regions data", "no connections found")
        raw_connections = raw["connections"]

        if not isinstance(raw_connections, list):
            raise JsonParserError(raw, raw_connections, "regions data", "connection must be list")

        regions_seen: set[str] = set()

        connections = []

        for raw_conn in raw_connections:
            conn = self.parse_region_connection(raw_conn)
            regions_seen.add(conn.region_to)
            regions_seen.add(conn.region_from)

            connections.append(conn)

        region_list = list(regions_seen)

        region_list.sort(key=lambda x: float(x.strip(string.ascii_letters)))

        return RegionsData(start, goal, exclude, region_list, connections)

    def parse_regions_data_list(self, raw: dict[str, dict[str, typing.Any]]) -> dict[str, RegionsData]:
        return {name: self.parse_regions_data(data) for name, data in raw.items()}
