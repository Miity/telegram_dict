import json


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, 
            indent=2, ensure_ascii = False)

def load_json(filename):
    with open(filename) as json_data:
        json_data = json.load(json_data)
    return json_data