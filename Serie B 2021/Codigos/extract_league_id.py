import requests
import json
#import argparse
#import config

import psycopg as pg

file = open('config.json')

args = json.load(file)

#print(d['x-rapidapi-host'])

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

headers = {
    'x-rapidapi-host': args['x-rapidapi-host'],
    'x-rapidapi-key': args['x-rapidapi-key']
    }

response = requests.request("GET", url, headers=headers)

json_data = json.loads(response.text)

with open('league_ids.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=4)

results = []

for i in range(len(json_data['response'])):
    print(json_data['response'][i]['country']["name"])
    print(json_data['response'][i]['league']["name"])
    print('Quantidade de temporadas: ', len(json_data['response'][i]['seasons']))

    #country_name = json_data['response'][i]['country']["name"]
    #league_name = json_data['response'][i]['league']["name"]
    #season_qtd = len(json_data['response'][i]['seasons'])


    league_id = json_data['response'][i]['league']["id"]
    league_name = json_data['response'][i]['league']["name"]
    league_type = json_data['response'][i]['league']["type"]
    league_logo = json_data['response'][i]['league']["logo"]
    country_name = json_data['response'][i]['country']["name"]
    country_code = json_data['response'][i]['country']["code"]
    country_flag = json_data['response'][i]['country']["flag"]
    season_qtd = len(json_data['response'][i]['seasons'])

    for j in range(1, season_qtd):
        season_year = json_data['response'][i]['seasons'][j]["year"]
        season_start = json_data['response'][i]['seasons'][j]["start"]
        season_end = json_data['response'][i]['seasons'][j]["end"]
        season_current = json_data['response'][i]['seasons'][j]["current"]
        season_coverage_fixtures_events = json_data['response'][i]['seasons'][j]["coverage"]["fixtures"]["events"]
        season_coverage_fixtures_lineups = json_data['response'][i]['seasons'][j]["coverage"]["fixtures"]["lineups"]
        season_coverage_fixtures_statistics_fixtures = json_data['response'][i]['seasons'][j]["coverage"]["fixtures"]["statistics_fixtures"]
        season_coverage_fixtures_statistics_players = json_data['response'][i]['seasons'][j]["coverage"]["fixtures"]["statistics_players"]
        season_coverage_stadings = json_data['response'][i]['seasons'][j]["coverage"]["standings"]
        season_coverage_players = json_data['response'][i]['seasons'][j]["coverage"]["players"]
        season_coverage_top_scorers = json_data['response'][i]['seasons'][j]["coverage"]["top_scorers"]
        season_coverage_top_assists = json_data['response'][i]['seasons'][j]["coverage"]["top_assists"]
        season_coverage_top_cards = json_data['response'][i]['seasons'][j]["coverage"]["top_cards"]
        season_coverage_injuries = json_data['response'][i]['seasons'][j]["coverage"]["injuries"]
        season_coverage_predictions = json_data['response'][i]['seasons'][j]["coverage"]["predictions"]
        season_coverage_odds = json_data['response'][i]['seasons'][j]["coverage"]["odds"]

    results.append((
        league_id, 
        league_name, 
        league_type, 
        league_logo, 
        country_name, 
        country_code,
        country_flag,
        season_year,
        season_start,
        season_end,
        season_current,
        season_coverage_fixtures_events,
        season_coverage_fixtures_lineups,
        season_coverage_fixtures_statistics_fixtures,
        season_coverage_fixtures_statistics_players,
        season_coverage_stadings,
        season_coverage_players,
        season_coverage_top_scorers,
        season_coverage_top_assists,
        season_coverage_top_cards,
        season_coverage_injuries,
        season_coverage_predictions,
        season_coverage_odds
        ))

#print(results)
#print(type(results))

insert_query = """INSERT INTO usr_landing.leagues
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

conn = pg.connect(args['url_conn'])
cur = conn.cursor()

cur.executemany(insert_query, results)

conn.commit()