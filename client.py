"""
    kayak-mobile-client

    A basic client for the Kayak mobile app's server API

    Follow the instructions at:

        http://www.shubhro.com/2014/12/18/reverse-engineering-kayak-mitmproxy/

    to learn your UUID and HASH with mitmproxy
"""

import sys
import json
import requests

# Replace the following two variables with your UUID and HASH
UUID = ""
HASH = ""

if not UUID:
    print "Please set up your UUID and HASH according to the instructions in the README"
    sys.exit()

origin_airport = raw_input("Departure airport code: ")
dest_airport = raw_input("Destination airport code: ")
departure_date = raw_input("Departure date (MM/DD/YY): ")

payload = {
    "action" : "registermobile",
    "uuid" : UUID,
    "hash" : HASH,
    "model" : "iPhone4,1",
    "appid" : "kayakfree",
    "os" : "8.1.1",
    "msgApiVersion" : "1",
    "as" : "0",
    "appdist" : "adhoc",
    "prefix" : ""
}
r = requests.get("https://www.kayak.com/k/authajax/", params=payload)

for line in r.text.split("\n"):
    if "sid" not in line:
        continue
    sid = line.split("=")[1]

payload = {
    "cabin" : "e",
    "travelers" : "1",
    "origin1" : origin_airport,
    "nearbyO1" : "false",
    "destination1" : dest_airport,
    "nearbyD1" : "false",
    "depart_date1" : departure_date,
    "depart_time1" : "a",
    "depart_date_flex1" : "exact",
    "_sid_" : sid
}
r = requests.get("https://www.kayak.com/api/search/V8/flight/start", params=payload)
searchid = json.loads(r.text)["searchid"]

payload = {
    "currency" : "USD",
    "searchid" : searchid,
    "c" : "2000",
    "providerData" : "true",
    "nc" : "40",
    "includeopaques" : "true",
    "showAirlineLogos" : "true",
    "_sid_" : sid
}
r = requests.get("https://www.kayak.com/api/search/V8/flight/poll", params=payload)

print "Browse here to view the response JSON: "
print r.url
