import time

from market_watcher_keys import *
from configurations import structure_watchlist

refresh_key = mw_refresh_key
from esi_formats import esi_search_functions, esi_classes, esi_structure


def market_watcher_func(market_watcher: list):
    item : esi_classes.market_item_history
    for item in market_watcher:
        for structure_market_item in watched_structures.market_order_list:
            if item.item == structure_market_item.item_name and not structure_market_item.is_buy_order:
                item.current_qty_in_region += structure_market_item.volume_remain
        item.calculate_quantity_required()
        print(f"{item.item}\t\t\t\t{item.to_be_produced}\t\t{watched_structures.name}\t\t{watched_structures.solar_system_name}")
    return None

def compare_mymarketorder_vs_other_orders(mychar: esi_classes.character,
                                          target_market_structure: esi_structure.structure):
    for myorder in mychar.market_orders:
        for order in target_market_structure.market_order_list:
            if myorder.type_id == order.type_id:
                if order.price <= myorder.price:
                    if not order.is_buy_order and not myorder.is_buy_order: # todo: what if the order is my own order?  :thinking:
                        myorder.is_lowest_sell_order = False







def get_my_market_ids_in_regions(character: esi_classes.character):
    unique_ids = set()
    regions = set()
    for order in achar.market_orders:
        # Get all market orders
        unique_ids.add(order.type_id)
        regions.add(order.region_id)
    return unique_ids, regions


def get_watched_struct_info_market(app_col, watched_structures, DEBUG = True):
    """
    Gets the structure info
    :param app_col:
    :param DEBUG:
    :return:
    """
    for structure_under_watch in watched_structures:
        structure_under_watch.get_struct_info(app_col)
        if DEBUG:
            start_time = time.time()
        structure_under_watch.get_market_orders(app_col)
        if DEBUG:
            print(f"Get market orders -> Execution took {time.time() - start_time} seconds.")


if __name__ == '__main__':
    app_col = esi_classes.char_api_swagger_collection("market_watcher_keys.env", scope)
    op = app_col.app.op['get_characters_character_id_orders'](character_id=app_col.api_info['sub'].split(':')[-1])
    orders = app_col.client.request(op)

    achar = esi_classes.character()
    achar.name = "Sajuukthanatoskhar"
    achar.market_orders = [esi_classes.esi_eve_market_order(**item) for item in orders.data]

    character_orders = achar.get_current_market_share(app_col,)


    watched_structures = [esi_structure.structure(name = struct_name)
                          for struct_name in structure_watchlist.structures_to_watch]
    get_watched_struct_info_market(app_col, watched_structures) # Gets the struct info and

    market_summary_by_id = {}
    unique_ids = set()  # Type ID's of market orders
    regions = set()

    compare_mymarketorder_vs_other_orders(achar, watched_structures)
    unique_ids, regions = get_my_market_ids_in_regions(achar)

    #esi_market.get_market_group_names(app_col)
    # Get structure market order aggregate
    for unique_id in unique_ids:
        struct_order_list = []
        for order in watched_structures.market_order_list:
            if unique_id == order.type_id:
                struct_order_list.append(order.volume_remain)

        total = sum(struct_order_list)
        market_summary_by_id[f'{unique_id}'] = total

    percentage_summary = {}

    for region in regions:
        for unique_id in unique_ids:
            percentage_summary[app_col.get_id_via_api_comm(unique_id)] = {}
            percentage_summary[app_col.get_id_via_api_comm(unique_id)][str(region)] =  character_orders[f'{unique_id}'][str(region)]*100/market_summary_by_id[f'{unique_id}']




    import dearpygui.dearpygui as dpg

    def save_callback():
        print("Save Clicked")



    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

    with dpg.window(label="Summary of Market Control"):
        for region in regions:
            print(f"********{(str(region))}*********")
            for k,v in percentage_summary.items():
                character_order = character_orders[str(esi_search_functions.get_item_typeid(k))][str(region)]

                region_orders = market_summary_by_id[str(esi_search_functions.get_item_typeid(k))]
                string_print = f"{k} -> {percentage_summary[k][str(region)]:.2f}% {character_order}/{region_orders}"
                print(string_print)
                dpg.add_text(string_print)
        # dpg.add_button(label="Save", callback=save_callback)
        # dpg.add_input_text(label="string")
        # dpg.add_slider_float(label="float")

    with dpg.window(label="Summary of Market Orders"):
        for region in regions:
            print(f"********{(str(region))}*********")
            import operator
            market_order : esi_classes.esi_eve_market_order

            # sort all of char orders by item name occurs here
            for order in achar.market_orders:
                order.item_name = app_col.get_id_via_api_comm(order.type_id)
            achar.market_orders.sort(key=operator.attrgetter("item_name"))
            compare_mymarketorder_vs_other_orders(achar, watched_structures)
            for market_order in achar.market_orders:
                if region == market_order.region_id and not market_order.is_lowest_sell_order:
                    string_print = f"{market_order.item_name} is lowest --> {market_order.is_lowest_sell_order}"
                    print(string_print)
                    dpg.add_text(string_print)
        # dpg.add_button(label="Save", callback=save_callback)
        # dpg.add_input_text(label="string")
        # dpg.add_slider_float(label="float")

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()