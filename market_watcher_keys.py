import os

from dotenv import load_dotenv

load_dotenv("market_watcher_keys.env")

client_id = os.environ.get("env_client_id")
secret_key = os.environ.get("env_secret_key")
call_back = "http://localhost:65432/callback/"
scope = ["esi-search.search_structures.v1",
         "esi-universe.read_structures.v1",
         "esi-markets.structure_markets.v1",
         "esi-corporations.read_structures.v1",
         "esi-markets.read_character_orders.v1",
         "esi-markets.read_corporation_orders.v1"]
mw_refresh_key= os.environ.get("env_refresh_key")
access_token: str = ""

