import json
config_file = 'config/config.json'

with open(config_file, 'r') as config_json:
    config = json.load(config_json)
