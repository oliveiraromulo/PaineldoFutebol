import requests
import json

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "2014cc0ea1msh118aa5cb2f5f7a4p16f82cjsn0f523407fcf8"
    }

response = requests.request("GET", url, headers=headers)

json_data = json.loads(response.text)

with open('league_ids.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=4)
