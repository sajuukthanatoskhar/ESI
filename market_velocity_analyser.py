from typing import List

import esi_config
import esi_classes
import esi_market
import esi_search_functions
import esi_config
import market_itemstocheck

target_region = "Outer Passage"

if __name__ == '__main__':

    items_analysed : List[esi_classes.market_item_history] = [esi_classes.market_item_history(market_history=[], item=item,
                                                                                              region_name=target_region)
                                                              for item in market_itemstocheck.items_to_analyse]




    for item in items_analysed:
        try:
            item.get_market_history()
        except KeyError as e:
            print(e)

        print(f"{item.item} {int(item.get_market_velocity(item.filter_data_by_days_passed(30))*15)}")
