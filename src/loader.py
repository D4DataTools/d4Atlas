import json
from pathlib import Path 
import os
from dotenv import load_dotenv, dotenv_values
from functools import cache
from global_values import *




def build_group_index(group_folder: Path):
    index = {}

    for file in group_folder.glob("*.json"):
        # Skeleton.act.json -> Skeleton
        name = file.name.split(".", 1)[0]
        index[name] = file

    return index

@cache
def load_json(filename):
    if VERBOSE: print(f'Opening {filename}')
    with open(filename, encoding="utf-8") as f:
        return json.load(f)

def load_strings(sno_entry, language="enUS"):
    if VERBOSE: print(f'Loading Strings for {sno_entry} ({language})')

    data_root = Path(os.getenv("DATA_ROOT")) 

    if isinstance(sno_entry, str):
        filename = (
            data_root / 
            'json' / 
            f'{language}_Text' / 
            'meta' / 
            'StringList' / 
            f'{sno_entry}.stl.json'
        )
    else:
        filename = (
            data_root /
            'json' /
            f'{language}_Text' / 
            'meta' / 
            'StringList' / 
            f'{sno_entry["groupName"]}_{sno_entry["name"]}.stl.json'
        )

    if not Path(filename).exists():
        return {}

    data = load_json(filename)

    strings = {}

    for s in data.get("arStrings", []):
        strings[s["szLabel"]] = s["szText"]
        strings[s["hLabel"]] = s["szText"]

    return strings

# @cache
# def load_data(group, name):

#     # really hacky solution to a bug I am having 
#     if group == 'SubZone': group = 'Subzone'

#     data_root = Path(os.getenv("DATA_ROOT")) 
#     folder = data_root / 'json' / 'base' / 'meta' / group
    
#     if VERBOSE: print( f'Loading folder: `{folder}`')

#     files = folder.glob(f'{name}.*.json')

#     for file in files:
#         return load_json(Path(file))

#     return {}

@cache
def load_data(group, name):
    folder = SNO_GROUP_MAP.get(group, group)

    path = indexes.get(folder, {}).get(name)
    if path is None:
        return {}

    return load_json(path)


indexes = {}

meta_root = Path(os.getenv('DATA_ROOT')) / "json" / "base" / "meta"

for folder in meta_root.iterdir():
    if folder.is_dir():
        indexes[folder.name] = build_group_index(folder)