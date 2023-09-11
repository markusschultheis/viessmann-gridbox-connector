import json
import requests
import os
import datetime
from influxdb import InfluxDBClient

# Opening JSON file and setting pwd
pwd = os.getcwd()
f = open(pwd+'/config.json')

date = str(int(datetime.datetime.now().timestamp()))
# returns JSON object as a dictionary
data = json.load(f)
f.close()

# InfluxDB-Konfiguration
host = 'localhost'  # Hostname oder IP-Adresse Ihres InfluxDB-Servers
port = 8086  # Port für InfluxDB, standardmäßig 8086
database = 'iobroker'  # Name Ihrer InfluxDB-Datenbank

# InfluxDB-Client initialisieren
client = InfluxDBClient(host=host, port=port, database=database)

class GridboxConnector:
    id_token = ""
    response_json = ""

    def __init__(self,config):
        self.login_url = config["urls"]["login"]
        self.login_body = config["login"]
        self.gateway_url = config["urls"]["gateways"]
        self.live_url = config["urls"]["live"]
        self.get_token()
        self.generate_header()
        self.get_gateway_id()
        self.get_response()

    def get_token(self):
        response = requests.post(self.login_url, self.login_body)
        response_json = response.json()
        self.id_token = response_json["id_token"]

    def generate_header(self):
        self.headers = {"Authorization": "Bearer {}".format(self.id_token)}

    def get_gateway_id(self):
        response = requests.get(self.gateway_url,headers=self.headers)
        response_json = response.json()
        gateway = response_json[0]
        self.gateway_id = gateway["system"]["id"]

    def get_response(self):
        response = requests.get(self.live_url.format(self.gateway_id),headers=self.headers)
        response_json = response.json()
        self.response_json = response_json
        measurement = "PV_Live_Monitoring"
        tags = {}  # Tags, falls benötigt
        fields = {
            "power": int(response_json["batteries"][0]["power"]),
            "remainingCharge": int(response_json["batteries"][0]["remainingCharge"]),  # Felder aus der JSON-Antwort
            "stateOfCharge": float(response_json["batteries"][0]["stateOfCharge"]),
            "consumption": int(response_json["consumption"]),
            "directConsumption": int(response_json['directConsumption']),
            "directConsumptionHousehold": int(response_json["directConsumptionHousehold"]),
            "directConsumptionRate": int(response_json["directConsumptionRate"]),
            "grid": int(response_json["grid"]),
            "measuredAt": response_json["measuredAt"],
            "photovoltaic": int(response_json["photovoltaic"]),
            "production": int(response_json['production']),
            "selfConsumption": int(response_json['selfConsumption']),
            "selfConsumptionRate": int(response_json["selfConsumptionRate"]),
            "selfSufficiencyRate": float(response_json["selfSufficiencyRate"]),
            "selfSupply": int(response_json["selfSupply"]),
            "totalConsumption": int(response_json["totalConsumption"])
        }
      
        # InfluxDB-Datenpunkt erstellen
        data_point = [
            {
                "measurement": measurement,
                "tags": tags,
                "time": response_json["measuredAt"],
                "fields": fields
            }
        ]

        # Daten in InfluxDB schreiben
        client.write_points(data_point)
        #control the output data
        #print(fields)


GridboxConnector(data)
