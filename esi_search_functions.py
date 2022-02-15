from typing import Union

import requests

import esi_config


def get_search(entity_type: str, search_string: str, strict="False") -> Union[list, str, int]:
    """
    Searches for any entity from the esi
    :param entity_type:
    :param search_string:  the thing you are looking for
    :return: requests json
    """
    url = f"{esi_config.esi_startpoint}search/?categories={entity_type}&datasource=tranquility&language=en&search={search_string.replace(' ', '%20')}&strict={strict}"
    #print(url)
    request_made = requests.get(url)
    if entity_type:
        if len(request_made.json()[entity_type]) == 1:
            return request_made.json()[entity_type][0]
        return request_made.json()[entity_type]
    else:
        return requests.get(url).json()


def get_regionid(region_name):
    """Gets the region ID"""
    return get_search(entity_type="region", search_string=region_name)

def get_character_id(char_id):
    return get_search(entity_type="character", search_string=char_id, strict="True")

def get_item_typeid(item_name: str):
    """

    :param item_name:
    :return:
    """
    return get_search(entity_type='inventory_type', search_string=item_name, strict="True")


def get_category_information(api_obj, category_id):
    pass

if __name__ == '__main__':
    print(get_item_typeid("sabre"))