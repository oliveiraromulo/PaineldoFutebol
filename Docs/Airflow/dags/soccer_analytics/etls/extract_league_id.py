import requests
import json
from datetime import datetime

import psycopg as pg # pyright: ignore[reportMissingImports]

'''
    Reading configuration file and setting headers for API requests
'''
file = open('/opt/airflow/dags/soccer_analytics/config.json')
args = json.load(file)
headers = {
    'x-rapidapi-host': args['x-rapidapi-host'],
    'x-rapidapi-key': args['x-rapidapi-key']
    }


url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

extract_league_id = [1, 71]

def extract_league_ids(url : str, headers : dict) -> list:
    results = []
    
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)

    for league in json_data['response']:
        if league["league"]["id"] in extract_league_id:
            txt = f"ID: {league["league"]["id"]} - Nome: {league["country"]["name"]} - {league["league"]["name"]} | Temporadas: {len(league["seasons"])}\n"
            print(txt)

            league_id = league["league"]["id"]
            league_name = league["league"]["name"]
            league_type = league["league"]["type"]
            league_logo = league["league"]["logo"]
            country_name = league["country"]["name"]
            country_code = league["country"]["code"]
            country_flag = league["country"]["flag"]
            season_qtd = len(league["seasons"])

            for j in range(1, season_qtd):
                season_year = league["seasons"][j]["year"]
                season_start = league["seasons"][j]["start"]
                season_end = league["seasons"][j]["end"]
                season_current = league["seasons"][j]["current"]
                season_coverage_fixtures_events = league["seasons"][j]["coverage"]["fixtures"]["events"]
                season_coverage_fixtures_lineups = league["seasons"][j]["coverage"]["fixtures"]["lineups"]
                season_coverage_fixtures_statistics_fixtures = league["seasons"][j]["coverage"]["fixtures"]["statistics_fixtures"]
                season_coverage_fixtures_statistics_players = league["seasons"][j]["coverage"]["fixtures"]["statistics_players"]
                season_coverage_stadings = league["seasons"][j]["coverage"]["standings"]
                season_coverage_players = league["seasons"][j]["coverage"]["players"]
                season_coverage_top_scorers = league["seasons"][j]["coverage"]["top_scorers"]
                season_coverage_top_assists = league["seasons"][j]["coverage"]["top_assists"]
                season_coverage_top_cards = league["seasons"][j]["coverage"]["top_cards"]
                season_coverage_injuries = league["seasons"][j]["coverage"]["injuries"]
                season_coverage_predictions = league["seasons"][j]["coverage"]["predictions"]
                season_coverage_odds = league["seasons"][j]["coverage"]["odds"]

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
        
    return results


'''
    Only execute the extraction and loading of league ids on the first day of each month, 
    since this data doesn't change frequently.
'''
if datetime.now().day in [1]:
    league_ids = extract_league_ids(url, headers)

    insert_query = """INSERT INTO usr_landing.leagues
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    conn = pg.connect(args['url_conn'])
    cur = conn.cursor()

    cur.executemany(insert_query, league_ids)

    conn.commit()