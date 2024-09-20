
import csv
from typing import List
from esi_formats import esi_classes

import requests
import pathlib

pi_types_csv_path = "../planetaryinteraction/planetSchematicsTypeMap.csv"

def get_pi_csv_fuzzworks():
    """
    Gets the csv file from fuzzworks containing the data for the
    :return:
    """
    path = pathlib.Path(pi_types_csv_path)
    if path.is_file():
        return csv.reader(path)
    else:
        req_url = "https://www.fuzzwork.co.uk/dump/latest/planetSchematicsTypeMap.csv"
        r = requests.get(req_url, allow_redirects=True)
        csvtext = r.content.decode().split('\r')
        with open(path, 'w') as csvfile:
            csvfile.writelines(csvtext)




class pi_schematic:
    def __init__(self, ID: int):
        self.ID = ID
        self.pi_name = None
        self.inputs : List[PI_Schematic_member] = []
        self.output : List[PI_Schematic_member] = []


    def add_outputinput(self, line:list):
        input_output_redirect = self.output
        if line[0] == self.ID:
            line.pop(0)

            if line[2]:
                input_output_redirect = self.inputs
            input_output_redirect.append(PI_Schematic_member(*line))

    def get_name(self):
        if self.output:
            self.pi_name = self.output[0].name

class PI_Schematic_member:
    def __init__(self, typeID, quantity, isInput):
        self.name = None
        self.typeID = int(typeID)
        self.quantity = int(quantity)
        self.isInput = bool(isInput)

    def get_name(self, api_link : esi_classes.char_api_swagger_collection):
        self.name = api_link.get_id_via_api_comm(self.typeID)









if __name__ == '__main__':
    with get_pi_csv_fuzzworks() as csvfile:
        pass