import codecs
import datetime
import json
import time
from collections import OrderedDict

import requests

from eve_esi_framwork import authpython, pythonserver
from MarketWatcher.market_and_fleet import read_tokens, req_esi, process_fleet_comp
"""
Main fleet function
Inputs are the fleet_file, the state of the fleet (further functionality is incoming) and the Fleet Commander who is boss of the fleet
Runs until the fleet FC leaves fleet, the cluster shuts down (for DT hopefully!) or the program is interrupted

!!Be warned when debugging, if authpython.refresh is not called every 1200 seconds after a set of tokens are made, this function cannot be run due to security requirements
Also, the tokens need to come from the Fleet Boss.!!
"""

def fleet_overwatch(fleet_type: str, state_of_fleet: int, fleet_commander_name: str):
    access = input('Do you need to run the server?')
    if access == 'a':
        pythonserver.run()
    ratio_scores = []
    # First we load the two keys from the keys.key file
    access_token, refresh_token = read_tokens("../configurations/keys.key")
    reader = codecs.getreader("utf-8")
    fleet_id = get_fleet_id(fleet_commander_name, access_token)["fleet_id"]
    url = "https://esi.tech.ccp.is/latest/fleets/" + str(fleet_id) + "/?datasource=tranquility&token=" + str(
        access_token)
    while state_of_fleet == 1:
        time_timer = datetime.datetime.now().time()
        # timeer = "The time is : " + str(time_timer) + "\n" # todo: deprecate
        fleetmembersjson = json.load(reader(req_esi(
            'fleets/' + str(fleet_id) + '/members/?datasource=tranquility&language=en-us&token=' + access_token)))
        fleetmemberslength = len(fleetmembersjson)
        print(fleetmemberslength)
        current_doctrine = doctrine(fleet_type)
        fleet_groups, group_ratio, fleet_group_count = process_fleet_comp(fleetmembersjson, fleetmemberslength,
                                                                          current_doctrine)
        # fleet_groups is for 'dps,logi,whatever'
        # group_ratio is the assigned values
        # ratiolength = len(fleet_group_count)
        ratio_scores = []
        scores = {}
        for i in range(0, len(fleet_group_count)):
            ratio_scores.append(float(fleet_group_count[i] / float(group_ratio[i])))
        minimum = max(ratio_scores)

        for i in range(0, len(fleet_group_count)):
            scores[fleet_groups[i]] = float(ratio_scores[i])

        # sorted(scores.items(), key=lambda x:float(x[1]))
        scores = OrderedDict(sorted(scores.items(), key=lambda x: float(x[1])))
        updatemessage = " "

        timeer = "\n" + updatemessage
        timeer = timeer + "\n****DOCTRINE SHIPS NEEDED****\n"
        for keys in scores.items():
            timeer = timeer + keys[0] + ">"
        timeer = timeer + "else\n"

        """status_put =requests.put(url, data=json.dumps(
            {
                'fleet_id': fleet_id,'new_settings': {"motd": "string"},}))"""

        status_put = requests.put(url, json.dumps({'fleet_id': fleet_id, 'motd': timeer}))
        time.sleep(2)
        print(authpython.refresh('1', refresh_token))
        print(status_put)
        del current_doctrine
        del scores


def get_fleet_id(FleetCommanderName: str, access_token: str):
    """
    Retrieves the Fleet ID that is being led by the FC
    Input is the FC's name and their access_token (Required, needs a refreshed auth token)
    Output is the fleet id
    """
    reader = codecs.getreader("utf-8")
    id_json = json.load(reader(req_esi(
        'search/?categories=character&datasource=tranquility&language=en-us&search=%s&strict=false' % (
            FleetCommanderName))))
    FleetCommandID = str(id_json['character']).replace("[", "")
    FleetCommandID = str(FleetCommandID).replace("]", "")
    fleet_id_json = json.load(
        reader(req_esi('characters/%s/fleet/?datasource=tranquility&token=%s' % (FleetCommandID, access_token))))
    return fleet_id_json


class doctrine:
    """
    This is the main class for the fleet doctrine
    It has (in order of appearance) the ships that are included in the doctrine, the allowed ships' ratios, their roles and their weighting in those roles (t1 logi should be rated half)
    There is no major method
    The static variables may be removed
    """
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
