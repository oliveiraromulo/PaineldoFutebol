import requests
import json
#import argparse
#import config
from datetime import date
import psycopg as pg # pyright: ignore[reportMissingImports]

file = open('/opt/airflow/dags/soccer_analytics/config.json')
args = json.load(file)
headers = {
    'x-rapidapi-host': args['x-rapidapi-host'],
    'x-rapidapi-key': args['x-rapidapi-key']
    }

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

def extract_fixture_id(url, headers, querystring) -> list:
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)

    results = []

    for fixture in json_data['response']:
        fixture_id = fixture['fixture']['id']
        fixture_referee = fixture['fixture']['referee']
        fixture_timezone = fixture['fixture']['timezone']
        fixture_date = fixture['fixture']['date']
        fixture_timestamp = fixture['fixture']['timestamp']
        fixture_period_first = fixture['fixture']['periods']['first']
        fixture_period_second = fixture['fixture']['periods']['second']
        fixture_venue_id = fixture['fixture']['venue']["id"]
        fixture_venue_name = fixture['fixture']['venue']["name"]
        fixture_venue_city = fixture['fixture']['venue']["city"]
        fixture_status_long = fixture['fixture']['status']["long"]
        fixture_status_short = fixture['fixture']['status']["short"]
        fixture_status_elapsed = fixture['fixture']['status']["elapsed"]

        league_id = fixture['league']['id']
        league_name = fixture['league']['name']
        league_country = fixture['league']['country']
        league_logo = fixture['league']['logo']
        league_flag = fixture['league']['flag']
        league_season = fixture['league']['season']
        league_round = fixture['league']['round']

        teams_home_id = fixture['teams']['home']['id']
        teams_home_name = fixture['teams']['home']['name']
        teams_home_logo = fixture['teams']['home']['logo']
        teams_home_winner = fixture['teams']['home']['winner']
        teams_away_id = fixture['teams']['away']['id']
        teams_away_name = fixture['teams']['away']['name']
        teams_away_logo = fixture['teams']['away']['logo']
        teams_away_winner = fixture['teams']['away']['winner']

        goals_home =  fixture['goals']['home']
        goals_away = fixture['goals']['away']

        score_halftime_home = fixture['score']['halftime']['home']
        score_halftime_away = fixture['score']['halftime']['away']
        score_fulltime_home = fixture['score']['fulltime']['home']
        score_fulltime_away = fixture['score']['fulltime']['away']
        score_extratime_home = fixture['score']['extratime']['home']
        score_extratime_away = fixture['score']['extratime']['away']
        score_penalty_home = fixture['score']['penalty']['home']
        score_penalty_away = fixture['score']['penalty']['away']

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

    return results


query_league = f"""
    select 
        league_id,
        league_name,
        country_name,
        season_year, 
        row_number() over(partition by league_id order by season_year, created_at desc) row_num
    from usr_landing.leagues
    where cast(season_start as date) <= current_date
    or cast(season_end as date) >= current_date
"""

conn = pg.connect(args['url_conn'])
cur = conn.cursor()

cur.execute(query_league)
leagues = cur.fetchall()

for league in leagues:
    querystring = {
        #"date":"2021-11-16",
        "league": f"{league[0]}",
        "season": f"{league[3]}"
    }

    print("Extracting fixtures from : ", league[1], " - ", league[2], " and season: ", league[3])

    print(querystring)

    fixtures = extract_fixture_id(url, headers, querystring)

    insert_query = """INSERT INTO usr_landing.fixtures
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s)"""

    cur.executemany(insert_query, fixtures)

    conn.commit()

conn.close()