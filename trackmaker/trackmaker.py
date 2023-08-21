import json


with open('src/trackmaker/parameters.json', 'r') as file:
    parameters = json.loads(file.read())

print(parameters['straights'][0]['start'])