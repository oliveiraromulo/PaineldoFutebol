import json

file = open('fixture_ids.json',)

data = json.load(file)

for i in range(len(data['response'])):
    print('ID Campeonato: ', data['response'][i]['league']['id'])
    print('País: ', data['response'][i]['league']['country'])
    print('Rodada: ', data['response'][i]['league']['round'])
    print('Temporada: ', data['response'][i]['league']['season'])
    print('Data: ', data['response'][i]['fixture']['date'])
    print('ID Estadio: ', data['response'][i]['fixture']['venue']['id'])
    print('Nome Estadio: ', data['response'][i]['fixture']['venue']['name'])
    print('Local Estadio: ', data['response'][i]['fixture']['venue']['city'])
    print('ID Equipe Casa: ', data['response'][i]['teams']['home']['id'])
    print('Nome Equipe Casa: ', data['response'][i]['teams']['home']['name'])
    print('ID Equipe Fora: ', data['response'][i]['teams']['away']['id'])
    print('Nome Equipe Fora: ', data['response'][i]['teams']['away']['name'])
    print('Gols Equipe Casa: ', data['response'][i]['goals']['home'])
    print('Gols Equipe Fora: ', data['response'][i]['goals']['away'])

    print('\n')
