import requests
import json
#import argparse
#import config

import psycopg as pg

file = open('config.json')

args = json.load(file)

url = "https://api-football-v1.p.rapidapi.com/v3/players"

# Fazer o passo de paginação pelo total de páginas
querystring = {"league":"71","season":"2023","page":"1"}

headers = {
    'x-rapidapi-host': args['x-rapidapi-host'],
    'x-rapidapi-key': args['x-rapidapi-key']
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_data = json.loads(response.text)

with open('player_stats_per_team_id.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=4)
