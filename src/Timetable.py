import requests
import json





base_url = "https://hiplan.thi.de/webservice/production/index.php"



data = {
    "username": "jus5656",
    "passwd": "",
    "service": "session",
    "method": "open",
    "format": "json"
}

print data

response = requests.post(base_url,data=data)
if response.status_code is not 200:
    raise Exception("Error getting session-id")
data_response = response.json()['data']
session_id =  data_response[0]



