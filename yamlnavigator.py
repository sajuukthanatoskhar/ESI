import urllib.request
import json
import codecs
import sqlite3
import sys
import re
import locale
import yaml

def nav():
    with open("regions_constellations_systems.yaml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            #print(len(config))
            #print("%s %s"%(config[0]["itemName"],config[0]["ItemID"]))
            max_lines = len(config)
            i=0
            while i<max_lines:
                print("%s %s\n"%(config[i]["itemName"],config[i]["itemID"]))
                i = i + 1
        except yaml.YAMLError as exc:
            print(exc)

def main():

    with open("regions_constellations_systems.yaml", 'r') as stream:
        file_write = codecs.open("regions_constellations_systems.etf", "w", "utf-8")
        config = yaml.safe_load(stream)
        max_lines = len(config)
        i = 0
        while i < max_lines:
            outputfromsqlite = str(config[i]["itemID"])+" "+str(config[i]["itemName"])
            print(outputfromsqlite)
            file_write.write(str(outputfromsqlite) + "\n")
            i = i+1
        file_write.close()



main()