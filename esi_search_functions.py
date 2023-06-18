from typing import Union

import requests

import esi_config


def get_search(entity_type: str, search_string: str, strict="True", api_obj = None) -> Union[list, str, int]:
    """
    Searches for any entity from the esi
    :param entity_type:
    :param search_string:  the thing you are looking for
    :return: requests json
    """
    # url = f"{esi_config.esi_startpoint}search/?categories={entity_type}&datasource=tranquility&language=en&search={search_string.replace(' ', '%20')}&strict={strict}"
    #print(url)
    request_made : dict = api_obj.execute_api_command('get',"characters_character_id_search",categories=f"{entity_type}",character_id=api_obj.char_id,search=f"{search_string}", strict=strict)

    if entity_type:
        if len(request_made[entity_type]) == 1:
            return request_made[entity_type][0]
        return request_made[entity_type]
    else:
        return request_made


def get_regionid(region_name,api_obj):
    """Gets the region ID"""
    return get_search(entity_type="region", search_string=region_name, api_obj=api_obj)

def get_character_id(char_id):
    return get_search(entity_type="character", search_string=char_id, strict="True")

def get_item_typeid(item_name: str, api_obj):
    """

    :param item_name:
    :return:
    """
    return get_search(entity_type='inventory_type', search_string=item_name, strict="True", api_obj = api_obj)


def get_category_information(api_obj, category_id):
    pass

if __name__ == '__main__':
    print(get_item_typeid("sabre"))