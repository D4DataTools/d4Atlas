import json
from pathlib import Path
import os
from dotenv import load_dotenv, dotenv_values
from functools import cache

from global_values import *
from set_data import * 
from loader import *
from marker import *
from helpers_geom import *

load_dotenv()


def format_ar_point(point):
    x = point.get('x')
    y = point.get('y')
    if x is None or y is None: return None
    return(f'{x} {y}')

def format_ar_points(ar_points):
    return ' L '.join( p for point in ar_points if (p := format_ar_point(point)))


def get_boundries_for_static_camp(camp): 
    if camp.get('__type__') != 'TerritoryRegionBoundary': return None 
    sno_territory = camp.get('snoTerritory')
    if not sno_territory: return None 

    strings = load_strings(sno_territory)
    points = format_ar_points(camp.get('arPoints', []))

    return (
        f'<path class="subzone-border" '
        f'd="M {points} z">'
        f'<title>{strings.get("Name", "")}</title></path>'
    )


def process_world(world): 
    for server_data in world.get('ptServerData', []):
        process_server_data(server_data)

def process_server_data(server_data): 
    for scene_chunk in server_data.get('ptSceneChunks', []):
        process_scene_chunk(scene_chunk)

def process_scene_chunk(scene_chunk):
    scene_spec = scene_chunk.get('tSceneSpec')
    if not scene_spec: return 

    for relation in scene_spec.get('arSubzones', []):
        process_subzone_relation(relation)

def process_subzone_relation(relation): 
    subzone_ref = relation.get('snoSubzone')
    if not subzone_ref: return
    subzone = load_data(subzone_ref["groupName"], subzone_ref["name"])
    process_subzone(subzone)

def process_subzone(subzone): 
    for world_marker_set in subzone.get('arWorldMarkerSets'): 
        process_world_marker_set(world_marker_set)

def process_world_marker_set(entry):
    sno_marker_set = entry.get('snoMarkerSet')
    if sno_marker_set and sno_marker_set.get('groupName') == 'MarkerSet':
        marker_set = load_data(sno_marker_set.get('groupName'), sno_marker_set.get('name'))
        process_marker_set(marker_set)

def process_global_markers(global_markers):
    for content_entry in global_markers.get('ptContent', []): 
        process_global_entry(content_entry)

def process_global_entry(content_entry):
    global_marker_actors = content_entry.get('arGlobalMarkerActors')
    if not isinstance(global_marker_actors, list): return
    for global_marker_actor in global_marker_actors:
        process_global_marker_actor(global_marker_actor)

def process_global_marker_actor(global_marker_actor):
    sno_world = global_marker_actor.get('snoWorld')
    sno_world_name = sno_world.get('name')
    sno_marker_set = global_marker_actor.get('snoMarkerSet')
    sno_marker_set_name = sno_marker_set.get('name')
    if(sno_world_name != 'Sanctuary_Eastern_Continent' or not sno_marker_set_name ): return

    process_marker_set(load_data(sno_marker_set.get('groupName'), sno_marker_set_name))