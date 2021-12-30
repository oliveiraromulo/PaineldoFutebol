import requests
import json

url = "https://api-football-v1.p.rapidapi.com/v3/teams"

querystring = {"country":"Brazil"}

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "2014cc0ea1msh118aa5cb2f5f7a4p16f82cjsn0f523407fcf8"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_data = json.loads(response_test.text)

with open('team_ids.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4, ensure_ascii=False)
