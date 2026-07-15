import json
from pathlib import Path 

import json
from pathlib import Path

def load_json(filename):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def load_strings(sno_entry, language="enUS"):
    if isinstance(sno_entry, str):
        filename = f"./json/{language}_Text/meta/StringList/{sno_entry}.stl.json"
    else:
        filename = (
            f"./json/{language}_Text/meta/StringList/"
            f"{sno_entry['groupName']}_{sno_entry['name']}.stl.json"
        )

    if not Path(filename).exists():
        return {}

    data = load_json(filename)

    strings = {}

    for s in data.get("arStrings", []):
        strings[s["szLabel"]] = s["szText"]
        strings[s["hLabel"]] = s["szText"]

    return strings

def load_data(group, name):
    folder = Path(f'json/base/meta/{group}')

    for file in folder.glob(f'{name}.*.json'):
        return load_json

    return {}