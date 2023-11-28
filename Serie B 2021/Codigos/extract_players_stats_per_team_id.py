import requests
import json
import config

url = "https://api-football-v1.p.rapidapi.com/v3/players"

# Fazer o passo de paginação pelo total de páginas
querystring = {"league":"71","season":"2020","page":"2"}

headers = {
    'x-rapidapi-host': "##############",
    'x-rapidapi-key': "##############"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_data = json.loads(response.text)

with open('player_stats_per_team_id.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=4)
