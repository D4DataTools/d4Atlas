import os
import json
from pathlib import Path 
from functools import cache

from d4atlas.config import CONFIG, SNO_GROUP_MAP

# Lazily populated index
_indexes = {}

#' Set / Override data_root Used in Loaders
#' @param Path Set the Path 
#' @return None
#' @details Changing the root invalidates folder indexes and cachces.
#' @export
def set_data_root(path: str | Path):

    CONFIG.data_root = Path(path)

    _indexes.clear()
    load_json.cache_clear()

#' Get the meta Root
#' @return a `Path`
def _get_meta_root() -> Path:
    if CONFIG.data_root is None:
        raise RuntimeError(
            'DATA_ROOT has not been configured.\n'
            'Set the DATA_ROOT environment variable or call '
            'd4atlas.set_data_root(...).'
        )

    return CONFIG.data_root / "json" / "base" / "meta"


#' Build an index of Files Within a SNO Group
#'
#' @description Internal function to dramatically increase speed of processing
#' Without the index test runs were taking 5.5 minutes to run. 
#' With the index it was running in 15 seconds.
#' @param group_folder: A `Path` to a copy of the d4Data repo. 
#' @return a `dict` of an index 
#'
def _build_group_index(group_folder: Path):
    index = {}

    for file in group_folder.glob("*.json"):
        name = file.name.split(".", 1)[0]
        index[name] = file

    return index

#' Get The Index For A Given Group
#' 
#' @param group a `str` with the Name of the gruop.
#' @return The index of the specified folder. A`dict` with key of str and Value of `Path`      

def _get_group_index(group: str) -> dict[str, Path]:
    folder = SNO_GROUP_MAP.get(group, group)

    # Early Exit for already indexed folders
    if folder in _indexes: return _indexes[folder]

    group_folder = _get_meta_root() / folder

    if not group_folder.exists():
        _indexes[folder] = {}
        return _indexes[folder]

    if CONFIG.verbose: print(f'Indexing {folder}')
    _indexes[folder] = _build_group_index(group_folder)

    return _indexes[folder]

#' Load a JSON file 
#' @param filename a `Path` to the given JSON.
#' @return a `dict` with the contents of the JSON.
#' @details JSON files are cached
@cache
def load_json(filename: Path):
    if CONFIG.verbose: print(f'Opening {filename}')
    with open(filename, encoding="utf-8") as f:
        return json.load(f)

#' Load a Data from a file
#' @param group a `str` with the name of the group.
#' @param name a `str` with the name of the file.
#' @return a `dict` with the contents of the JSON.
#' @details JSON files are cached
@cache
def load_data(group: str, name: str):
    # Fix for the SubZone groupName not matching
    folder = SNO_GROUP_MAP.get(group, group)
    index = _get_group_index(group)
    path = index.get(name)

    # If path is None the file doesn't exist
    if path is None: return {}

    return load_json(path)

#' Load String Lists From File
#' 
#' @param sno_entry Either a str or a dict containing a reference to a sno object.abs
#' @param language Optional arguement defaults to "enUS"
def load_strings(sno_entry, language: str="enUS"):
    if CONFIG.verbose: print(f'Loading Strings for {sno_entry} ({language})')

    data_root = Path(os.getenv("DATA_ROOT")) 

    if isinstance(sno_entry, str):
        filename = (
            data_root 
            / 'json' 
            / f'{language}_Text' 
            / 'meta' 
            / 'StringList' 
            / f'{sno_entry}.stl.json'
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
        if CONFIG.verbose: 
            print(
                f'⚠️ The referenced sno_entry `{sno_entry}` file does not exists for language: `{language}`'
                f'⚠️ `{filename}` does not exisit.'
                )
        return {}

    data = load_json(filename)

    strings = {}

    for s in data.get("arStrings", []):
        strings[s["szLabel"]] = s["szText"]
        strings[s["hLabel"]] = s["szText"]

    return strings



