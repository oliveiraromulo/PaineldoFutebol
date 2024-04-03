import requests
import json
#import argparse
#import config

import psycopg as pg

file = open('config.json')

args = json.load(file)

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

# Deve ser parametrizado de acordo com a necessidade. Ou processa rodada ou processa temporada inteira.
querystring = {
#"date":"2021-11-16",
"league":"71",
"season":"2023"}

headers = {
    'x-rapidapi-host': args['x-rapidapi-host'],
    'x-rapidapi-key': args['x-rapidapi-key']
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_data = json.loads(response.text)

#with open('fixture_ids.json', 'w') as json_file:
#    json.dump(json_json_data, json_file, indent=4, ensure_ascii=False)

results = []

for i in range(len(json_data['response'])):
    fixture_id = json_data['response'][i]['fixture']['id']
    fixture_referee = json_data['response'][i]['fixture']['referee']
    fixture_timezone = json_data['response'][i]['fixture']['timezone']
    fixture_date = json_data['response'][i]['fixture']['date']
    fixture_timestamp = json_data['response'][i]['fixture']['timestamp']
    fixture_period_first = json_data['response'][i]['fixture']['periods']['first']
    fixture_period_second = json_data['response'][i]['fixture']['periods']['second']
    fixture_venue_id = json_data['response'][i]['fixture']['venue']["id"]
    fixture_venue_name = json_data['response'][i]['fixture']['venue']["name"]
    fixture_venue_city = json_data['response'][i]['fixture']['venue']["city"]
    fixture_status_long = json_data['response'][i]['fixture']['status']["long"]
    fixture_status_short = json_data['response'][i]['fixture']['status']["short"]
    fixture_status_elapsed = json_data['response'][i]['fixture']['status']["elapsed"]

    league_id = json_data['response'][i]['league']['id']
    league_name = json_data['response'][i]['league']['name']
    league_country = json_data['response'][i]['league']['country']
    league_logo = json_data['response'][i]['league']['logo']
    league_flag = json_data['response'][i]['league']['flag']
    league_season = json_data['response'][i]['league']['season']
    league_round = json_data['response'][i]['league']['round']

    teams_home_id = json_data['response'][i]['teams']['home']['id']
    teams_home_name = json_data['response'][i]['teams']['home']['name']
    teams_home_logo = json_data['response'][i]['teams']['home']['logo']
    teams_home_winner = json_data['response'][i]['teams']['home']['winner']
    teams_away_id = json_data['response'][i]['teams']['away']['id']
    teams_away_name = json_data['response'][i]['teams']['away']['name']
    teams_away_logo = json_data['response'][i]['teams']['away']['logo']
    teams_away_winner = json_data['response'][i]['teams']['away']['winner']

    goals_home =  json_data['response'][i]['goals']['home']
    goals_away = json_data['response'][i]['goals']['away']

    score_halftime_home = json_data['response'][i]['score']['halftime']['home']
    score_halftime_away = json_data['response'][i]['score']['halftime']['away']
    score_fulltime_home = json_data['response'][i]['score']['fulltime']['home']
    score_fulltime_away = json_data['response'][i]['score']['fulltime']['away']
    score_extratime_home = json_data['response'][i]['score']['extratime']['home']
    score_extratime_away = json_data['response'][i]['score']['extratime']['away']
    score_penalty_home = json_data['response'][i]['score']['penalty']['home']
    score_penalty_away = json_data['response'][i]['score']['penalty']['away']

    results.append((
    fixture_id,
    fixture_referee,
    fixture_timezone,
    fixture_date,
    fixture_timestamp,
    fixture_period_first,
    fixture_period_second,
    fixture_venue_id,
    fixture_venue_name,
    fixture_venue_city,
    fixture_status_long,
    fixture_status_short,
    fixture_status_elapsed,
    league_id,
    league_name,
    league_country,
    league_logo,
    league_flag,
    league_season,
    league_round,
    teams_home_id,
    teams_home_name,
    teams_home_logo,
    teams_home_winner,
    teams_away_id,
    teams_away_name,
    teams_away_logo,
    teams_away_winner,
    goals_home,
    goals_away,
    score_halftime_home,
    score_halftime_away,
    score_fulltime_home,
    score_fulltime_away,
    score_extratime_home,
    score_extratime_away,
    score_penalty_home,
    score_penalty_away))



#print(results)

insert_query = """INSERT INTO usr_landing.fixtures
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s)"""

conn = pg.connect(args['url_conn'])
cur = conn.cursor()

cur.executemany(insert_query, results)

conn.commit()