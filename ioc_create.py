import json
import os
from falconpy import IOC

# Hardcoded credentials
credentials = {
    'client_id': "replace with your id",
    'client_secret': "replace with your password"
}

def connect_api(creds: dict):
    falcon_api = IOC(creds=creds, base_url="https://api.us-2.crowdstrike.com")
    return falcon_api

# Specify the path to your indicator JSON file
indicator_file_path = "ioc.json"

falcon = connect_api(credentials)

if not os.path.exists(indicator_file_path):
    raise SystemExit("Unable to load indicator file.")

with open(indicator_file_path, "r", encoding="utf-8") as indicator_file:
    indicator_data = json.load(indicator_file)

if "value" in indicator_data and isinstance(indicator_data["value"], list):
    for ip_address in indicator_data["value"]:
        indicator_entry = {
            "source": indicator_data["source"],
            "action": indicator_data["action"],
            "expiration": indicator_data["expiration"],
            "description": indicator_data["description"],
            "type": indicator_data["type"],
            "value": ip_address,
            "platforms": indicator_data["platforms"],
            "severity": indicator_data["severity"],
            "applied_globally": indicator_data["applied_globally"]
        }

        response = falcon.indicator_create(**indicator_entry)
        print(response)
else:
    print("The 'value' field in the indicator file is not a list.")
