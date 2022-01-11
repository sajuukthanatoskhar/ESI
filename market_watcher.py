import dataclasses

import esipy
import webbrowser

import esi_market
from market_watcher_keys import *
import structure_watchlist
refresh_key = mw_refresh_key
import esi_classes
import esi_structure
import market_lists
import esi_search_functions

def market_watcher_func(market_watcher: list):
    item : esi_classes.market_item_history
    for item in market_watcher:
        for structure_market_item in watched_structures.market_order_list:
            if item.item == structure_market_item.item_name and not structure_market_item.is_buy_order:
                item.current_qty_in_region += structure_market_item.volume_remain
        item.calculate_quantity_required()
        print(f"{item.item}\t\t\t\t{item.to_be_produced}\t\t{watched_structures.name}\t\t{watched_structures.solar_system_name}")
    return None

if __name__ == '__main__':
    app_col = esi_classes.char_api_swagger_collection("market_watcher_keys.env", scope)
    op = app_col.app.op['get_characters_character_id_orders'](character_id=app_col.api_info['sub'].split(':')[-1])
    orders = app_col.client.request(op)

    achar = esi_classes.character
    achar.name = "Sajuukthanatoskhar"
    achar.market_orders = [esi_classes.esi_eve_market_order(**item) for item in orders.data]



    watched_structures = esi_structure.structure(name = structure_watchlist.structures_to_watch[1])
    watched_structures.get_struct_info(app_col)
    watched_structures.get_market_orders(app_col)

    #esi_market.get_market_group_names(app_col)

    market_watcher = market_lists.stage_1_escalation
    market_watcher_func(market_watcher)


    import dearpygui.dearpygui as dpg

    def save_callback():
        print("Save Clicked")

    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

    with dpg.window(label="Example Window"):
        dpg.add_text("Hello world")
        dpg.add_button(label="Save", callback=save_callback)
        dpg.add_input_text(label="string")
        dpg.add_slider_float(label="float")

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

