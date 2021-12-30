import json

file = open('league_ids.json',)

data = json.load(file)

for i in range(len(data['response'])):
    print(data['response'][i]['country'])
    print(data['response'][i]['league'])
    print('Quantidade de temporadas: ', len(data['response'][i]['seasons']))
