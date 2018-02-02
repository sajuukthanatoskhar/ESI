import codecs
import datetime
import json
import sqlite3
import time
import urllib.request
import os
# from ruamel.yaml import YAML
import threading

import math
import requests
import yaml
from multiprocessing import Pool
# locale.setlocale(locale.LC_ALL, "en_US")
# local.format("%d",1255000,grouping=True)
import authpython
import pythonserver
from operator import itemgetter
from collections import OrderedDict

# headers: {'Authorization': '{} {}'.format(token_type, access_token)}


def req_esi(request_esi):
    wp = urllib.request.urlopen("https://esi.tech.ccp.is/latest/" + request_esi)
    return wp


def req_fuzzwork(request):
    wp = urllib.request.urlopen("https://www.fuzzwork.co.uk/blueprint/api/blueprint.php?typeid=%s" % (request))
    return wp


def load_evedb(eve_db_file):
    conn = sqlite3.connect(eve_db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM invtypes")
    rows = cur.fetchall()
    file_write = codecs.open("eve_inv_types.etf", "w", "utf-8")
    for row in rows:
        outputfromsqlite = str(row[0]) + " " + str(row[2])
        print(outputfromsqlite)
        file_write.write(str(outputfromsqlite) + "\n")
    file_write.close()

"""
This gets the item_id from the *.etf listed
returns type_id as an integer value
"""
def get_typeid(name):
    with open("eve_inv_types.etf", mode="r", encoding="utf-8") as sourcefile:
        for line in sourcefile:
            # target = re.search(r'\d+', line).group()
            # print(target)
            # print(type_id)
            # typeid, itemname = line.split(None, 1)
            parts_k = line.split()
            type_id = parts_k[0]
            itemname_k = ' '.join(parts_k[1:])
            # print("%s %s %s"%(name,itemname_k,typeid_k))
            if str(name) == str(itemname_k):
                return type_id

'''
Gives the region_id
Input is region name
returns region_id as integer
'''
def get_region(name):
    with open("regions_constellations_systems.etf", mode="r", encoding="utf-8") as sourcefile:
        for line in sourcefile:
            # target = re.search(r'\d+', line).group()
            # print(target)
            # print(type_id)
            # typeid, itemname = line.split(None, 1)
            parts_k = line.split()
            region_id = parts_k[0]
            itemname_k = ' '.join(parts_k[1:])
            # print("%s %s %s"%(name,itemname_k,typeid_k))
            if str(name) == str(itemname_k):
                return region_id

'''
Is reciprocal function of get_typeid
Gives the item name
Input is item input
returns item name as string
'''
def get_name(item_id_input):
    with open("eve_inv_types.etf", mode="r", encoding="utf-8") as sourcefile:
        for line in sourcefile:
            parts_k = line.split()
            item_name = ' '.join(parts_k[1:])
            item_id = parts_k[0]
            # print(str(int(name)))
            # print(str(int(itemname_k)))
            # print("%s %s %s"%(name,itemname_k,typeid_k))
            if int(item_id_input) == int(item_id):
                return item_name

"""
Returns the output from a blueprint
Doesn't deal with drugs very well (rip)
input is reaction id
returns output quantity as string
"""
def get_reaction_output_quantity(reaction_id):
    with open("blueprints.etf", mode="r", encoding="utf-8") as sourcefile:
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
def get_market_price(region, itemtype):
    type_id_request = get_typeid(itemtype)
    region_id = get_region(region)

    reader = codecs.getreader("utf-8")
    # pw = json.load(reader(req_esi("alliances/names/?alliance_ids=1000171,498125261&datasource=tranquility")))
    pw = json.load(reader(
        req_esi("markets/%s/orders/?order_type=sell&type_id=%s&datasource=tranquility" % (region_id, type_id_request))))
    # pw = json.load(reader(req_esi("markets/10000002/orders/?order_type=sell&type_id=24702&datasource=tranquility")))

    ordered_list = print_ordered_JSON(pw, type_id_request, region_id, region, itemtype)
    ordered_list_index_total = len(ordered_list)

    spread = int(round(ordered_list_index_total / 10, 0) * 2)
    if spread is 0:
        spread = 1
    ordercount = 0
    totalcost = 0
    for i in range(0, spread):
        totalcost = totalcost + ordered_list[i].cost * ordered_list[i].volumeremain
        ordercount = ordercount + ordered_list[i].volumeremain
    # print(totalcost)
    # print(ordercount)
    price = totalcost / ordercount
    # print("Price of "+itemtype + " in region: " + region)
    # print("Price = " + str(round(price,2)) + " (From " + str(ordercount) + " Orders)")

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


# (7:47:51 AM) relay: <Skyvyr> uhh, requests.put(url, headers={auththoken shit})

'''
Parses the json from the ordered market order from get_market_price(x,y,z,a)
Input is json_market_order_part
'''
def print_ordered_JSON(json_market_order_part, type_id_request, region_id, region, itemtype):
    i = 0
    marketorders = []
    # print("Price Lookup for %s (%s) in %s (%s)"%(itemtype,type_id_request,region,region_id))
    # print("Item Type \t\t\tPrice \t\t\tRemaining Items")
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

"""
Class defining a market order that is useful for gauging its cost, could've used a dict but I didn't like how much formatting and work is required whereas a class solves it easily enough for me
"""
class market_item():
    def __init__(self, itemtype, volumeremain, cost):
        self.itemtype = itemtype
        self.volumeremain = volumeremain
        self.cost = cost

"""
Get the blueprint details from fuzzworks
Example - https://www.fuzzwork.co.uk/blueprint/api/blueprint.php?typeid=22457
Input is the name of the blueprint, you have to include the ' Blueprint' or ' Reaction Formula', note the spaces
Output is a JSON blob for the blueprint
"""
def get_blueprint_details(name):
    reader = codecs.getreader("utf-8")
    type_id_request = get_typeid(name)
    js_wp = json.load(reader(req_fuzzwork(type_id_request)))
    return js_wp

"""
Getting Reaction Output using the blueprints.yaml
Deprecated but kept to show previous mistakes
"""
def get_reactionoutput(reaction_togetoutputof):
    with open("blueprints.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
        max_lines = len(config)
        print(config[int(reaction_togetoutputof)]["activities"]["reaction"]["products"][0]["quantity"])
        return config[int(reaction_togetoutputof)]["activities"]["reaction"]["products"][0]["quantity"]

"""
Calculates complex reaction expenditure and revenue based on the get_market_price(x,y) function algorithm
Input is the name of the complex reaction as a string, the number of runs of raw moon minerals, the marketregion where you are retrieving your prices from, homeregion has no functionality 
The results are printed out and the return is void
It prints out the resources needed for the runs and are formatted on the console in a way so that you can put them into multibuy
"""
def reaction_cost(complex_reaction, runs, marketregion, homeregion):
    if complex_reaction != "Fullerides":
        complexr = get_blueprint_details(complex_reaction + " Reaction Formula")
    else:
        complexr = get_blueprint_details(complex_reaction[:-1] + " Reaction Formula")
    if complex_reaction != "Fullerides":
        print(str(complex_reaction) + " Output Revenue (" + str(runs) + " runs of raw minerals): " + str(
            int(get_market_price(marketregion, complex_reaction)) * runs * 2 * int(get_reaction_output_quantity(
                get_typeid(complex_reaction + " Reaction Formula"))) / 1E6) + " M Isk  (Total Units = " + str(
            int(get_reaction_output_quantity(get_typeid(complex_reaction + " Reaction Formula"))) * runs * 2) + ")")
    else:
        print(str(complex_reaction) + " Output Revenue (" + str(runs) + " runs of raw minerals): " + str(
            int(get_market_price(marketregion, complex_reaction)) * runs * 2 * int(get_reaction_output_quantity(
                get_typeid(complex_reaction[:-1] + " Reaction Formula"))) / 1E6) + " M Isk  (Total Units = " + str(int(
            get_reaction_output_quantity(get_typeid(complex_reaction[:-1] + " Reaction Formula"))) * runs * 2) + ")")
    simple_reaction = []
    total_raw_input = 0

    for line in complexr['activityMaterials']['11']:
        # print(line['name'])
        tempprice = get_market_price(marketregion, line['name'])
        if 'Block' in line['name']:
            #print(line['name'] + " " + str(tempprice * 5 * runs * 2))
            total_raw_input = tempprice * 5 * runs * 2 + total_raw_input
        else:
            # print(line['name'] + " " + str(tempprice))
            simple_reaction.append(get_blueprint_details(line['name'] + " Reaction Formula"))
    i = 0

    for superline in simple_reaction:
        for line in superline['activityMaterials']['11']:
            tempprice = get_market_price(marketregion, line['name'])
            if 'Block' in line['name']:
                print(line['name'] + " " + str(runs * 100))  # + str(tempprice*5*runs))
                # We will deal with this later
                total_raw_input = total_raw_input + tempprice * 5 * runs
            else:
                print(line['name'] + " " + str(runs * 100))  # + " " + str(tempprice*100*runs))
                total_raw_input = total_raw_input + tempprice * 100 * runs
        i = i + 1
    # How many simple reactions?
    print("Input cost is = " + str(round(float(total_raw_input / 1E6), 2)) + " M Isk")

"""
Retrieves the different groups of fleets as described in the fleet_doc input as described in any of the doctrines folder's files
It compresses the lists so that nothing is duplicated
outputs are the fleet groups in group index and the group's ratios
"""
def get_fleet_groups(fleet_doc):

    #Compresses the duplicates of the roles of ships so you don't have duplicate shiptypes
    groups = list(set(fleet_doc.allowedshipsrole))
    group_ratio = []

    ratio_index_list = [i for i in range(len(fleet_doc.allowedshipsrole)) if not i == fleet_doc.allowedshipsrole.index(fleet_doc.allowedshipsrole[i])]
    # These find the indexes being used... I didn't write this code and is hard to read holy shit. TODO: Learn how to code in python
    ratioindex = [i for j, i in enumerate(fleet_doc.allowedshipsratio) if j not in ratio_index_list]
    groupindex = [i for j, i in enumerate(fleet_doc.allowedshipsrole) if j not in ratio_index_list]
    return groupindex,ratioindex

"""
Reads through the fleetjson (fleet json blob input) and checks against the fleet doctrine if the 
length is the number of members in the fleet.  It then add's the allowed ship's weight to the fleet group count.  
fleet doctrine input is a fleet_doctrine 

This function is very important and is hard to get your head around.  
"""
def process_fleet_comp(fleetjson, length, fleet_doctrine):
    i = 0
    fleet_groups,group_ratio = get_fleet_groups(fleet_doctrine)
    fleet_group_count = list(range(0,len(group_ratio)))
    i = 0
    while i < len(fleet_group_count):  #Resets fleet group count, probably can delete  #TODO: Please check!
        fleet_group_count[i] = 0
        i = i+1
    i = j = z =0
    while z < length:  #Loop through every member in the fleet to....
        checkshipname = get_name(fleetjson[z]["ship_type_id"])
        i = 0
        while i < len(fleet_doctrine.allowedships): #...check if they have one of the allowed ship types by looping through them and then...
            if checkshipname == fleet_doctrine.allowedships[i]:
               # print(checkshipname + " is allowed")
                j = 0
                while j<len(fleet_group_count): #...it's added to the right fleet group by checking their ship belongs to that group
                    if fleet_doctrine.allowedshipsrole[i] == fleet_groups[j]:
                        #add 1 to the group in fleet_group_count if the ship role matches
                        fleet_group_count[j] =fleet_group_count[j] +1  #todo: implement the weight where the '1' is in this line, it's really simple but I am lazy

                    j = j +1
                # add ship's weight to total group weight
            i=i+1
        z = z + 1
    return fleet_groups,group_ratio,fleet_group_count
'''
This is the main class for the fleet doctrine
It has (in order of appearance) the ships that are included in the doctrine, the allowed ships' ratios, their roles and their weighting in those roles (t1 logi should be rated half)
There is no major method
The static variables may be removed
'''
class doctrine:
    allowedships = []
    allowedshipsratio = []
    allowedshipsrole = []
    allowedshipsweight = []

    def __init__(self, fleettype):
        fleet_file = open('doctrines/' + fleettype, 'r')
        self.allowedships[:] = []
        self.allowedshipsratio[:] = []
        self.allowedshipsrole[:] = []
        self.allowedshipsweight[:] = []
        for lines in fleet_file:
            pw = lines.split(" ")  # [0] is access_token, #[1] is refresh
            self.allowedships.append(pw[0])
            self.allowedshipsratio.append(pw[1])
            self.allowedshipsrole.append(pw[2])
            self.allowedshipsweight.append(pw[3])

"""
Reading the tokens made from the pythonserver.py functions from a file (mostly it should be 'key.key')
Input is the file
The file is formatted into two columns, one line
output are the two tokens
"""
def read_tokens(file):
    keys_file = open(file, "r")
    access_token = refresh_token = 0
    for lines in keys_file:
        pw = lines.split(" ")  # [0] is access_token, #[1] is refresh
        access_token = pw[0] #First column
        refresh_token = pw[1] #Second Column
    print(authpython.refresh('1', refresh_token))
    return access_token, refresh_token

"""
Retrieves the Fleet ID that is being led by the FC
Input is the FC's name and their access_token (Required, needs a refreshed auth token)
Output is the fleet id
"""
def get_fleet_id(FleetCommanderName, access_token):
    reader = codecs.getreader("utf-8")
    id_json = json.load(reader(req_esi(
        'search/?categories=character&datasource=tranquility&language=en-us&search=%s&strict=false' % (
        FleetCommanderName))))
    FleetCommandID = str(id_json['character']).replace("[", "")
    FleetCommandID = str(FleetCommandID).replace("]", "")
    fleet_id_json = json.load(
        reader(req_esi('characters/%s/fleet/?datasource=tranquility&token=%s' % (FleetCommandID, access_token))))
    return fleet_id_json


"""
Main fleet function
Inputs are the fleet_file, the state of the fleet (further functionality is incoming) and the Fleet Commander who is boss of the fleet
Runs until the fleet FC leaves fleet, the cluster shuts down (for DT hopefully!) or the program is interrupted

!!Be warned when debugging, if authpython.refresh is not called every 1200 seconds after a set of tokens are made, this function cannot be run due to security requirements
Also, the tokens need to come from the Fleet Boss.!!
"""

def fleet_overwatch(Fleet_Type, state_of_fleet, FleetCommanderName):
    access= input('Do you need to run the server?')
    if access is 'a':
        pythonserver.run()
    ratio_scores = []
    # First we load the two keys from the keys.key file
    access_token, refresh_token = read_tokens("keys.key")
    reader = codecs.getreader("utf-8")
    fleet_id = get_fleet_id(FleetCommanderName, access_token)["fleet_id"]
    url = "https://esi.tech.ccp.is/latest/fleets/" + str(fleet_id) + "/?datasource=tranquility&token=" + str(
        access_token)
    while state_of_fleet == 1:
        time_timer = datetime.datetime.now().time()
        timeer = "The time is : " + str(time_timer) + "\n"
        fleetmembersjson = json.load(reader(req_esi(
            'fleets/' + str(fleet_id) + '/members/?datasource=tranquility&language=en-us&token=' + access_token)))
        fleetmemberslength = len(fleetmembersjson)
        print(fleetmemberslength)
        current_doctrine = doctrine(Fleet_Type)
        fleet_groups, group_ratio, fleet_group_count = process_fleet_comp(fleetmembersjson, fleetmemberslength, current_doctrine)
        #fleet_groups is for 'dps,logi,whatever'
        #group_ratio is the assigned values
        #ratiolength = len(fleet_group_count)
        ratio_scores = []
        scores = {}
        for i in range(0,len(fleet_group_count)):
            ratio_scores.append(float(fleet_group_count[i]/float(group_ratio[i])))
        minimum = max(ratio_scores)

        for i in range(0,len(fleet_group_count)):
            scores[fleet_groups[i]] = float(ratio_scores[i])

        #sorted(scores.items(), key=lambda x:float(x[1]))
        scores = OrderedDict(sorted(scores.items(),key=lambda x:float(x[1])))
        #x = {'heavy_tackle': 1.0, 'recon': 0.0, 'ewar': 3.0, 'interdictor': 1.0, 'dps': 2.75, 'tackle': 0.0, 'logistics': 2.0}
        #orderedx = OrderedDict(sorted(x.items(),key=lambda x:float(x[1])))
        #print(x)

#        for i in range(0,len(ratio_scores)):
#            for j in range(0,len(ratio_scores)):
#                if ratio_scores[j] < minimum:
#                    minimum = ratio_scores



        updatemessage = " "

        '''

        ratio_logi = 1
        ratio_dps = 3
        if ratio_logi>ratio_dps:
            a_logi_ships = no_logi/ratio_logi #anticipated logi ships
            if a_logi_ships*ratio_dps > no_dps:
                updatemessage = "Need more DPS!!!!"
            elif a_logi_ships*ratio_dps < no_dps:
                updatemessage = "Need more LOGISTICS!!!!"
        elif ratio_dps>ratio_logi :
            a_dps_ships = no_dps / ratio_dps #anticipated dps ships
            if a_dps_ships * ratio_logi > no_logi:
                updatemessage = "Need more LOGISTICS!!!!"
            elif a_dps_ships * ratio_logi < no_logi:
                updatemessage = "Need more DPS!!!!"
            else:
                if no_logi is 0 and no_dps is 0:
                    updatemessage = "Fleet is fucked, no one is in doctrine ships"
                else:
                    updatemessage = "Ratio is met, fleet is perfectly ratio'd"

        '''
        # while i < fleetmemberslength:
        #    timeer = "%s  Character %s has ship type  %s\n"%(timeer,fleetmembersjson[i]["character_id"],get_name(fleetmembersjson[i]["ship_type_id"]))
        #    i = i+1
        timeer = "\n" + updatemessage
        timeer = timeer + "\n****DOCTRINE SHIPS NEEDED****\n"
        for keys in scores.items():
            timeer = timeer + keys[0] + ">"
        timeer = timeer+ "else\n"

        #for i in range(0,len(fleet_groups)):
            #timeer = timeer + " Fleet Group ratioscore/number (" + str(fleet_groups[i]) + ") :" + str(ratio_scores[i]) + "("+str(fleet_group_count[i]) + ")\n"



        """status_put =requests.put(url, data=json.dumps(
            {
                'fleet_id': fleet_id,'new_settings': {"motd": "string"},}))"""
        status_put = requests.put(url, json.dumps({'fleet_id': fleet_id, 'motd': timeer}))

        # for lines in fleetmembersjson['character_id']:
        #   print(str(fleetmembersjson['character_id'][lines]))

        time.sleep(2)
        print(authpython.refresh('1', refresh_token))
        print(status_put)
        del(current_doctrine)
        del(scores)
    return


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
        'search/?categories=inventorytype&datasource=tranquility&language=en-us&search=%s&strict=true' % (name))))
    print(ship_id["inventorytype"][0])
    return ship_id["inventorytype"][0]

"""
Reads the blueprints.yaml file and translates it into a simpler file that states the name of the blueprint nad its output quantity
Not yet implemented for drugs
"""
def unload_blueprintsyaml():
    with open("blueprints.yaml", 'r') as stream:
        file_write = codecs.open("blueprints.etf", "w", "utf-8")
        config = yaml.safe_load(stream)
        max_lines = len(config)
        # i = 0

        for line in config:
            # print(config[line].items())

            if "reaction" not in str(config[line].items()):
                print("Continued : " + str(line))
                continue
            else:
                file_write.write(str(line) + " " + str(
                    config[int(line)]["activities"]["reaction"]["products"][0]["quantity"]) + "\n")
            # print(config[int(line)]["activities"]["reaction"]["products"][0]["quantity"])
            # outputfromsqlite = str(config[681]['activities']['manufacturing']['products'][0]['quantity'])
            # file_write.write(str(outputfromsqlite) + "")
        # print(outputfromsqlite)
        # print(line)

        # i = i+1
        file_write.close()


# + str(config[i]["activities"]["reaction"]["products"][0])


"""
Creates a database using the file name as input.  If the table in the database exists, it won't be modified
"""
def create_DB(db_file_name):
    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS evestuff(id INTEGER, name varchar[200])")
    with open("eve_inv_types.etf", mode="r", encoding="utf-8") as sourcefile:
        for line in sourcefile:
            parts_k = line.split()
            parts_k = (parts_k[0], ' '.join(parts_k[1:]))
            c.execute('insert into evestuff values (?,?)', (int(parts_k[0]), str(parts_k[1])))
    conn.commit()
    return [c, conn]


"""
Experimental Function using sqlite
Not implemented
Input is ship id and database connection (not database itself and is the 'conn' variable output from create_db)
"""
def get_shipname_from_db(name, db):
    db.execute('select id,name from evestuff WHERE id="%s"' % name)
    rows = db.fetchall()
    for row in rows:
        print(row[1])
    return row[1]

"""
Experimental Function using threading
Not implemented
"""
def multi_stuff():
    conn = sqlite3.connect('evetype.db')
    c = conn.cursor()
    # get_shipname_from_db(getshiptypeid('Sabre'),c)
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

"""
Checks if the file exists
"""
def check_file(file):
        if os.path.exists(file):
            #print(str(file + " Exists"))
            return 1
        else:
            #print(str(file + " Does not exists"))
            return 0


"""
In this function I want to read materials 
First, we take stuff from fuzzworks and dump it into a file, this is done outside the program for now
Secondly, we read the contents of that file line by line
    In each line, we will need to get the name of the complex material and the number of runs it needs to be done (runs needs to be ceil-rounded)
    These runs and materials will then be fed into reaction_cost()
"""
def get_number_of_runs_for_build(market_hub,alliance_home_region,file):

    if check_file(file):
        with open(file,mode="r") as file_to_read:
            for line in file_to_read:
                parts_k = line.split()

                materialname = str(' '.join(parts_k[1:]))
                #print(type(materialname))
                materialquantity = parts_k[0]
                #print(str(materialname))

                #complex_reaction_id = get_complex_material_reaction_id(materialname)["typeid"] #forgotten how to retrieve dictionary stuff as i haven't seen this code for a month
                #print(get_reaction_output_quantity(get_typeid(get_complex_material_reaction_name(materialname))))
                runs_required = math.ceil(float(materialquantity)/(2*float(get_reaction_output_quantity(get_typeid(get_complex_material_reaction_name(materialname)))))) #It is correct OH NO IT ISN"T
                #print(str(runs_required))
                #asdfasdg
                reaction_cost(materialname,runs_required,market_hub,alliance_home_region)
        with open(file, mode="r") as file_to_read:
            for line in file_to_read:
                parts_k = line.split()

                materialname = str(' '.join(parts_k[1:]))
                #print(type(materialname))
                materialquantity = parts_k[0]
                #print(str(materialname))

                #complex_reaction_id = get_complex_material_reaction_id(materialname)["typeid"] #forgotten how to retrieve dictionary stuff as i haven't seen this code for a month
                #print(get_reaction_output_quantity(get_typeid(get_complex_material_reaction_name(materialname))))
                runs_required = math.ceil(float(materialquantity)/(2*float(get_reaction_output_quantity(get_typeid(get_complex_material_reaction_name(materialname))))))
                print(materialname + " " + str(runs_required))
    else:
        print("Error: " + file + " does not exist")


def get_complex_material_reaction_name(complex_reaction):
    #print(complex_reaction)
    if complex_reaction != "Fullerides":
        complexr = complex_reaction + " Reaction Formula"
    else:
        complexr = complex_reaction[:-1] + " Reaction Formula"
    return complexr
"""
The Main function
There is a lot of random stuff commented out here as I tend to uncomment them for various uses
"""
def main():
    get_number_of_runs_for_build("The Forge","Esoteria","outputdump.txt")
    #multi_stuff()
    #unload_blueprintsyaml()
    #load_evedb("eve.db")
    #fleet_overwatch("harpy", 1, 'sajuukthanatoskhar')
    #print(get_market_price("The Forge","Plasmonic Metamaterials"))
    #print(get_market_price("The Forge", "Ferrogel"))
    #print(get_market_price("The Forge", "Photonic Metamaterials"))
    #print(get_market_price("The Forge", "Nanotransistors"))
    #print(get_market_price("The Forge", "Sylramic Fibers"))

    #print(get_market_price("The Forge", "Paladin"))
    #print(get_market_price("The Forge", "Plasmonic Metamaterials"))
    #print(get_market_price("The Forge", "Nonlinear Metamaterials"))

    #print(get_market_price("The Forge", "Tungsten Carbide"))
    #reaction_cost('Tungsten Carbide', 1048, "The Forge", "Esoteria")
    #reaction_cost('Nanotransistors', 100, "The Forge", "Esoteria")
    #reaction_cost('Hypersynaptic Fibers', 100, "The Forge", "Esoteria")
    #reaction_cost('Terahertz Metamaterials', 136, "The Forge", "Esoteria")
    #reaction_cost('Nanotransistors', 25, "The Forge", "Esoteria")
    #reaction_cost('Hypersynaptic Fibers', 18, "The Forge", "Esoteria")
    #reaction_cost('Fullerides', 342, "The Forge", "Esoteria")
    #reaction_cost('Fullerides', 100, "The Forge", "Esoteria")

    #reaction_cost('Fernite Carbide', 200, "The Forge", "Esoteria")
    #reaction_cost('Terahertz Metamaterials', 100, "The Forge", "Esoteria")
    #reaction_cost('Plasmonic Metamaterials', 100, "The Forge", "Esoteria")
    #reaction_cost('Nonlinear Metamaterials', 100, "The Forge", "Esoteria")
    #reaction_cost('Phenolic Composites', 200, "The Forge", "Esoteria")

    #reaction_cost('Photonic Metamaterials', 75, "The Forge", "Esoteria")
    #reaction_cost('Ferrogel', 75, "The Forge", "Esoteria")
    #reaction_cost('Nonlinear Metamaterials', 100, "The Forge", "Esoteria")
    #reaction_cost('Crystalline Carbonide', 200, "The Forge", "Esoteria")

    #reaction_cost('Tungsten Carbide', 200, "The Forge", "Esoteria")
    #reaction_cost('Sylramic Fibers', 200, "The Forge", "Esoteria")
    #reaction_cost('Titanium Carbide', 100, "The Forge", "Esoteria")
    #reaction_cost('Fermionic Condensates', 40, "The Forge", "Esoteria")
    #reaction_cost('Crystalline Carbonide', 200, "The Forge", "Esoteria")
    #reaction_cost('Plasmonic Metamaterials',50,"The Forge","Esoteria")
    #reaction_cost('Nonlinear Metamaterials', 50, "The Forge", "Esoteria")
    #reaction_cost('Fernite Carbide', 200, "The Forge", "Esoteria")
    #reaction_cost('Phenolic Composites', 100, "The Forge", "Esoteria")
    #reaction_cost('Fernite Carbide', 100, "The Forge", "Esoteria")
    #reaction_cost('Fermionic Condensates',25,'The Forge','Esoteria')
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


start_time = time.time()
main()
print("%s seconds" % (time.time() - start_time))
