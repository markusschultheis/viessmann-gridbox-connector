# Viessmann Gridbox Connector Fork 
**This is a fork of unl0ck's repo viessmann-gridbox-connector **

a GridboxConnector Lib to fetch your Data from the Cloud.
It is using the same Rest-API like the Dashboard and the App.

It requests the data from the portal end stores them on a local file.
Store the file on your (public) webserver directory to give access to other applications.

For example you can use Grafana and the CSV plugin to fetch the data from your server.
Choose the query option - delimiter: Semicolon, Format - Field 1: String
Transform the data for your needs.

## Setup first
edit the email and password in the config.json. 
You need your Login Data from the App or from https://mygridbox.viessmann.com/login

## How-To run
```script shell
pip install -r requirements.txt
python read_live_data.py
```

