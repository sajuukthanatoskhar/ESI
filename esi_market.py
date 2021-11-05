import requests

import esi_classes
import esi_search_functions
import esi_config

def get_market_history_item_region(item : str = None,
                                   region : str = None,
                                   typeid : str = None,
                                   region_name : str = None) -> List[market_history_entry]:
    """
    Gets the market history for an item in a region
    :param item: Item name
    :param region: id of region
    :param typeid: typeid of item
    :return:
    """
    if not typeid:
        typeid = esi_search_functions.get_item_typeid(item)
    if not region:
        region = esi_search_functions.get_regionid(region_name)

    market_endpoint = f"markets/{region}/history/?datasource=tranquility&type_id={typeid}"
    market_dict_list = requests.get(esi_config.esi_startpoint + market_endpoint).json()
    return [esi_classes.market_history_entry(**entry) for entry in market_dict_list]