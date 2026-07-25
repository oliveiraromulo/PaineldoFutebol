import requests
import json
#import argparse
#import config

import psycopg as pg

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

file = open('/opt/airflow/dags/soccer_analytics/config.json')

args = json.load(file)
headers = {
    'x-rapidapi-host': args['x-rapidapi-host'],
    'x-rapidapi-key': args['x-rapidapi-key']
}

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"

def request_api(url, header, kwargs):
    session = requests.Session()

    retry = Retry(connect=3,
                  status_forcelist=[429],
                  allowed_methods=["GET"],
                  backoff_factor=60)
    
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(url, headers=header, params=kwargs)
    return response


def extract_fixtures_stats(url, headers, querystring, fixture_id):

    #response = requests.get(url, headers=headers, params=querystring)
    response = request_api(url, headers, querystring)
    json_payload = json.loads(response.text)
    
    if json_payload['results'] != 0:
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

    else:
        print(f"Fixture ID: {fixture_id} - No statistics available for this fixture.")

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
        and CURRENT_TIMESTAMP between start_round_date and end_round_date
        --and start_round_date >= current_timestamp - interval '30' DAY
        and cast(fix.league_id as int) = dim.league_id
        and cast(fix.league_season as int) = dim.league_season
        and fix.league_round = dim.league_round
    )
    and cast(fixture_date AS TIMESTAMP ) - INTERVAL '3' HOUR <= current_timestamp
    and fixture_status_short != 'NS'
"""

conn = pg.connect(args['url_conn'])
cur = conn.cursor()

cur.execute(query_fixtures)
fixtures_ids = cur.fetchall()

if len(fixtures_ids) == 0:
    print("No fixtures found for the last round of the championship.")

else:
    result_list = []
    for fixture in fixtures_ids:   
        querystring = {"fixture": fixture[0]}

        returned_result = extract_fixtures_stats(url, headers, querystring, fixture[0])
        if returned_result is not None:
            result_list.append(returned_result)

    insert_query = """INSERT INTO usr_landing.fixture_stats 
    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cur.executemany(insert_query, result_list)

conn.commit()
conn.close()