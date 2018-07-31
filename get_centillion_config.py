import json

CONFIG_FILE = 'config_centillion.json'

def get_centillion_config(filename=CONFIG_FILE):
    """
    Load the centillion configuration
    """
    with open(filename,'r') as f:
        d = json.load(f)
    return d

