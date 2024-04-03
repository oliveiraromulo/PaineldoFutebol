import requests
import json
#import argparse
#import config

import psycopg as pg

file = open('config.json')

args = json.load(file)

url = "https://api-football-v1.p.rapidapi.com/v3/teams"

querystring = {"country":"Brazil"}

headers = {
    'x-rapidapi-host': args['x-rapidapi-host'],
    'x-rapidapi-key': args['x-rapidapi-key']
    }
    
response = requests.request("GET", url, headers=headers, params=querystring)

json_data = json.loads(response.text)

#with open('team_ids.json', 'w') as json_file:
#    json.dump(json_data, json_file, indent=4, ensure_ascii=False)

results = []

for i in range(len(json_data['response'])):
    #print('ID Equipe: ', data['response'][i]['team']['id'])
    #print('País: ', data['response'][i]['team']['country'])
    #print('Nome: ', data['response'][i]['team']['name'])
    #print('Fundação: ', data['response'][i]['team']['founded'])
    #print('Flag Seleção: ', data['response'][i]['team']['national'])
    #print('Escudo: ', data['response'][i]['team']['logo'])
    #print('ID Estadio: ', data['response'][i]['venue']['id'])
    #print('Nome: ', data['response'][i]['venue']['name'])
    #print('Local: ', data['response'][i]['venue']['address'])
    #print('Cidade: ', data['response'][i]['venue']['city'])
    #print('Capacidade: ', data['response'][i]['venue']['capacity'])
    #print('Gramado: ', data['response'][i]['venue']['surface'])
    #print('Foto: ', data['response'][i]['venue']['image'])


    team_id = json_data['response'][i]['team']['id']
    team_country = json_data['response'][i]['team']['country']
    team_name = json_data['response'][i]['team']['name']
    team_founded = json_data['response'][i]['team']['founded']
    team_national = json_data['response'][i]['team']['national']
    team_logo = json_data['response'][i]['team']['logo']
    venue_id = json_data['response'][i]['venue']['id']
    venue_name = json_data['response'][i]['venue']['name']
    venue_address = json_data['response'][i]['venue']['address']
    venue_city = json_data['response'][i]['venue']['city']
    venue_capacity = json_data['response'][i]['venue']['capacity']
    venue_surface = json_data['response'][i]['venue']['surface']
    venue_image = json_data['response'][i]['venue']['image']

    results.append((
    team_id,
    team_country,
    team_name,
    team_founded,
    team_national,
    team_logo,
    venue_id,
    venue_name,
    venue_address,
    venue_city,
    venue_capacity,
    venue_surface,
    venue_image))

insert_query = """INSERT INTO usr_landing.teams
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

conn = pg.connect(args['url_conn'])
cur = conn.cursor()

cur.executemany(insert_query, results)

conn.commit()