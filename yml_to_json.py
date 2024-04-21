import yaml
import json

with open('he1000se.yml', 'r') as file:
    configuration = yaml.safe_load(file)

with open('he1000se.json', 'w') as json_file:
    json.dump(configuration, json_file)