import requests
import json

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

# Deve ser parametrizado de acordo com a necessidade. Ou processa rodada ou processa temporada inteira.
querystring = {
#"date":"2021-11-16",
"league":"71",
"season":"2020"}

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "2014cc0ea1msh118aa5cb2f5f7a4p16f82cjsn0f523407fcf8"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_data = json.loads(response.text)

with open('fixture_ids.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4, ensure_ascii=False)
