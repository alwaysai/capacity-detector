import os
import json

def load_json(filepath):
    if os.path.exists(filepath) == False:
        raise Exception('File at {} does not exist'.format(filepath))
    with open(filepath) as data:
        return json.load(data)
