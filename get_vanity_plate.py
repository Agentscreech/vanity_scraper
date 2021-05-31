#!python3

import requests

STATES = [
    "AK",
    "AL",
    "AR",
    "AZ",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MD",
    "ME",
    "MI",
    "MN",
    "MO",
    "MS",
    "MT",
    "NC",
    "ND",
    "NE",
    "NH",
    "NJ",
    "NM",
    "NV",
    "NY",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "VT",
    "WA",
    "WY",
    "WI",
    "WV"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5 --compressed ",
    "Content-Type": "application/json",
    "Origin": "https://www.vroom.com",
    "Connection": "keep-alive",
    "Referer": "https://www.vroom.com/sell"
}


def get_vin(plate, state):
    url = "https://www.vroom.com/api/appraisal/license-to-vin"
    payload = {"licensePlate": plate, "state": state}
    r = requests.post(url, headers=HEADERS, json=payload)
    if r.status_code == 200:
        r = r.json()
        return r["data"]["vehicles"][0]["vin"]
    return False


def decode_vin(vin):
    url = f"https://www.vroom.com/api/appraisal/decode-vin/{vin}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        r = r.json()
        return r["data"]["decodeVIN"]
    return False

def parse_data(data):
    year = data["basicData"]["year"]
    make = data["basicData"]["make"]
    model = data["basicData"]["model"]
    trims = ""
    if data["trimData"]["trims"]:
        trims_list = [ x["long_description"] for x in data["trimData"]["trims"]]
        trims = ', '.join(trims_list)
    if make == "":
        return False
    return f"{year} {make} {model} {trims}"

plate = input("Plate to lookup: ")
plate = plate.upper()
for state in STATES:
    vin = get_vin(plate, state)
    if vin and len(vin) == 17:
        data = decode_vin(vin)
        if data:
            s = parse_data(data)
            if s:
                print(f"{plate} in {state} has a VIN of {vin} and is a {s}")
