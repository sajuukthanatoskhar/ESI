from typing import List, Union

import requests

import esi_search_functions
import esi_config
import esi_classes
import fuzzworks_bpos.fuzzworks


def get_market_history_item_region(item: str = None,
                                   region_id: str = None,
                                   typeid: str = None,
                                   region_name: str = None, app_col = None):
    """
    Gets the market history for an item in a region
    :param region_name:
    :param item: Item name
    :param region_id: id of region
    :param typeid: typeid of item
    :return:
    """
    if not typeid:
        typeid = esi_search_functions.get_item_typeid(item, app_col)
    if not region_id:
        region_id = esi_search_functions.get_regionid(region_name, app_col)

    market_endpoint = f"markets/{region_id}/history/?datasource=tranquility&type_id={typeid}"
    market_dict_list = requests.get(esi_config.esi_startpoint + market_endpoint).json()
    return [esi_classes.market_history_entry(**entry) for entry in market_dict_list], typeid, region_id


def get_market_orders(api_obj) -> Union[None, dict]:
    """


    """


    return api_obj.execute_api_command('get', "characters_corporation_id_orders", character_id=api_obj.char_id)


def get_open_market_order_regionid_typeid_ordertype(api_obj, region_name : str, item_name : str, order_type = 'sell',  ):
    """
    Gets the order for an item in a region using the public market index
    """
    type_id = fuzzworks_bpos.fuzzworks.get_single_id(item_name)
    region_id = esi_search_functions.get_regionid(region_name, api_obj)
    return api_obj.execute_api_command('get', "markets_region_id_orders", region_id=region_id, type_id = type_id, order_type = order_type)


def get_market_groups(api_obj) -> list[int]:
    """Gets all market groups
    :return list of all item group ids"""
    return api_obj.execute_api_command('get', "markets_groups")


def get_market_group_names(api_obj):
    import threading
    import queue
    q = queue.Queue()
    tasks = []
    for group in get_market_groups(api_obj):
        tasks.append(threading.Thread(target=api_obj.execute_api_command,
                                      kwargs={
                                          'type': 'get',
                                          'api_command': "markets_groups_market_group_id",
                                          'queue_obj': q,
                                          'market_group_id': group}))
    for idx, task in enumerate(tasks):
        task.start()
        task.join()
        print(f"Thread {idx} started")

    # for idx, task in enumerate(tasks):
    #     task.join()
    #     print(f"Thread {idx} joined\n")

    result_list = []
    while not q.empty():
        result_list.append(q.get())

    return result_list
