import requests
import json
import config

url = "https://api-football-v1.p.rapidapi.com/v3/teams"

querystring = {"country":"Brazil"}

headers = {
    'x-rapidapi-host': "##############",
    'x-rapidapi-key': "##############"
    }
    
response = requests.request("GET", url, headers=headers, params=querystring)

json_data = json.loads(response_test.text)

with open('team_ids.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4, ensure_ascii=False)
