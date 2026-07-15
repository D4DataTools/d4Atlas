import json
from pathlib import Path
import os
from dotenv import load_dotenv, dotenv_values
from functools import cache
load_dotenv()

from global_values import *
from set_data import * 
from loader import *
from marker import *
from helpers_geom import *

# from world import * 
# from render import * 



sanctuary_eastern_continent = load_data('World','Sanctuary_Eastern_Continent')
global_markers = load_data('Global','global_markers')

#if VERBOSE: print(f'`global_markers` keys: {global_markers.keys()}')
content_entries = global_markers.get('ptContent')
#if VERBOSE: print(f'global_markers["ptContent"] is of length {len(content_entries)}')

for content_entry in content_entries: 
    #if VERBOSE: print(f'content_entry has keys: {content_entry.keys()}')
    global_marker_actors = content_entry.get('arGlobalMarkerActors')
    #if VERBOSE: print(f'global_marker_actors is of type {type(global_marker_actors)}')
    if not isinstance(global_marker_actors, list): continue

    for global_marker_actor in global_marker_actors:
        #if VERBOSE: print(f'global_maker_actor has keys: {global_marker_actor.keys()}')
        sno_world = global_marker_actor.get('snoWorld')
        sno_world_name = sno_world.get('name')
        sno_marker_set = global_marker_actor.get('snoMarkerSet')
        sno_marker_set_name = sno_marker_set.get('name')
        if(sno_world_name != 'Sanctuary_Eastern_Continent' or not sno_marker_set_name ): continue

        marker_set = load_data(sno_marker_set.get('groupName'), sno_marker_set_name)
        process_marker_set(marker_set)








if VERBOSE: print(f'`sanctuary_eastern_continent` keys: {sanctuary_eastern_continent.keys()}')
server_data = sanctuary_eastern_continent['ptServerData'] 
if VERBOSE: print(f'sanctuary_eastern_continent["ptServerData"] is of length {len(server_data)}')
# This should be cleaned up into functions for readability 
# too many tabs
for x in server_data: 
    # if VERBOSE: print(f'x has keys: {x.keys()}') 
    if x is None: continue

    scene_chunks = x.get('ptSceneChunks')
    for chunk in scene_chunks:
        # if VERBOSE: print(f'chunk keys: {chunk.keys()}')
        scene_spec = chunk.get('tSceneSpec')
        # if VERBOSE: print(f'tSceneSpec keys {scene_spec.keys()}')

        subzones = scene_spec.get('arSubzones')
        # if VERBOSE: print(f'Subzones is of length {len(subzones)}')
        
        for subzone_entry in subzones:
            # if VERBOSE: print(f'subzone_entry keys: {subzone_entry.keys()}')
            subzone_ref = subzone_entry.get('snoSubzone')
            # if VERBOSE: print(subzone_ref)
            # if VERBOSE: print(f'subzone_ref keys: {subzone_ref.keys()}')
            subzone = load_data(subzone_ref.get('groupName'), subzone_ref.get('name'))

            # if VERBOSE: print(f'subzone keys: {subzone.keys()}')

            world_marker_sets = subzone.get('arWorldMarkerSets')
        
            for entry in world_marker_sets:
                # if VERBOSE: print(f'entry keys: {entry.keys()}')
                sno_marker_set = entry.get('snoMarkerSet')
                # if VERBOSE: print(f'sno_marker_set keys {sno_marker_set.keys()}')
                if sno_marker_set and sno_marker_set.get('groupName') == 'MarkerSet':
                    marker_set = load_data(sno_marker_set.get('groupName'), sno_marker_set.get('name'))
                    process_marker_set(marker_set)

        

# process_marker_set()
# write_atlas_html(markers)

