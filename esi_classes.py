import dataclasses
from typing import List

import esi_market


@dataclasses.dataclass
class market_history_entry:
    average : int
    date: str
    highest : float
    lowest : float
    order_count : int
    volume : int

@dataclasses.dataclass
class market_item_history:
    name: str
    item: str
    item_typeid : str
    market_history : List[market_history_entry]
    region: str
    region_name : str

    def get_market_history(self):
        self.market_history = esi_market.get_market_history_item_region(item = self.item, region = self.region,
                                                                        typeid = self.item_typeid,
                                                                        region_name = self.region_name)