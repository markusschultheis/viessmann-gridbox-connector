import json
import requests
import os
import datetime

#Getting the actual path of your working dir and open the config file
pwd = os.getcwd()
file = open(pwd+'/config.json')

#Getting time and date as a timestamp for further use
# date = str(datetime.datetime.now())

# returns JSON object as a dictionary
data = json.load(file)
file.close() 

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
    
    def retrieve_live_data(self):
        response = requests.get(self.live_url.format(self.gateway_id),headers=self.headers)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
        else:
            self.get_token()
            self.generate_header()
            self.retrieve_live_data(self)

with open("gridbox_data.json", "a") as f:
    json.dump(GridboxConnector(data).response_json, f)
    f.write('\t')
    f.write('\n')
