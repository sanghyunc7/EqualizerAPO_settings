import json
import yaml

with open('he1000se.json', 'r') as file:
    configuration = json.load(file)

with open('out.yml', 'w') as yaml_file:
    yaml.dump(configuration, yaml_file)