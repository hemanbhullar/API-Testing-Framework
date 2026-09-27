import json
from pathlib import Path

#JSON Data Provider
def read_json_data(filepath):
    print(filepath)
    with open(filepath, 'r') as f:
        data_list = json.load(f)
    return [(item["email"], item["password"])for item in data_list]
