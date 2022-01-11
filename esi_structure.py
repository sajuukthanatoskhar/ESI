import dataclasses
import queue
import threading
from typing import List
import asyncio
import esi_classes


@dataclasses.dataclass
class c_coordinate:
    y: float = 0.0
    x: float = 0.0
    z: float = 0.0
    def update_pos(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
        return 1


@dataclasses.dataclass
class structure:
    str_id: int = 0
    name: str = ""
    position: c_coordinate = c_coordinate(x = -1, y = -1, z = -1)
    solar_system_id: int = 0
    type_id: int  = 0 # structure
    solar_system_name: str = ""
    type_name: str = ""  # structure type

    market_order_list: List[esi_classes.esi_eve_market_order] = dataclasses.field(default_factory=list)

    def get_name(self, api_obj) -> int:
        op = api_obj.execute_api_command('get', "characters_character_id_search",
                                    categories = "structure",
                                    character_id = api_obj.char_id,
                                    search = f"{self.name}")
        data = op.data
        self.name = data[0]



    def get_market_orders(self, api_obj:esi_classes.char_api_swagger_collection) -> int:
        """

        :param api_obj:
        :return:
        """
        if self.str_id != '0':
            op = api_obj.execute_api_command('get', "markets_structures_structure_id", structure_id = self.str_id)
            market_data = op
            market_item_q = queue.Queue()
            tasks = []
            # for item in market_data:
            #     tasks.append(threading.Thread(target= api_obj.get_id_via_api_comm,
            #                                   args = {
            #                                       item['type_id'],
            #                                       market_item_q
            #                                   }))
            # for idx, task in enumerate(tasks):
            #     task.start()
            #     task.join(timeout=1)

            # while not market_item_q.empty():
            #     k,v = market_item_q.get()
            #     for order in market_data:
            #         self.market_order_list.append(esi_classes.esi_eve_market_order())
            #         if v == order['type_id']:
            #             print(self.market_order_list[-1].item_name)
            #             self.market_order_list[-1].update_values(**order)
            #             self.market_order_list[-1].item_name = k
            #             print(self.market_order_list[-1].item_name)
            for order in market_data:
                self.market_order_list.append(esi_classes.esi_eve_market_order())
                self.market_order_list[-1].update_values(**order)
                self.market_order_list[-1].item_name = api_obj.execute_api_command('get',"universe_types_type_id",type_id = order['type_id'])['name']



            return 0 # successful
        return 1 # Not successful
    def get_struct_info(self, api_obj :esi_classes.char_api_swagger_collection):
        if self.name == "" and self.str_id == 0:
            print("Name or ID not provided")
            return 0
        if self.str_id == 0 and self.name != "":
            self.get_id(api_obj)
        data = api_obj.execute_api_command('get', "universe_structures_structure_id", structure_id = self.str_id)

        for k,v in data.items():
            self.__setattr__(k,v)
        self.type_name = api_obj.execute_api_command('get',"universe_types_type_id",type_id = self.type_id).name
        return 1

    def get_id(self, api_obj :esi_classes.char_api_swagger_collection):


        data = api_obj.execute_api_command('get', "characters_character_id_search",
                                              categories = "structure",
                                              character_id = api_obj.char_id,
                                              search = f"{self.name}")

        if len(data['structure']) == 1:
            self.str_id = data['structure'][0]
            return 0
        elif len(data['structure']) == 0:
            print("No structure found")
            return 1
        print(data['structure'])