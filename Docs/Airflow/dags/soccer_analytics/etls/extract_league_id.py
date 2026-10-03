import requests
import json
from datetime import datetime

import psycopg as pg # pyright: ignore[reportMissingImports]
from auxiliar_funcs import upload_file_to_volume, get_api_credentials

'''
    Reading configuration files and setting headers for API requests and databases
'''
args = get_api_credentials('dev') # 'prd' or 'dev' depending on the environment

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
            txt = "ID: {} - Nome: {} - {} | Temporadas: {}".format(league["league"]["id"], 
                                                                   league["country"]["name"],
                                                                   league["league"]["name"],
                                                                   len(league["seasons"])
                                                                )
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

            json_league = {
                "league_id": league_id, 
                "league_name": league_name, 
                "league_type": league_type, 
                "league_logo": league_logo, 
                "country_name": country_name, 
                "country_code": country_code,
                "country_flag": country_flag,
                "season_year": season_year,
                "season_start": season_start,
                "season_end": season_end,
                "season_current": season_current,
                "season_coverage_fixtures_events": season_coverage_fixtures_events,
                "season_coverage_fixtures_lineups": season_coverage_fixtures_lineups,
                "season_coverage_fixtures_statistics_fixtures": season_coverage_fixtures_statistics_fixtures,
                "season_coverage_fixtures_statistics_players": season_coverage_fixtures_statistics_players,
                "season_coverage_stadings": season_coverage_stadings,
                "season_coverage_players": season_coverage_players,
                "season_coverage_top_scorers": season_coverage_top_scorers,
                "season_coverage_top_assists": season_coverage_top_assists,
                "season_coverage_top_cards": season_coverage_top_cards,
                "season_coverage_injuries": season_coverage_injuries,
                "season_coverage_predictions": season_coverage_predictions,
                "season_coverage_odds": season_coverage_odds
            }

            print(json_league)
        
            filename = "league_id_{}_{}.json".format(league_id, datetime.now().strftime("%Y%m%d_%H%M%S"))

            local_path = "/home/romulo/Documents/Git/PaineldoFutebol/Docs/Airflow/dags/soccer_analytics/etls/"
            with open(f"{local_path}{filename}", "w") as json_file:
                json.dump(json_league, json_file)
        
            upload_file_to_volume(#local_file_path=f"/opt/airflow/{filename}",
                                   local_file_path=f"{local_path}{filename}",
                                    catalog='footballdb',
                                    volume='jsonfiles',
                                    folder='leagues',
                                    filename=filename)

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
    Only execute the extraction and load new league ids on the first day of each month
    since this data doesn't change frequently.
'''

if datetime.now().day in [10]:
    league_ids = extract_league_ids(url, headers)

    insert_query = """
        MERGE INTO dimension.dim_leagues as dim
        USING (
            SELECT  %s as league_id
                    %s as league_name
                    %s as league_type
                    %s as league_logo
                    %s as country_name
                    %s as country_code
                    %s as country_flag
                    %s as season_year
                    %s as season_start
                    %s as season_end
                    %s as season_current
                    %s as season_coverage_fixtures_events
                    %s as season_coverage_fixtures_lineups
                    %s as season_coverage_fixtures_statistics_fixtures
                    %s as season_coverage_fixtures_statistics_players
                    %s as season_coverage_stadings
                    %s as season_coverage_players
                    %s as season_coverage_top_scorers
                    %s as season_coverage_top_assists
                    %s as season_coverage_top_cards
                    %s as season_coverage_injuries
                    %s as season_coverage_predictions
                    %s as season_coverage_odds
            ) as aux
        ON (dim.league_id = src.league_id
        and dim.season_year = src.season_year)
        WHEN NOT MATCHED THEN 
            INSERT VALUES (src.league_id
                           src.league_name
                           src.league_type
                           src.league_logo
                           src.country_name
                           src.country_code
                           src.country_flag
                           src.season_year
                           src.season_start
                           src.season_end
                           src.season_current
                           src.season_coverage_fixtures_events
                           src.season_coverage_fixtures_lineups
                           src.season_coverage_fixtures_statistics_fixtures
                           src.season_coverage_fixtures_statistics_players
                           src.season_coverage_stadings
                           src.season_coverage_players
                           src.season_coverage_top_scorers
                           src.season_coverage_top_assists
                           src.season_coverage_top_cards
                           src.season_coverage_injuries
                           src.season_coverage_predictions
                           src.season_coverage_odds)
    """

    conn = pg.connect(args['url_conn'])
    cur = conn.cursor()

    cur.executemany(insert_query, league_ids)

    conn.commit()