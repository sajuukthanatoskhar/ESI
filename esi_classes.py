import dataclasses
import datetime
import io
import os
import queue
import webbrowser
from typing import List, Union, Optional
import esi_search_functions
import esipy
import pyswagger.primitives

import esi_market


@dataclasses.dataclass
class market_history_entry:
    average: int
    date: any
    highest: float
    lowest: float
    order_count: int
    volume: int

    def convert_date(self) -> None:
        """
        Converts string date to datetime - expected  is DD-MM-YYYY
        :return:
        """
        if isinstance(self.date, str):
            self.date = datetime.datetime.fromisoformat(self.date)

    def compare_date_to_today_date(self) -> int:
        """
        Returns days
        :return:
        """
        if isinstance(self.date, str):
            self.convert_date()
        today = datetime.datetime.today()
        return (today - self.date).days

    def export_to_json(self) -> None:
        """
        Exports market history to json
        :return: None
        """
        return None

    @classmethod
    def import_from_json(cls, input_json_file):
        if not input_json_file or input_json_file != io.TextIOWrapper:
            return False


@dataclasses.dataclass
class market_item_history:
    market_history: List[market_history_entry]
    name: str = ""
    item: str = ""
    item_typeid: str = ""
    regionid: str = ""
    region_name: str = ""
    required_qty: int = 0  # Reserved for market watcher, not used for actual history
    current_qty_in_region: int = 0  # Reserved for market watcher, not used for actual history
    to_be_produced: int = 0  # Reserved for market watcher, not used for actual history

    def calculate_quantity_required(self):
        """
        # Reserved for market watcher, not used for actual history
        :return:
        """
        self.to_be_produced = self.required_qty - self.current_qty_in_region

    def get_market_history(self):
        """
        Gets the Market history of an item
        :return:
        """
        self.market_history, self.item_typeid, self.regionid = esi_market.get_market_history_item_region(item=self.item,
                                                                                                         region_id=self.regionid,
                                                                                                         typeid=self.item_typeid,
                                                                                                         region_name=self.region_name)

    def update_all_dates(self) -> None:
        for entry in self.market_history:
            entry.convert_date()

    def filter_data_by_days_passed(self, days: int = 30) -> List[market_history_entry]:
        """
        Filter market data by a maximum number of days since the current date
        :param days:
        :return:
        """
        filtered_data: List[market_history_entry] = []
        for entry in self.market_history:
            if entry.compare_date_to_today_date() < days:
                filtered_data.append(entry)
            else:
                continue
        return filtered_data

    def get_market_velocity(self, market_data: List[market_history_entry] = None) -> float:
        no_of_days = len(market_data)
        number_of_orders = 0
        for entry in market_data:
            number_of_orders += entry.volume
        try:
            return number_of_orders / no_of_days
        except ZeroDivisionError:
            return 1


@dataclasses.dataclass
class esi_eve_market_order:
    """
    For eve online market orders
    """
    duration: int = 30
    escrow: float = 45.6
    is_buy_order: bool = False
    is_corporation: bool = False
    issued: Union[str, datetime.datetime, pyswagger.primitives.Datetime] = "2016-09-03T05:12:25Z"
    location_id: int = 456
    min_volume: int = 1
    order_id: int = 123
    price: float = 33.3
    range: str = "station"
    region_id: int = 123
    type_id: int = 456
    volume_remain: int = 4422
    volume_total: int = 123456
    item_name: str = "namename"
    type_name: str = "typetype"
    is_lowest_sell_order : bool = True

    def convert_issued_to_datetime(self) -> None:
        """
        Converts eve market orders to a datetime obj
        :return: None
        """
        if self.issued is str:
            self.issued = datetime.datetime.strptime(self.issued, "%Y-%m-%dT%H:%M:%S%z")
        elif self.issued is pyswagger.primitives.Datetime:
            self.issued = datetime.datetime.fromisoformat(self.issued)

    def update_values(self, **kwargs):
        """
        Updates all values from kwargs
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            try:
                self.__setattr__(k, v)
            except ValueError:
                print(f"{k} not present!")


class corporation:
    id: int
    name: str
    market_orders: List[esi_eve_market_order]

    def get_id(self, api_obj):
        return

    # @property
    # def old_market_orders(self) -> List[esi_eve_market_order]:
    #     if open(f"{self.id}_{self.name}_market_orders"):
    #         print("Market orders from previous day")

    # def get_market_orders(self, api_obj) -> Optional[dict]:
    #     self.market_orders = [order for order in esi_market.get_market_orders(self.id, self.name, api_obj)]
    #     return 0

    def convert_time_in_orders(self):
        for item in self.market_orders:
            item.convert_issued_to_datetime()


def check_data_header(data):
    x_page = None
    try:
        x_page = data.header.get('x-pages', None)
    except AttributeError:
        pass
    return x_page



class char_api_swagger_collection:
    def __init__(self, dot_env_f: str, scope: List[str]):

        # Set up esi_security stuff from dotenv
        self.dot_env_f = dot_env_f
        self.esi_security_details = Esi_Security_Details()
        self.esi_security_details.update_from_env_f(dot_env_f)
        self.call_back = self.esi_security_details.call_back
        self.client_id = self.esi_security_details.client_id
        self.secret_key = self.esi_security_details.secret_key
        self.mw_refresh_key = self.esi_security_details.mw_refresh_key
        self.scope = scope
        self.app = esipy.EsiApp().get_latest_swagger  # todo
        self.security = self.create_esi_security()
        self.client = self.create_client()
        self.api_info = self.security.verify(options={'verify_aud':False})
        self.char_id = self.get_char_id()

    def create_esi_security(self) -> esipy.EsiSecurity:
        return esipy.EsiSecurity(
            self.call_back,
            self.client_id,
            self.secret_key,
            headers={'User-Agent': 'Owned by Sajuukthanatoskhar'})

    def get_id_via_api_comm(self, type_id, market_item_q: queue.Queue = None):
        name = self.execute_api_command('get', "universe_types_type_id", type_id=type_id)['name']
        if market_item_q:
            market_item_q.put([name, type_id])
            return
        return name

    def get_universe_name_via_api_comm(self, region_id, market_item_q: queue.Queue = None):
        name = self.execute_api_command('get', "universe_names", type_id=region_id)['name']
        if market_item_q:
            market_item_q.put([name, region_id])
            return
        return name

    def refresh_token_key(self):
        self.security.update_token(
            {
                'access_token': '',  # leave this empty
                'expires_in': -1,  # seconds until expiry, so we force refresh anyway
                'refresh_token': self.mw_refresh_key
            })
        return self.security.refresh()

    def create_client(self):
        client = esipy.EsiClient(
            retry_requests=True,
            headers={'User-Agent': 'Owned by Sajuukthanatoskhar'},
            security=self.security  # Might be a problem
        )
        try:
            import dotenv
            if self.mw_refresh_key == "":
                webbrowser.open(self.security.get_auth_uri(state='logging_in_state', scopes=self.scope), new=1)
                access_token = input("Access token please (copypaste from the code section) --> ")
                refresh_key = self.security.auth(str(access_token))['refresh_token']

                dotenv.set_key(self.dot_env_f, "env_refresh_key", refresh_key)
            else:
                try:
                    self.refresh_token_key()
                except Exception:
                    webbrowser.open(self.security.get_auth_uri(state='logging_in_state', scopes=self.scope), new=1)
                    access_token = input("Access token please (copypaste from the code section")
                    refresh_key = self.security.auth(str(access_token))['refresh_token']
                    dotenv.set_key(self.dot_env_f, "env_refresh_key", refresh_key)

        except UnboundLocalError:
            pass
        return client

    def execute_api_command(self, type='get', api_command="characters_character_id_orders",
                            queue_obj: queue.Queue = None, **kwargs):
        """
        Executes an api command, kwargs are for the inputs required for an api command
        """
        data = None
        combined_command = f"{type}_{api_command}"

        try:
            op = self.app.op[combined_command](**kwargs)
            data = self.client.request(op)
        except ValueError as e:
            print(f"Exception - {kwargs} does not have the required input parameter -> {e.args}")
        except Exception as d:
            print(f"Unknown Error occurred -> {d}")
        if queue_obj:
            queue_obj.put(data.data)

        x_page = check_data_header(data)
        if not x_page:
           pass # raise KeyError(f"data.header has no 'xpages'")
        try:
            extra_data = data.data
        except AttributeError:
            extra_data = None
            print(f"data -> {data}?  Attribute error!")


        if x_page:
            if x_page[0] > 1:
                for i in range(2, data.header.get('x-pages')[0] + 1):
                    try:
                        kwargs['page'] = i
                        op = self.app.op[combined_command](**kwargs)
                        data = self.client.request(op)
                    except ValueError as e:
                        print(f"Exception - {kwargs} does not have the required input parameter -> {e.args}")
                    except Exception as d:
                        print(f"Unknown Error occurred -> {d}")
                    extra_data.extend(data.data)

        return extra_data

    def get_char_id(self):
        return self.api_info['sub'].split(':')[-1]


class character:
    id: int = -1
    name: str = ""
    #
    market_orders: List[esi_eve_market_order] = []


    def get_market_orders(self, api_obj) -> Optional[dict]:
        self.market_orders = [order for order in esi_market.get_market_orders(self.id, self.name, api_obj)]
        return 0

    def convert_time_in_orders(self):
        for item in self.market_orders:
            item.convert_issued_to_datetime()

    def get_current_market_share(self, api_obj: char_api_swagger_collection):
        """
        Gets the market share for all order types that are on market
        It gets each order, groups them by type id and region
        :return:
        """
        current_id = None
        temp_market_orders = set()
        market_ids_to_check = set()
        qty = 0
        regions = set()
        order : esi_eve_market_order

        market_order_dict = {}

        for order in self.market_orders:
            # Get all market orders
            market_ids_to_check.add(order.type_id)

        ######


        for order in self.market_orders:

            if not market_order_dict.get(f'{order.type_id}', None):
                market_order_dict[f'{order.type_id}'] = {}
                market_order_dict[f'{order.type_id}'][f'{order.region_id}'] = order.volume_remain
            else:# market_order_dict.get(f'{order.type_id}', {}).get(f'{order.region_id}', None):
                market_order_dict[f'{order.type_id}'][f'{order.region_id}'] += order.volume_remain

            #print(f"{order.order_id} -> {api_obj.get_id_via_api_comm(order.type_id)} --> ++{order.volume_remain} --> {market_order_dict[f'{order.type_id}'][f'{order.region_id}']}")




        return market_order_dict







@dataclasses.dataclass
class Esi_Security_Details:
    call_back: str = ""
    client_id: str = ""
    secret_key: str = ""
    mw_refresh_key: str = ""

    def update_from_env_f(self, env_file):
        import dotenv
        dotenv.load_dotenv(env_file)
        self.secret_key = os.environ.get("env_secret_key")
        self.client_id = os.environ.get("env_client_id")
        self.call_back = os.environ.get("env_call_back")
        self.mw_refresh_key = os.environ.get("env_refresh_key")



if __name__ == '__main__':
    import pyautogui

    pyautogui.press('F13')
