import requests
import json
#import argparse
#import config

import psycopg as pg

file = open('config.json')

args = json.load(file)

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"

headers = {
    'x-rapidapi-host': args['x-rapidapi-host'],
    'x-rapidapi-key': args['x-rapidapi-key']
}

select_fixtures_query = "SELECT fixture_id FROM usr_landing.fixtures"

cur.execute(select_fixtures_query)

fixtures_list = cur.fetchmany(result)


def extract_fixtures_stats(list_fix):
    results = []
    for r in range(len(list_fix)):
        print(list_fix[r][0])
        querystring = {"fixture": list_fix[r][0]}
        response = requests.get(url, headers=headers, params=querystring)
        print(response.json())
        json_data = json.loads(response.text)
        #with open('fixture_ids.json', 'w') as json_file:
        #    json.dump(json_json_data, json_file, indent=4, ensure_ascii=False)
                
        for i in range(len(json_data['response'])):
            fixture_id = json_data['parameters']['fixture']
            #print(f'ID: {fixture_id}')
            team_id = json_data['response'][i]['team']['id']
            #print(f'team id: {team_id}')
            team_name = json_data['response'][i]['team']['name']
            #print(f'team name: {team_name}')
            tuple_game = (fixture_id, team_id, team_name)
            stats_list = []
            for j in range(len(json_data['response'][i]['statistics'])):
                stats = json_data['response'][i]['statistics'][j]['value']
                stats_list.append(stats)
                print(f'Stats: {stats_list}')
            #tuple_append = tuple(stats_list)
            #print(f'Tuple Append: {tuple_append}')
            tuple_game_status = tuple_game + tuple(stats_list)
            #print(tuple_game_status)
            results.append(tuple_game_status)
    #print(results)
    return results

fixture_stats_return = extract_fixtures_stats(fixtures_list)


#print(results)

insert_query = """INSERT INTO usr_landing.fixtures_stats
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s)"""

conn = pg.connect(args['url_conn'])

cur = conn.cursor()

cur.executemany(insert_query, results)

conn.commit()