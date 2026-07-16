import json
from pathlib import Path
import os
from dotenv import load_dotenv, dotenv_values
from functools import cache
import math
load_dotenv()

from global_values import *
from set_data import * 
from loader import *
from marker import *
from helpers_geom import *
from world import *
from render import * 

sanctuary_eastern_continent = load_data('World','Sanctuary_Eastern_Continent')
global_markers = load_data('Global','global_markers')


region_boundries = sanctuary_eastern_continent.get('arRegionBoundaries')

borders = [
    border for camp in region_boundries
    if (border := get_boundries_for_static_camp(camp))
]

process_world(sanctuary_eastern_continent)
process_global_markers(global_markers)

zone_art = calc_zone_art(sanctuary_eastern_continent)

markers_values = sorted(markers.values(), reverse=True)
write_atlas_html(borders, markers_values, zone_art)