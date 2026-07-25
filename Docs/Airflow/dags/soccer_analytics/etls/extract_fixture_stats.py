import requests
import json
#import argparse
#import config

import psycopg as pg # pyright: ignore[reportMissingImports]

file = open('/opt/airflow/dags/soccer_analytics/config.json')
#file = open('/home/romulo/Documents/Git/PaineldoFutebol/Serie B 2021/Codigos/config.json')
args = json.load(file)
headers = {
    'x-rapidapi-host': args['x-rapidapi-host'],
    'x-rapidapi-key': args['x-rapidapi-key']
}

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"

def extract_fixtures_stats(url, headers, querystring, fixture_id):
    response = requests.get(url, headers=headers, params=querystring)
    json_payload = json.loads(response.text)

    result_set = []
    result_set.append(fixture_id)

    for part in json_payload['response']:
        team_id = part['team']['id']
        team_name = part['team']['name']

        result_set.append(team_id)
        result_set.append(team_name)

        for stats in part['statistics']:
            if stats['type'] not in ['goals_prevented']:
                result_set.append(stats['value'])
            
    return result_set

'''
    Query to extract all fixture_ids from the last round of the championship
'''
query_fixtures = """
    select distinct fixture_id 
    from usr_landing.fixtures fix
    where exists (
        select league_id, league_season, league_season
        from dimension.dim_rounds dim
        where 1=1
        --and CURRENT_TIMESTAMP between start_round_date and end_round_date
        and cast(fix.league_id as int) = dim.league_id
        and cast(fix.league_season as int) = dim.league_season
        and fix.league_round = dim.league_round
    )
    and cast(fixture_date AS TIMESTAMP ) - INTERVAL '3' HOUR <= current_timestamp
    and fixture_status_short = 'FT'
"""

conn = pg.connect(args['url_conn'])
cur = conn.cursor()

cur.execute(query_fixtures)
fixtures_ids = cur.fetchall()

result_list = []
for fixture in fixtures_ids:   
    querystring = {"fixture": fixture[0]}
    
    result_list.append(extract_fixtures_stats(url, headers, querystring, fixture[0]))

#print(result_list)

insert_query = """INSERT INTO usr_landing.fixture_stats 
values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

cur.executemany(insert_query, result_list)

conn.commit()
conn.close()