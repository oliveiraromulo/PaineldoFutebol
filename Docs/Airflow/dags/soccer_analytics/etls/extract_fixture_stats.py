import requests
import json
#import argparse
#import config

import psycopg as pg # pyright: ignore[reportMissingImports]

file = open('/opt/airflow/dags/soccer_analytics/config.json')
args = json.load(file)

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"

headers = {
    'x-rapidapi-host': args['x-rapidapi-host'],
    'x-rapidapi-key': args['x-rapidapi-key']
}

def extract_fixtures_stats(fixture_id, json_payload):
    result_set = []
    result_set.append(fixture_id)

    for part in json_payload['response']:
        team_id = part['team']['id']
        team_name = part['team']['name']

        result_set.append(team_id)
        result_set.append(team_name)

        for stats in part['statistics']:
                result_set.append(stats['value'])
            
    return result_set

'''
    QUERY TO EXTRACT ALL FIXTURE_IDS FROM THE LAST ROUND OF THE CHAMPIONSHIP
'''
query_fixtures_query = """
    select distinct fixture_id 
    from usr_landing.fixtures 
    where league_season = '2023' 
    and league_round = 'Regular Season - 1'
"""

conn = pg.connect(args['url_conn'])
cur = conn.cursor()

cur.execute(query_fixtures_query)
fixtures_ids = cur.fetchall()

result_list = []
for fixture in fixtures_ids:
    #print(fixture[0])
    
    querystring = {"fixture": fixture[0]}
    response = requests.get(url, headers=headers, params=querystring)
    result_list.append(extract_fixtures_stats(fixture[0], json.loads(response.text)))

print(result_list)

insert_query = """INSERT INTO usr_landing.fixture_stats 
values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

cur.executemany(insert_query, result_list)

conn.commit()
conn.close()