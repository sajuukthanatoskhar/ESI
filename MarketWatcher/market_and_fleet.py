import codecs
import json
import sqlite3
import time
import urllib.request
import _thread
import os
import threading
from queue import Queue
import math
import yaml

from eve_esi_framwork import authpython
from esi_formats import esi_classes

from MarketWatcher.market_watcher_keys import scope

global totalcost
totalcost = 0
global _debug
global moon_ingredients
moon_ingredients = {}
_debug = 0

print_lock = threading.Lock()
queueumult = Queue()
locks = []
from configurations.esi_config import esi_startpoint


def req_esi(request_esi):
    """
    General ESI request
    @warning will be deprecated
    :param request_esi:
    :return:
    """
    if _debug == 1:
        print(f"{esi_startpoint}{request_esi}")
    wp = urllib.request.urlopen(f"{esi_startpoint}{request_esi}")
    return wp


def req_fuzzwork(request):
    """
    Generic fuzzwork
    @warning will be deprecated
    :param request:
    :return:
    """
    wp = urllib.request.urlopen("https://www.fuzzwork.co.uk/blueprint/api/blueprint.php?typeid=%s" % (request))
    return wp


def threaded_reaction_cost(thread_lock_no, materialname, runs_required, market_hub, alliance_home_region, api_obj):
    """
    Calculates reaction cost using a thread
    :param thread_lock_no:
    :param materialname:
    :param runs_required:
    :param market_hub:
    :param alliance_home_region:
    :return:
    """
    # TODO:reactioncost
    print("calculating cost of reaction using" + str(thread_lock_no))
    reaction_cost(materialname, runs_required, market_hub, alliance_home_region, api_obj= api_obj)
    thread_lock_no.release()
    '''
    One time run function
    '''


def load_evedb(eve_db_file):
    conn = sqlite3.connect(eve_db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM invtypes")
    rows = cur.fetchall()
    file_write = codecs.open("../resources/eve_inv_types.etf", "w", "utf-8")
    for row in rows:
        outputfromsqlite = str(row[0]) + " " + str(row[1])
        print(outputfromsqlite)
        file_write.write(str(outputfromsqlite) + "\n")
    file_write.close()


"""
This gets the item_id from the *.etf listed
returns type_id as an integer value
"""

from esi_formats.esi_search_functions import get_item_typeid
def get_typeid(name,api_obj):
    return get_item_typeid(name,api_obj)




from esi_formats.esi_search_functions import get_regionid
def get_region(name,api_obj):
    '''
    Gives the region_id
    Input is region name
    returns region_id as integer
    '''
    return get_regionid(name, api_obj=api_obj)

'''
Is reciprocal function of get_typeid
Gives the item name
Input is item input
returns item name as string
'''


def get_name(item_id_input):
    with open("../resources/eve_inv_types.etf", mode="r", encoding="utf-8") as sourcefile:
        for line in sourcefile:
            parts_k = line.split()
            item_name = ' '.join(parts_k[1:])
            item_id = parts_k[0]
            if int(item_id_input) == int(item_id):
                return item_name


"""
Returns the output from a blueprint
Doesn't deal with drugs very well (rip)
input is reaction id
returns output quantity as string
"""


def get_reaction_output_quantity(reaction_id):
    with open("../resources/blueprints.etf", mode="r", encoding="utf-8") as sourcefile:
        for line in sourcefile:
            parts_k = line.split()
            reaction_list_id = parts_k[0]
            output_from_list = parts_k[1]
            if str(reaction_id) == str(reaction_list_id):
                return output_from_list


"""
Function gets market price in target region
region is name of a region in Tranquility
itemtype is the name of an item
"""


def get_market_price(region, itemtype, api_obj, order_type = 'sell'):
    type_id_request = get_typeid(itemtype, api_obj=api_obj)
    region_id = get_region(region, api_obj)
    reader = codecs.getreader("utf-8")
    pw = api_obj.execute_api_command('get',"markets_region_id_orders",order_type= order_type,region_id=region_id,type_id=type_id_request)

    # pw = json.load(reader(req_esi("markets/%s/orders/?order_type=sell&type_id=%s&datasource=tranquility" % (region_id, type_id_request))))
    ordered_list = print_ordered_JSON(pw, type_id_request, region_id, region, itemtype)
    ordered_list_index_total = len(ordered_list)
    spread = int(round(ordered_list_index_total / 10, 0) * 2)
    if spread == 0:
        spread = 1
    ordercount = 0
    totalcost = 0
    for an_order in ordered_list:
        totalcost += an_order.cost * an_order.volumeremain
        ordercount += an_order.volumeremain
    try:
        price = totalcost / ordercount
    except ZeroDivisionError:
        return 0
    return round(price, 2)


""""
    i = 0
    # print(pw[0]["average_price"])


    remainder = ""
    print("Price Lookup for %s (%s) in %s (%s)"%(itemtype,type_id_request,region,region_id))
    print("Item Type \t\t\tPrice \t\t\tRemaining Items")
    while i < len(pw):
        type_id = pw[i]["type_id"]
        volume_total = pw[i]["volume_total"]
        price = pw[i]["price"]
        with open("eve_inv_types.etf", mode="r", encoding="utf-8") as sourcefile:
            for line in sourcefile:
                target = re.search(r'\d+', line).group()
                # print(target)
                # print(type_id)
                # typeid, itemname = line.split(None, 1)
                parts_k = line.split()
                typeid_k = parts_k[0]
                itemname_k = ' '.join(parts_k[1:])
                # print(itemname_k)
                if str(target) == str(type_id_request):
                    # print("A match - %s compared to %s and is %s" % (target, type_id,itemname_k))
                    print("%s \t\t\t%-15s \t\t\t%-10.5s \t\t\t%-10.8s mil isk" % (itemname_k, pw[i]["price"], pw[i]["volume_remain"],str(float(pw[i]["price"]) * float(pw[i]["volume_remain"] / 1000000))))
                    # print(remainder)
        # print(str(pw[i]["type_id"])+"\t\t\t"+str(pw[i]["volume_total"])+"\t\t\t"+str(pw[i]["price"]))
        i = i + 1
        """


def print_ordered_JSON(json_market_order_part, type_id_request, region_id, region, itemtype):
    """
    Parses the json from the ordered market order from get_market_price(x,y,z,a)
    Input is json_market_order_part
    """
    i = 0
    marketorders = []
    while i < len(json_market_order_part):
        type_id = json_market_order_part[i]["type_id"]
        volume_total = json_market_order_part[i]["volume_total"]
        price = json_market_order_part[i]["price"]
        market_order = market_item(itemtype=type_id, volumeremain=volume_total, cost=price)
        marketorders.append(market_order)
        i = i + 1
    marketorders.sort(key=lambda marketorders: marketorders.cost)
    i = 0
    return marketorders


class market_item:
    """
    Class defining a market order that is useful for gauging its cost, could've used a dict but I didn't like how much formatting and work is required whereas a class solves it easily enough for me
    """

    def __init__(self, itemtype, volumeremain, cost):
        self.itemtype = itemtype
        self.volumeremain = volumeremain
        self.cost = cost


def get_blueprint_details(name, api_obj):
    """
    Get the blueprint details from fuzzworks
    Example - https://www.fuzzwork.co.uk/blueprint/api/blueprint.php?typeid=22457
    Input is the name of the blueprint, you have to include the ' Blueprint' or ' Reaction Formula', note the spaces
    Output is a JSON blob for the blueprint
    :param name:
    :return:
    """
    reader = codecs.getreader("utf-8")
    type_id_request = get_typeid(name, api_obj=api_obj)
    js_wp = json.load(reader(req_fuzzwork(type_id_request)))
    return js_wp


def get_reactionoutput(target_reaction):
    """
    Getting Reaction Output using the blueprints.yaml
    Deprecated but kept to show previous mistakes
    :param target_reaction: reaction to get
    :return:
    """
    with open("../resources/blueprints.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
        max_lines = len(config)
        print(config[int(target_reaction)]["activities"]["reaction"]["products"][0]["quantity"])
        return config[int(target_reaction)]["activities"]["reaction"]["products"][0]["quantity"]


def reaction_cost(complex_reaction, runs, marketregion, homeregion, api_obj):
    """
    Calculates complex reaction expenditure and revenue based on the get_market_price(x,y) function algorithm
    Input is the name of the complex reaction as a string, the number of runs of raw moon minerals, the marketregion where you are retrieving your prices from, homeregion has no functionality
    The results are printed out and the return is void
    It prints out the resources needed for the runs and are formatted on the console in a way so that you can put them into multibuy
    """
    global moon_ingredients
    if complex_reaction != "Fullerides":
        complexr = get_blueprint_details(complex_reaction + " Reaction Formula", api_obj)
    else:
        complexr = get_blueprint_details(complex_reaction[:-1] + " Reaction Formula", api_obj)
    if complex_reaction != "Fullerides":
        print(str(complex_reaction) + " Output Revenue (" + str(runs) + " runs of raw minerals): " + str(
            int(get_market_price(marketregion, complex_reaction, api_obj)) * runs * 2 * int(get_reaction_output_quantity(
                get_typeid(complex_reaction + " Reaction Formula",api_obj))) / 1E6) + " M Isk  (Total Units = " + str(
            int(get_reaction_output_quantity(get_typeid(complex_reaction + " Reaction Formula",api_obj))) * runs * 2) + ")")
    else:
        print(str(complex_reaction) + " Output Revenue (" + str(runs) + " runs of raw minerals): " + str(
            int(get_market_price(marketregion, complex_reaction, api_obj)) * runs * 2 * int(get_reaction_output_quantity(
                get_typeid(complex_reaction[:-1] + " Reaction Formula", api_obj))) / 1E6) + " M Isk  (Total Units = " + str(int(
            get_reaction_output_quantity(get_typeid(complex_reaction[:-1] + " Reaction Formula", api_obj))) * runs * 2) + ")")
    simple_reaction = []
    total_raw_input = 0

    for line in complexr['activityMaterials']['11']:
        tempprice = get_market_price(marketregion, line['name'], api_obj)
        if 'Block' in line['name']:
            total_raw_input = tempprice * 5 * runs * 2 + total_raw_input
        else:
            simple_reaction.append(get_blueprint_details(line['name'] + " Reaction Formula", api_obj))
    i = 0

    for superline in simple_reaction:
        for line in superline['activityMaterials']['11']:
            tempprice = get_market_price(marketregion, line['name'], api_obj)
            if 'Block' in line['name']:
                # print(line['name'] + " " + str(runs * 5))  # + str(tempprice*5*runs))
                # print(line['name'] + " " + str(runs * 100))  # + str(tempprice*5*runs))
                # We will deal with this later
                total_raw_input = total_raw_input + tempprice * 5 * runs
            else:
                print(line['name'] + " " + str(runs * 100))  # + " " + str(tempprice*100*runs))
                total_raw_input = total_raw_input + tempprice * 100 * runs
                if line['name'] in moon_ingredients:
                    moon_ingredients[line['name']] += runs * 100
                else:
                    moon_ingredients[line['name']] = runs * 100

        i = i + 1
    # How many simple reactions?
    print("Input cost is = " + str(round(float(total_raw_input / 1E6), 2)) + " M Isk")

    global totalcost
    totalcost += total_raw_input



def get_fleet_groups(fleet_doc):
    """
    Retrieves the different groups of fleets as described in the fleet_doc input as described in any of the doctrines folder's files
    It compresses the lists so that nothing is duplicated
    outputs are the fleet groups in group index and the group's ratios
    """
    # Compresses the duplicates of the roles of ships so you don't have duplicate shiptypes
    groups = list(set(fleet_doc.allowedshipsrole))
    group_ratio = []

    ratio_index_list = [i for i in range(len(fleet_doc.allowedshipsrole)) if i != fleet_doc.allowedshipsrole.index(fleet_doc.allowedshipsrole[i])]
    # These find the indexes being used... I didn't write this code and is hard to read holy shit. TODO: Learn how to code in python
    ratioindex = [i for j, i in enumerate(fleet_doc.allowedshipsratio) if j not in ratio_index_list]
    groupindex = [i for j, i in enumerate(fleet_doc.allowedshipsrole) if j not in ratio_index_list]
    return groupindex, ratioindex


"""
Reads through the fleetjson (fleet json blob input) and checks against the fleet doctrine if the 
length is the number of members in the fleet.  It then add's the allowed ship's weight to the fleet group count.  
fleet doctrine input is a fleet_doctrine 

This function is very important and is hard to get your head around.  
"""


def process_fleet_comp(fleetjson, length, fleet_doctrine):
    """
    Processes the fleet composition
    :param fleetjson:
    :param length:
    :param fleet_doctrine:
    :return:
    """
    i = 0
    fleet_groups, group_ratio = get_fleet_groups(fleet_doctrine)
    fleet_group_count = list(range(0, len(group_ratio)))

    while i < len(fleet_group_count):  # Resets fleet group count, probably can delete  #TODO: Please check!
        fleet_group_count[i] = 0
        i += 1
    i = j = z = 0
    while z < length:  # Loop through every member in the fleet to....
        checkshipname = get_name(fleetjson[z]["ship_type_id"])
        i = 0
        while i < len(
                fleet_doctrine.allowedships):  # ...check if they have one of the allowed ship types by looping through them and then...
            if checkshipname == fleet_doctrine.allowedships[i]:
                # print(checkshipname + " is allowed")
                j = 0
                while j < len(
                        fleet_group_count):  # ...it's added to the right fleet group by checking their ship belongs to that group
                    if fleet_doctrine.allowedshipsrole[i] == fleet_groups[j]:
                        # add 1 to the group in fleet_group_count if the ship role matches
                        fleet_group_count[j] = fleet_group_count[
                                                   j] + 1  # todo: implement the weight where the '1' is in this line, it's really simple but I am lazy

                    j = j + 1
                # add ship's weight to total group weight
            i = i + 1
        z = z + 1
    return fleet_groups, group_ratio, fleet_group_count


def read_tokens(file):
    """
    Reading the tokens made from the pythonserver.py functions from a file (mostly it should be 'key.key')
    Input is the file
    The file is formatted into two columns, one line
    output are the two tokens
    """
    keys_file = open(file, "r")
    access_token = refresh_token = 0
    for lines in keys_file:
        pw = lines.split(" ")  # [0] is access_token, #[1] is refresh
        access_token = pw[0]  # First column
        refresh_token = pw[1]  # Second Column
    print(authpython.refresh('1', refresh_token))
    return access_token, refresh_token




"""
requests.put(url, data=json.dumps(
{
'fleet_id': 000000,
'new_settings': {
"motd": "string",
"is_free_move": true
},
<other parameters>
}))
"""

"""
Retrieves a ship's id
Input is the name of the ship (capitalisation is required)
output is the ship's id
Implemented for multithreading based functions only"""


def getshiptypeid(name):
    reader = codecs.getreader("utf-8")
    ship_id = json.load(reader(req_esi(
        'search/?categories=inventorytype&datasource=tranquility&language=en-us&search=%s&strict=true' % name)))
    print(ship_id["inventorytype"][0])
    return ship_id["inventorytype"][0]


def unload_blueprintsyaml():
    """
    Reads the blueprints.yaml file and translates it into a simpler file that states the name of the blueprint nad its output quantity
    Not yet implemented for drugs
    :return:
    """
    with open("../resources/blueprints.yaml", 'r') as stream:
        file_write = codecs.open("../resources/blueprints.etf", "w", "utf-8")
        config = yaml.safe_load(stream)
        for line in config:
            if "reaction" not in str(config[line].items()):
                print("Continued : " + str(line))
            else:
                file_write.write(str(line) + " " + str(
                    config[int(line)]["activities"]["reaction"]["products"][0]["quantity"]) + "\n")
        file_write.close()


def create_DB(db_file_name):
    """
    Creates a database using the file name as input.  If the table in the database exists, it won't be modified
    """
    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS evestuff(id INTEGER, name varchar[200])")
    with open("../resources/eve_inv_types.etf", mode="r", encoding="utf-8") as sourcefile:
        for line in sourcefile:
            parts_k = line.split()
            parts_k = (parts_k[0], ' '.join(parts_k[1:]))
            c.execute('insert into evestuff values (?,?)', (int(parts_k[0]), str(parts_k[1])))
    conn.commit()
    return [c, conn]





def get_shipname_from_db(name, db):
    """
    Experimental Function using sqlite
    Not implemented
    Input is ship id and database connection (not database itself and is the 'conn' variable output from create_db)
    """
    db.execute('select id,name from evestuff WHERE id="%s"' % name)
    rows = db.fetchall()
    for row in rows:
        print(row[1])
    return row[1]





def multi_stuff():
    """
    Experimental Function using threading
    Not implemented
    """
    conn = sqlite3.connect('evetype.db')
    c = conn.cursor()
    threadList = []
    ship = ['sabre']
    numofThread = 250
    for i in range(numofThread):
        t = threading.Thread(target=getshiptypeid, args=ship)
        t.start()
        threadList.append(t)
    print(str(threading.active_count()))
    for i in threadList:
        i.join()




def check_file(file):
    """
    Checks if the file exists
    """
    if os.path.exists(file):
        return 1
    else:
        return 0





def get_number_of_runs_for_build(market_hub, alliance_home_region, file, api_obj):
    """
    In this function I want to read materials
    First, we take stuff from fuzzworks and dump it into a file, this is done outside the program for now
    Secondly, we read the contents of that file line by line
        In each line, we will need to get the name of the complex material and the number of runs it needs to be done (runs needs to be ceil-rounded)
        These runs and materials will then be fed into reaction_cost()
    INPUTS

    market_hub = high sec market hub of choice (region) eg. The Forge (for jita)
    alliance_home_region = Alliance's home region (Not implemented)
    file = file that you have dumped the following format
    COMPLEX_REACTION_NAME COMPLEX_REACTION_QUANTITY
    """
    # Get number of lines in file
    global moon_ingredients
    NumofThreads = sum(1 for line in open(file))
    threadList = []
    if check_file(file):
        with open(file, mode="r") as file_to_read:  # Does the reaction cost
            for line in file_to_read:
                parts_k = line.split()
                materialname = str(' '.join(parts_k[1:]))
                materialquantity = parts_k[0]
                runs_required = math.ceil(float(materialquantity) / (2 * float(
                    get_reaction_output_quantity(get_typeid(get_complex_material_reaction_name(materialname),api_obj)))))
                a_lock = _thread.allocate_lock()
                a_lock.acquire()
                locks.append(a_lock)
                _thread.start_new_thread(threaded_reaction_cost,
                                         (a_lock, materialname, runs_required, market_hub, alliance_home_region, api_obj))
        with open(file, mode="r") as file_to_read:  # Summarises the complex reactions
            for line in file_to_read:
                parts_k = line.split()
                materialname = str(' '.join(parts_k[1:]))
                materialquantity = parts_k[0]
                runs_required = math.ceil(float(materialquantity) / (2 * float(
                    get_reaction_output_quantity(get_typeid(get_complex_material_reaction_name(materialname),api_obj)))))
                print(materialname + " " + str(runs_required))
    else:
        print("Error: " + file + " does not exist")





def get_complex_material_reaction_name(complex_reaction):
    """
    This function takes in the name of a complex reaction
    """
    if complex_reaction != "Fullerides":
        complexr = complex_reaction + " Reaction Formula"
    else:
        complexr = complex_reaction[:-1] + " Reaction Formula"
    return complexr





def main():
    """
    The Main function
    There is a lot of random stuff commented out here as I tend to uncomment them for various uses
    """
    #load_evedb("eve.db")
    app_col = esi_classes.char_api_swagger_collection("market_watcher_keys.env", scope)
    achar = esi_classes.character()
    achar.name = "Sajuukthanatoskhar"


   # get_number_of_runs_for_build("The Forge", "Perrigen Falls", "outputdump.txt", app_col)
    # MoonGooGUI.MoonGooGui()
    # multi_stuff()
    # unload_blueprintsyaml()
    # create_DB("stuff.db")
    # fleet_overwatch("harpy", 1, 'sajuukthanatoskhar')
    # print(get_market_price("The Forge","Tungsten Carbide"))
    # print(get_market_price("The Forge", "Titanium Carbide"))
    # print(get_market_price("The Forge", "Terahertz Metamaterials"))
    # #print(get_market_price("The Forge", "Sylramic Fibers"))
    # print(get_market_price("The Forge", "Plasmonic Metamaterials"))
    # print(get_market_price("The Forge", "Photonic Metamaterials"))
    # #print(get_market_price("The Forge", "Phenolic Composites"))
    # print(get_market_price("The Forge", "Nonlinear Metamaterials"))
    # print(get_market_price("The Forge", "Nanotransistors"))
    # #print(get_market_price("The Forge", "Hypersynaptic Fibers"))
    # print(get_market_price("The Forge", "Fullerides"))
    # #print(get_market_price("The Forge", "Ferrogel"))
    # print(get_market_price("The Forge", "Fernite Carbide"))
    # print(get_market_price("The Forge", "Fermionic Condensates"))
    # print(get_market_price("The Forge", "Crystalline Carbonide"))

    # print(get_market_price("The Forge", "Ferrogel"))
    # print(get_market_price("The Forge", "Photonic Metamaterials"))
    # print(get_market_price("The Forge", "Hypersynaptic Fibers"))
    # print(get_market_price("The Forge", "Sylramic Fibers"))

    # print(get_market_price("The Forge", "Paladin"))
    # print(get_market_price("The Forge", "Plasmonic Metamaterials"))
    # print(get_market_price("The Forge", "Nonlinear Metamaterials"))

    # reaction_cost('Fernite Carbide', 500, "The Forge", "Esoteria")
    # reaction_cost('Hypersynaptic Fibers', 300, "The Forge", "Esoteria")
    # print(get_market_price("The Forge", "Tungsten Carbide")99999)
    '''reaction_cost('Tungsten Carbide', 300, "The Forge", "Esoteria")
    reaction_cost('Titanium Carbide', 300, "The Forge", "Esoteria")
    reaction_cost('Crystalline Carbonide', 300, "The Forge", "Esoteria")
    
    reaction_cost('Phenolic Composites', 300, "The Forge", "Esoteria")
    reaction_cost('Fermionic Condensates', 200, "The Forge", "Esoteria")
    reaction_cost('Terahertz Metamaterials', 200, "The Forge", "Esoteria")
    reaction_cost('Plasmonic Metamaterials', 200, "The Forge", "Esoteria")
    reaction_cost('Nonlinear Metamaterials', 200, "The Forge", "Esoteria")
    reaction_cost('Photonic Metamaterials', 200, "The Forge", "Esoteria")
    reaction_cost('Phenolic Composites', 300, "The Forge", "Esoteria")
    reaction_cost('Nanotransistors', 200, "The Forge", "Esoteria")
    reaction_cost('Hypersynaptic Fibers', 200, "The Forge", "Esoteria")
    reaction_cost('Fullerides', 250, "The Forge", "Esoteria")
    '''

    # reaction_cost('Nanotransistors', 100, "The Forge", "Esoteria")
    # reaction_cost('Hypersynaptic Fibers', 100, "The Forge", "Esoteria")
    # reaction_cost('Terahertz Metamaterials', 136, "The Forge", "Esoteria")

    # reaction_cost('Fullerides', 100, "The Forge", "Esoteria")

    # reaction_cost('Titanium Carbide', 300, "The Forge", "Esoteria")
    # reaction_cost('Fullerides', 400, "The Forge", "Esoteria")
    # reaction_cost('Terahertz Metamaterials', 100, "The Forge", "Esoteria")

    # reaction_cost('Phenolic Composites', 200, "The Forge", "Esoteria")

    # reaction_cost('Photonic Metamaterials', 75, "The Forge", "Esoteria")
    # reaction_cost('Ferrogel', 75, "The Forge", "Esoteria")
    # reaction_cost('Nonlinear Metamaterials', 100, "The Forge", "Esoteria")
    # reaction_cost('Crystalline Carbonide', 200, "The Forge", "Esoteria")

    # reaction_cost('Tungsten Carbide', 200, "The Forge", "Esoteria")
    # reaction_cost('Sylramic Fibers', 200, "The Forge", "Esoteria")
    # reaction_cost('Titanium Carbide', 100, "The Forge", "Esoteria")
    # reaction_cost('Fermionic Condensates', 40, "The Forge", "Esoteria")
    # reaction_cost('Crystalline Carbonide', 200, "The Forge", "Esoteria")
    # reaction_cost('Plasmonic Metamaterials',50,"The Forge","Esoteria")
    # reaction_cost('Nonlinear Metamaterials', 50, "The Forge", "Esoteria")
    # reaction_cost('Photonic Metamaterials', 100, "The Forge", "Esoteria")
    # reaction_cost('Phenolic Composites', 100, "The Forge", "Esoteria")
    # reaction_cost('Fernite Carbide', 100, "The Forge", "Esoteria")
    # reaction_cost('Fermionic Condensates',25,'The Forge','Esoteria')
    # unload_blueprintsyaml()
    # print(str(get_reaction_output_quantity(str(46210))))
    # load_evedb("eve.db")
    # print(get_typeid("Hurricane"))
    # type_id_request = get_typeid("Griffin")
    #
    # reader = codecs.getreader("utf-8")
    # # pw = json.load(reader(req_esi("alliances/names/?alliance_ids=1000171,498125261&datasource=tranquility")))
    # pw = json.load(reader(
    #     req_esi("markets/10000002/orders/?order_type=sell&type_id=%s&datasource=tranquility" % (type_id_request))))
    # # pw = json.load(reader(req_esi("markets/10000002/orders/?order_type=sell&type_id=24702&datasource=tranquility")))
    # i = 0
    # # print(pw[0]["average_price"])
    # max_index = len(pw)
    #
    # remainder = ""
    #
    # print("Item Type \t\t\tPrice \t\t\tRemaining Items")
    # while i < max_index:
    #     type_id = pw[i]["type_id"]
    #     volume_total = pw[i]["volume_total"]
    #     price = pw[i]["price"]
    #     with open("eve_inv_types.etf", mode="r", encoding="utf-8") as sourcefile:
    #         for line in sourcefile:
    #             target = re.search(r'\d+', line).group()
    #             # print(target)
    #             # print(type_id)
    #             # typeid, itemname = line.split(None, 1)
    #             parts_k = line.split()
    #             typeid_k = parts_k[0]
    #             itemname_k = ' '.join(parts_k[1:])
    #             # print(itemname_k)
    #             if str(target) == str(type_id_request):
    #                 # print("A match - %s compared to %s and is %s" % (target, type_id,itemname_k))
    #                 print("%s \t\t\t%-15s \t\t\t%-10.5s \t\t\t%-10.8s mil isk" % (itemname_k, pw[i]["price"], pw[i]["volume_remain"],str(float(pw[i]["price"]) * float(pw[i]["volume_remain"] / 1000000))))
    #                 # print(remainder)
    #     # print(str(pw[i]["type_id"])+"\t\t\t"+str(pw[i]["volume_total"])+"\t\t\t"+str(pw[i]["price"]))
    #     i = i + 1


screen_lock = threading.Semaphore(value=1)
start_time = time.time()
main()
all(lock.acquire() for lock in locks)
print("***********************************************")
for i in moon_ingredients:
    print("%s %d" % (i, moon_ingredients[i]))
print("%s Mil ISK" % str(totalcost / 1E6))
print("%s seconds" % (time.time() - start_time))
