import requests
import json

url = "https://api-football-v1.p.rapidapi.com/v3/players"

# Fazer o passo de paginação pelo total de páginas
querystring = {"league":"71","season":"2020","page":"2"}

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "2014cc0ea1msh118aa5cb2f5f7a4p16f82cjsn0f523407fcf8"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_data = json.loads(response.text)

with open('player_stats_per_team_id.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=4)
