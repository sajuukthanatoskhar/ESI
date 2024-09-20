#from market_list import req_esi
import urllib.request
import json
import codecs
import sqlite3
import sys
import re
import requests
import locale

def req_esi(request_esi):
    wp = urllib.request.urlopen("https://esi.tech.ccp.is/latest/" + request_esi)
    return wp


#State - Identify Sajuuk's id
#Get Sajuuk's Id
character = "sajuukthanatoskhar"
character_id = req_esi("search/?categories=character&datasource=tranquility&language=en-us&search="+character+"&strict=false")

#Get Current Fleet
#Sajuuk's ID 120205143




#State - Fleet Number Feedback
while True:
    a = 5
