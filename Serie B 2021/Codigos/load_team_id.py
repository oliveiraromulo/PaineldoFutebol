import json

file = open('team_ids.json',)

data = json.load(file)

for i in range(len(data['response'])):
    print('ID Equipe: ', data['response'][i]['team']['id'])
    print('País: ', data['response'][i]['team']['country'])
    print('Nome: ', data['response'][i]['team']['name'])
    print('Fundação: ', data['response'][i]['team']['founded'])
    print('Flag Seleção: ', data['response'][i]['team']['national'])
    print('Escudo: ', data['response'][i]['team']['logo'])
    print('ID Estadio: ', data['response'][i]['venue']['id'])
    print('Nome: ', data['response'][i]['venue']['name'])
    print('Local: ', data['response'][i]['venue']['address'])
    print('Cidade: ', data['response'][i]['venue']['city'])
    print('Capacidade: ', data['response'][i]['venue']['capacity'])
    print('Gramado: ', data['response'][i]['venue']['surface'])
    print('Foto: ', data['response'][i]['venue']['image'])

    print('\n')
