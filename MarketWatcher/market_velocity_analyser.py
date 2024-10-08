import sys
from typing import List

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    pass
else:
    pass
from esi_formats import esi_classes
from configurations import market_itemstocheck

target_region = "Deklein"

if __name__ == '__main__':



    items_analysed : List[esi_classes.market_item_history] = [
        esi_classes.market_item_history(market_history=[], item=item,
                                        region_name=target_region)
        for item in market_itemstocheck.items_to_analyse]




    for item in items_analysed:
        try:
            item.get_market_history(app= None)
        except KeyError as e:
            print(e)

        print(f"{item.item} {int(item.get_market_velocity(item.filter_data_by_days_passed(30))*15)}")
