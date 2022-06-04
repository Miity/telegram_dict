from secret import URL
import requests
import json


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, 
            indent=2, ensure_ascii = False)

def load_json(filename):
    with open(filename) as json_data:
        json_data = json.load(json_data)
    return json_data

def get_updates(offset = None):
    url = URL + "getUpdates"
    if offset:
        r = requests.get(url, params = {'offset': offset })
    else:
        r = requests.get(url)
    return r.json()

def is_new_updates(r, update_id):
    try:
        if r['result'][-1]['update_id'] != update_id:
            update_id = r['result'][-1]['update_id']
            return True

        elif update_id == r['result'][-1]['update_id']:
            return False
    except:
        return False
    
    